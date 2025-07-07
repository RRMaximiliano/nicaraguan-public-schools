"""
Enhanced Nicaragua Schools Scraper
This version extracts additional metadata from dropdown menus including:
- School IDs from "Buscar Centros Educativos"
- Modality IDs from "Buscar por Modalidad" 
- Program IDs from "Buscar por Programa Educativo"
"""

import pandas as pd
import re
import html
import time
import random
import os
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, JavascriptException, WebDriverException
from bs4 import BeautifulSoup


def extract_dropdown_data(page_source):
    """
    Extract school IDs, modality IDs, and program IDs from dropdown menus.
    
    Returns:
        dict: Contains schools_lookup, modalities_lookup, programs_lookup
    """
    soup = BeautifulSoup(page_source, 'html.parser')
    
    # Extract school IDs and names from "Buscar Centros Educativos"
    schools_lookup = {}
    school_select = soup.find('select', {'name': 'ctl00$ContentPlaceHolder1$ddlCentroEducativo'})
    if not school_select:
        # Try alternative selectors
        school_select = soup.find('select', id=lambda x: x and 'ddlCentroEducativo' in x)
    
    if school_select:
        for option in school_select.find_all('option'):
            value = option.get('value')
            text = option.text.strip()
            if value and value != '' and text and text != 'SELECCIONE':
                schools_lookup[text] = {
                    'school_id': value,
                    'school_name': html.unescape(text)
                }
    
    # Extract modality IDs from "Buscar por Modalidad"
    modalities_lookup = {}
    modality_select = soup.find('select', {'name': 'ctl00$ContentPlaceHolder1$ddlModalidad'})
    if not modality_select:
        modality_select = soup.find('select', id=lambda x: x and 'ddlModalidad' in x)
    
    if modality_select:
        for option in modality_select.find_all('option'):
            value = option.get('value')
            text = option.text.strip()
            if value and value != '' and text and text != 'SELECCIONE':
                modalities_lookup[text] = {
                    'modality_id': value,
                    'modality_name': html.unescape(text)
                }
    
    # Extract program IDs from "Buscar por Programa Educativo"
    programs_lookup = {}
    program_select = soup.find('select', {'name': 'ctl00$ContentPlaceHolder1$ddlPrograma'})
    if not program_select:
        program_select = soup.find('select', id=lambda x: x and 'ddlPrograma' in x)
    
    if program_select:
        for option in program_select.find_all('option'):
            value = option.get('value')
            text = option.text.strip()
            if value and value != '' and text and text != 'SELECCIONE':
                programs_lookup[text] = {
                    'program_id': value,
                    'program_name': html.unescape(text)
                }
    
    return {
        'schools_lookup': schools_lookup,
        'modalities_lookup': modalities_lookup,
        'programs_lookup': programs_lookup
    }


def get_enhanced_school_data_from_page_source(page_source):
    """
    Extract school data from the page source AND dropdown metadata.
    """
    # Get the original school data
    schools_data = get_school_data_from_page_source_original(page_source)
    
    # Get dropdown metadata
    dropdown_data = extract_dropdown_data(page_source)
    
    # Enhance school data with IDs where possible
    enhanced_schools = []
    for school in schools_data:
        enhanced_school = school.copy()
        
        # Try to match school name to get school_id
        school_name = school.get('Nombre', '').strip()
        school_id = None
        
        # Look for exact match first
        if school_name in dropdown_data['schools_lookup']:
            school_id = dropdown_data['schools_lookup'][school_name]['school_id']
        else:
            # Try partial matching (sometimes names might have slight differences)
            for lookup_name, lookup_data in dropdown_data['schools_lookup'].items():
                if school_name.upper() in lookup_name.upper() or lookup_name.upper() in school_name.upper():
                    school_id = lookup_data['school_id']
                    break
        
        enhanced_school['school_id'] = school_id
        
        # Try to match modalities to get modality IDs
        modalities_text = school.get('Modalidades', '')
        matched_modality_ids = []
        matched_modality_names = []
        matched_program_ids = []
        matched_program_names = []
        
        if modalities_text:
            modalities_list = [m.strip() for m in modalities_text.split(',')]
            
            for modality in modalities_list:
                modality_normalized = modality.upper().strip()
                
                # Try exact match first for modalities
                modality_matched = False
                for lookup_modality, lookup_data in dropdown_data['modalities_lookup'].items():
                    lookup_normalized = lookup_modality.upper().strip()
                    if modality_normalized == lookup_normalized:
                        matched_modality_ids.append(lookup_data['modality_id'])
                        matched_modality_names.append(lookup_data['modality_name'])
                        modality_matched = True
                        break
                
                # If no exact match, try partial matching (but more carefully)
                if not modality_matched:
                    for lookup_modality, lookup_data in dropdown_data['modalities_lookup'].items():
                        lookup_normalized = lookup_modality.upper().strip()
                        # Only match if the modality is a significant substring (avoid short matches)
                        if (len(modality_normalized) > 3 and modality_normalized in lookup_normalized) or \
                           (len(lookup_normalized) > 3 and lookup_normalized in modality_normalized):
                            matched_modality_ids.append(lookup_data['modality_id'])
                            matched_modality_names.append(lookup_data['modality_name'])
                            break
                
                # Try exact match first for programs
                program_matched = False
                for lookup_program, lookup_data in dropdown_data['programs_lookup'].items():
                    lookup_normalized = lookup_program.upper().strip()
                    if modality_normalized == lookup_normalized:
                        matched_program_ids.append(lookup_data['program_id'])
                        matched_program_names.append(lookup_data['program_name'])
                        program_matched = True
                        break
                
                # If no exact match, try partial matching for programs
                if not program_matched:
                    for lookup_program, lookup_data in dropdown_data['programs_lookup'].items():
                        lookup_normalized = lookup_program.upper().strip()
                        # Only match if the modality is a significant substring
                        if (len(modality_normalized) > 3 and modality_normalized in lookup_normalized) or \
                           (len(lookup_normalized) > 3 and lookup_normalized in modality_normalized):
                            matched_program_ids.append(lookup_data['program_id'])
                            matched_program_names.append(lookup_data['program_name'])
                            break
        
        enhanced_school['modality_ids'] = ','.join(matched_modality_ids) if matched_modality_ids else None
        enhanced_school['modality_labels'] = ','.join(matched_modality_names) if matched_modality_names else None
        enhanced_school['program_ids'] = ','.join(matched_program_ids) if matched_program_ids else None
        enhanced_school['program_labels'] = ','.join(matched_program_names) if matched_program_names else None
        
        enhanced_schools.append(enhanced_school)
    
    return enhanced_schools, dropdown_data


def get_school_data_from_page_source_original(page_source):
    """
    Original function to extract school data from the page source using regex patterns.
    """
    marker_pattern = r'L\.marker\(\[([^,]+),\s*([^,]+)\].*?\.bindPopup\(\'([^\']*)\'\);'
    
    schools_data = []
    
    # Find all marker matches
    matches = re.finditer(marker_pattern, page_source, re.DOTALL)
    
    for match in matches:
        lat = match.group(1).strip()
        lon = match.group(2).strip()
        popup_html = match.group(3)
        
        # Extract name
        name_pattern = r"<b>Nombre:</b>\s*([^<]+)"
        name_match = re.search(name_pattern, popup_html)
        name = html.unescape(name_match.group(1).strip()) if name_match else "N/A"
        
        # Extract address
        address_pattern = r"<b>Dirección:</b>\s*([^<]+)"
        address_match = re.search(address_pattern, popup_html)
        address = html.unescape(address_match.group(1).strip()) if address_match else "N/A"
        
        # Extract modalities
        modalities_pattern = r"<li>([^<]+)</li>"
        modalities = [html.unescape(m.strip()) for m in re.findall(modalities_pattern, popup_html)]
        
        # Store the school data
        schools_data.append({
            "Nombre": name,
            "Latitud": lat,
            "Longitud": lon,
            "Direccion": address,
            "Modalidades": ", ".join(modalities)
        })
    
    return schools_data


def save_dropdown_metadata(dropdown_data, department_name, municipality_name, output_dir="data/raw"):
    """
    Save the dropdown metadata for reference and debugging.
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Save schools lookup
    if dropdown_data['schools_lookup']:
        schools_df = pd.DataFrame([
            {
                'school_name': data['school_name'],
                'school_id': data['school_id'],
                'department': department_name,
                'municipality': municipality_name
            }
            for name, data in dropdown_data['schools_lookup'].items()
        ])
        schools_file = os.path.join(output_dir, f"schools_lookup_{department_name}_{municipality_name}_{timestamp}.csv")
        schools_df.to_csv(schools_file, index=False, encoding='utf-8')
    
    # Save modalities lookup
    if dropdown_data['modalities_lookup']:
        modalities_df = pd.DataFrame([
            {
                'modality_name': data['modality_name'],
                'modality_id': data['modality_id'],
                'department': department_name,
                'municipality': municipality_name
            }
            for name, data in dropdown_data['modalities_lookup'].items()
        ])
        modalities_file = os.path.join(output_dir, f"modalities_lookup_{department_name}_{municipality_name}_{timestamp}.csv")
        modalities_df.to_csv(modalities_file, index=False, encoding='utf-8')
    
    # Save programs lookup
    if dropdown_data['programs_lookup']:
        programs_df = pd.DataFrame([
            {
                'program_name': data['program_name'],
                'program_id': data['program_id'],
                'department': department_name,
                'municipality': municipality_name
            }
            for name, data in dropdown_data['programs_lookup'].items()
        ])
        programs_file = os.path.join(output_dir, f"programs_lookup_{department_name}_{municipality_name}_{timestamp}.csv")
        programs_df.to_csv(programs_file, index=False, encoding='utf-8')


# Test function to try this enhancement on a single municipality
def test_enhanced_scraper(department_name="Boaco", municipality_name="Boaco"):
    """
    Test the enhanced scraper on a single municipality to verify it works.
    """
    print(f"Testing enhanced scraper on {department_name} - {municipality_name}")
    
    # Import the required functions from the main scraper
    import sys
    sys.path.append('.')
    
    try:
        # Import from the original scraper
        from scripts.python.nicaragua_schools_scraper import (
            DEPARTMENTS, create_stealth_driver, human_like_navigation
        )
        
        municipality_id = DEPARTMENTS[department_name]['municipalities'][municipality_name]
        dept_id = DEPARTMENTS[department_name]['id']
        
        driver = create_stealth_driver()
        if not driver:
            print("Failed to create driver")
            return None
        
        try:
            # Navigate to the page
            human_like_navigation(driver, "https://serviciosenlinea.mined.gob.ni/", "main website")
            human_like_navigation(driver, "https://serviciosenlinea.mined.gob.ni/mapa-de-la-educacion/", "education map")
            
            department_url = f"https://serviciosenlinea.mined.gob.ni/mapa-de-la-educacion/Departamento.aspx?Departamento={dept_id}"
            human_like_navigation(driver, department_url, f"department {department_name}")
            
            time.sleep(5)
            
            municipality_url = f"https://serviciosenlinea.mined.gob.ni/mapa-de-la-educacion/Georreferencia.aspx?Municipio={municipality_id}"
            human_like_navigation(driver, municipality_url, f"municipality {municipality_name}")
            
            # Wait for page to load completely
            WebDriverWait(driver, 45).until(lambda d: "L.marker" in d.page_source)
            time.sleep(5)  # Extra time for dropdowns to populate
            
            page_source = driver.page_source
            
            # Test the enhanced extraction
            enhanced_schools, dropdown_data = get_enhanced_school_data_from_page_source(page_source)
            
            print(f"Found {len(enhanced_schools)} schools")
            print(f"Found {len(dropdown_data['schools_lookup'])} schools in dropdown")
            print(f"Found {len(dropdown_data['modalities_lookup'])} modalities in dropdown")
            print(f"Found {len(dropdown_data['programs_lookup'])} programs in dropdown")
            
            # Save metadata for reference
            save_dropdown_metadata(dropdown_data, department_name, municipality_name)
            
            # Save test results
            if enhanced_schools:
                df = pd.DataFrame(enhanced_schools)
                test_file = f"data/raw/test_enhanced_{department_name}_{municipality_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
                df.to_csv(test_file, index=False, encoding='utf-8')
                print(f"Test results saved to: {test_file}")
            
            # Save dropdown metadata
            save_dropdown_metadata(dropdown_data, department_name, municipality_name)
            
            # Show sample data
            if enhanced_schools:
                print("\nSample enhanced school data:")
                for i, school in enumerate(enhanced_schools[:3]):
                    print(f"School {i+1}:")
                    print(f"  Name: {school['Nombre']}")
                    print(f"  School ID: {school.get('school_id', 'Not found')}")
                    print(f"  Modalities: {school['Modalidades']}")
                    print(f"  Modality IDs: {school.get('modality_ids', 'Not found')}")
                    print(f"  Program IDs: {school.get('program_ids', 'Not found')}")
                    print()
            
            return enhanced_schools, dropdown_data
            
        finally:
            driver.quit()
    
    except Exception as e:
        print(f"Error in test: {e}")
        return None


if __name__ == "__main__":
    # Run test
    result = test_enhanced_scraper()
    if result:
        print("Enhanced scraper test completed successfully!")
    else:
        print("Enhanced scraper test failed.")
