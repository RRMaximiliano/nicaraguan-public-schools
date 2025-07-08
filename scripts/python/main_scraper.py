#!/usr/bin/env python3
"""
Nicaragua Schools Scraper - Complete Edition
Author: Rony Rodriguez
Date: July 2025

This is the main scraper for extracting comprehensive school data from Nicaragua's 
Ministry of Education website. It includes all enhanced features:
- Basic school information (name, coordinates, address, modalities)
- School IDs from dropdown menus
- Modality IDs and labels
- Program IDs and labels
- Department and municipality information

Usage:
    python main_scraper.py                    # Interactive mode
    python main_scraper.py --all              # Scrape all departments
    python main_scraper.py --dept Managua     # Scrape specific department
"""

import pandas as pd
import re
import html
import time
import random
import os
import sys
import argparse
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, JavascriptException, WebDriverException
from bs4 import BeautifulSoup

# Department and municipality mapping
DEPARTMENTS = {
    "Boaco": {
        "id": 11,
        "municipalities": {
            "Boaco": 100,
            "Camoapa": 101,
            "San José de los Remates": 97,
            "San Lorenzo": 102,
            "Santa Lucía": 99,
            "Teustepe": 98,
        },
    },
    "Carazo": {
        "id": 8,
        "municipalities": {
            "Diriamba": 76,
            "Dolores": 77,
            "El Rosario": 79,
            "Jinotepe": 78,
            "La Conquista": 82,
            "La Paz de Carazo": 80,
            "San Marcos": 75,
            "Santa Teresa": 81,
        },
    },
    "Chinandega": {
        "id": 4,
        "municipalities": {
            "Chichigalpa": 39,
            "Chinandega": 36,
            "Cinco Pinos": 32,
            "Corinto": 38,
            "El Realejo": 37,
            "El Viejo": 28,
            "Posoltega": 40,
            "Puerto Morazán": 29,
            "San Francisco del Norte": 34,
            "San Pedro del Norte": 33,
            "Santo Tomás del Norte": 31,
            "Somotillo": 30,
            "Villanueva": 35,
        },
    },
    "Chontales": {
        "id": 12,
        "municipalities": {
            "Acoyapa": 109,
            "Comalapa": 103,
            "San Francisco de Cuapa": 111,
            "El Coral": 112,
            "Juigalpa": 104,
            "La Libertad": 105,
            "San Pedro de Lóvago": 107,
            "Santo Domingo": 106,
            "Santo Tomás": 108,
            "Villa Sandino": 110,
        },
    },
    "Estelí": {
        "id": 3,
        "municipalities": {
            "Condega": 23,
            "Estelí": 25,
            "La Trinidad": 26,
            "Pueblo Nuevo": 22,
            "San Juan de Limay": 24,
            "San Nicolás": 27,
        },
    },
    "Granada": {
        "id": 9,
        "municipalities": {
            "Diriá": 84,
            "Diriomo": 85,
            "Granada": 83,
            "Nandaime": 86
        },
    },
    "Jinotega": {
        "id": 13,
        "municipalities": {
            "El Cuá": 120,
            "Jinotega": 119,
            "La Concordia": 116,
            "San José de Bocay": 121,
            "San Rafael del Norte": 117,
            "San Sebastián de Yalí": 115,
            "Santa María de Pantasma": 118,
            "Wiwilí de Jinotega": 114,
        },
    },
    "León": {
        "id": 5,
        "municipalities": {
            "Achuapa": 46,
            "El Jicaral": 48,
            "El Sauce": 45,
            "La Paz Centro": 49,
            "Larreynaga": 44,
            "León": 41,
            "Nagarote": 50,
            "Quezalguaque": 42,
            "Santa Rosa del Peñón": 47,
            "Telica": 43,
        },
    },
    "Madriz": {
        "id": 2,
        "municipalities": {
            "Las Sabanas": 20,
            "Palacagüina": 18,
            "San José de Cusmapa": 21,
            "San Juan de Río Coco": 16,
            "San Lucas": 19,
            "Somoto": 13,
            "Telpaneca": 15,
            "Totogalpa": 14,
            "Yalagüina": 17,
        },
    },
    "Managua": {
        "id": 6,
        "municipalities": {
            "El Crucero": 58,
            "Managua": 59,
            "Mateare": 53,
            "San Francisco Libre": 51,
            "San Rafael del Sur": 55,
            "Ticuantepe": 57,
            "Tipitapa": 52,
            "Villa El Carmen": 54,
            "Ciudad Sandino": 56,
        },
    },
    "Masaya": {
        "id": 7,
        "municipalities": {
            "Catarina": 72,
            "La Concepción": 66,
            "Masatepe": 70,
            "Masaya": 68,
            "Nandasmo": 71,
            "Nindirí": 67,
            "Niquinohomo": 73,
            "San Juan de Oriente": 74,
            "Tisma": 69,
        },
    },
    "Matagalpa": {
        "id": 14,
        "municipalities": {
            "Ciudad Darío": 125,
            "Esquipulas": 128,
            "Matagalpa": 130,
            "Matiguás": 134,
            "Muy Muy": 129,
            "Rancho Grande": 133,
            "Río Blanco": 135,
            "San Dionisio": 127,
            "San Isidro": 123,
            "San Ramón": 131,
            "Sébaco": 124,
            "Terrabona": 126,
            "El Tuma La Dalia": 132,
        },
    },
    "Nueva Segovia": {
        "id": 1,
        "municipalities": {
            "Ciudad Antigua": 7,
            "Dipilto": 3,
            "El Jícaro": 8,
            "Jalapa": 9,
            "Macuelizo": 2,
            "Mozonte": 5,
            "Murra": 10,
            "Ocotal": 4,
            "Quilalí": 11,
            "San Fernando": 6,
            "Santa María": 1,
            "Wiwilí de Nueva Segovia": 12,
        },
    },
    "Rivas": {
        "id": 10,
        "municipalities": {
            "Altagracia": 96,
            "Belén": 88,
            "Buenos Aires": 90,
            "Cárdenas": 94,
            "Moyogalpa": 95,
            "Potosí": 89,
            "Rivas": 91,
            "San Jorge": 92,
            "San Juan del Sur": 93,
            "Tola": 87,
        },
    },
    "Río San Juan": {
        "id": 17,
        "municipalities": {
            "El Almendro": 156,
            "El Castillo": 159,
            "Morrito": 155,
            "San Carlos": 158,
            "San Juan de Nicaragua": 160,
            "San Miguelito": 157,
        },
    },
    "RACCN": {
        "id": 15,
        "municipalities": {
            "Bonanza": 137,
            "Mulukukú": 143,
            "Prinzapolka": 142,
            "Puerto Cabezas": 139,
            "Rosita": 138,
            "Siuna": 141,
            "Waslala": 140,
            "Waspán": 136,
        },
    },
    "RACCS": {
        "id": 16,
        "municipalities": {
            "Bluefields": 151,
            "Corn Island": 152,
            "Desembocadura de la Cruz de Río Grande": 154,
            "El Ayote": 113,
            "El Rama": 148,
            "El Tortuguero": 153,
            "Kukra Hill": 147,
            "La Cruz de Río Grande": 145,
            "Laguna de Perlas": 146,
            "Muelle de los Bueyes": 149,
            "Nueva Guinea": 150,
            "Paiwas": 144,
        },
    },
}

def create_stealth_driver():
    """
    Create a Chrome WebDriver with stealth options to avoid detection.
    
    Returns:
        webdriver.Chrome: Configured Chrome driver or None if failed
    """
    try:
        options = webdriver.ChromeOptions()
        
        # Stealth options
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_argument('--disable-features=VizDisplayCompositor')
        options.add_argument('--disable-extensions')
        options.add_argument('--disable-plugins')
        options.add_argument('--disable-images')
        options.add_argument('--disable-javascript')
        options.add_argument('--disable-web-security')
        options.add_argument('--allow-running-insecure-content')
        options.add_argument('--no-first-run')
        options.add_argument('--no-default-browser-check')
        options.add_argument('--disable-default-apps')
        options.add_argument('--disable-popup-blocking')
        options.add_argument('--disable-translate')
        options.add_argument('--disable-background-timer-throttling')
        options.add_argument('--disable-renderer-backgrounding')
        options.add_argument('--disable-device-discovery-notifications')
        
        # User agent
        options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')
        
        # Window size and position
        options.add_argument('--window-size=1920,1080')
        options.add_argument('--start-maximized')
        
        # Debugging
        options.add_argument('--remote-debugging-port=9222')
        
        # Additional preferences
        prefs = {
            "profile.default_content_setting_values": {
                "images": 2,
                "plugins": 2,
                "popups": 2,
                "geolocation": 2,
                "notifications": 2,
                "media_stream": 2,
            }
        }
        options.add_experimental_option("prefs", prefs)
        
        # Create driver
        driver = webdriver.Chrome(options=options)
        driver.set_page_load_timeout(60)
        
        return driver
        
    except Exception as e:
        print(f"Error creating Chrome driver: {e}")
        print("Make sure Chrome and chromedriver are installed and updated.")
        return None


def human_like_navigation(driver, url, description=""):
    """
    Navigate to a URL with human-like behavior patterns.
    
    Args:
        driver: Selenium WebDriver instance
        url (str): URL to navigate to
        description (str): Human-readable description for logging
    """
    try:
        # Random delay before navigation
        time.sleep(random.uniform(1.5, 3.5))
        
        print(f"    🌐 Navigating to: {description}")
        driver.get(url)
        
        # Random reading time
        reading_time = random.uniform(2.0, 5.0)
        print(f"    👀 Reading page for {reading_time:.1f} seconds...")
        time.sleep(reading_time)
        
    except Exception as e:
        print(f"    ❌ Navigation error: {e}")
        raise


def extract_dropdown_data(page_source):
    """
    Extract school IDs, modality IDs, and program IDs from dropdown menus.
    Preserves order and allows duplicate names for schools.
    
    Args:
        page_source (str): HTML source of the page
        
    Returns:
        dict: Contains schools_list (ordered), schools_lookup (legacy), modalities_lookup, programs_lookup
    """
    soup = BeautifulSoup(page_source, 'html.parser')
    
    # Extract school IDs and names from "Buscar Centros Educativos" - PRESERVE ORDER
    schools_list = []  # New: ordered list that preserves duplicates
    schools_lookup = {}  # Legacy: for backward compatibility
    school_select = soup.find('select', {'name': 'ctl00$ContentPlaceHolder1$ddlCentroEducativo'})
    if not school_select:
        school_select = soup.find('select', id=lambda x: x and 'ddlCentroEducativo' in x)
    
    if school_select:
        for option in school_select.find_all('option'):
            value = option.get('value')
            text = option.text.strip()
            # Filter out placeholder and empty options
            if (value and value != '' and text and 
                text != 'SELECCIONE' and 
                text != '-- Escriba nombre del centro --' and
                value != '-- Escriba nombre del centro --'):
                
                school_entry = {
                    'school_id': value,
                    'school_name': html.unescape(text)
                }
                
                # Add to ordered list (preserves duplicates and order)
                schools_list.append((text, school_entry))
                
                # Also add to lookup dict for legacy compatibility (will overwrite duplicates)
                schools_lookup[text] = school_entry
    
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
        'schools_list': schools_list,      # New: ordered list with duplicates preserved
        'schools_lookup': schools_lookup,  # Legacy: dict for backward compatibility
        'modalities_lookup': modalities_lookup,
        'programs_lookup': programs_lookup
    }


def extract_html_counter(page_source):
    """
    Extract the HTML counter (ContentPlaceHolder_H1Contador) from the page.
    
    Args:
        page_source (str): HTML source of the page
        
    Returns:
        dict: Contains counter information
    """
    counter_patterns = [
        r'ContentPlaceHolder_H1Contador[^>]*>([^<]+)',
        r'ContentPlaceHolder.*?H1.*?Contador[^>]*>([^<]+)', 
        r'H1Contador[^>]*>([^<]+)',
        r'id=["\'].*?contador.*?["\'][^>]*>([^<]+)',
        r'class=["\'].*?contador.*?["\'][^>]*>([^<]+)'
    ]
    
    counter_info = {
        'counter_found': False,
        'counter_text': None,
        'counter_number': None
    }
    
    for pattern in counter_patterns:
        matches = re.findall(pattern, page_source, re.IGNORECASE | re.DOTALL)
        if matches:
            counter_text = matches[0].strip()
            counter_info['counter_found'] = True
            counter_info['counter_text'] = counter_text
            
            # Try to extract number from counter text
            number_matches = re.findall(r'\d+', counter_text)
            if number_matches:
                counter_info['counter_number'] = int(number_matches[-1])  # Take the last number found
            
            break
    
    return counter_info


def get_school_data_from_page_source(page_source):
    """
    Extract comprehensive school data from page source including enhanced metadata.
    Uses map marker data as primary source, supplements with dropdown for IDs.
    
    Args:
        page_source (str): HTML source of the page
        
    Returns:
        tuple: (enhanced_schools_list, extraction_stats_dict)
    """
    # Extract HTML counter first
    counter_info = extract_html_counter(page_source)
    
    # Extract dropdown data for ID matching
    dropdown_data = extract_dropdown_data(page_source)
    
    # Extract map marker data from CDATA sections - this is the authoritative source
    map_schools = []
    
    # First try the L.marker pattern for coordinates and details
    marker_pattern = r'L\.marker\(\[([^,]+),\s*([^,]+)\].*?\.bindPopup\(\'([^\']*)\'\);'
    coordinate_data = {}
    
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
        modalities_text = ','.join(modalities) if modalities else "MISSING"
        
        # Store coordinate and detail data by school name
        coordinate_data[name] = {
            "Latitud": lat,
            "Longitud": lon,
            "Direccion": address,
            "modality_labels": modalities_text  # Store modalities too!
        }
    
    # Now extract ALL schools from CDATA sections - use multiple strategies
    target_cdata_pattern = r'//<!\[CDATA\[\s*var osmUrl\s*=(.*?)//\]\]>'
    target_cdata_match = re.search(target_cdata_pattern, page_source, re.DOTALL)
    
    all_school_names = []  # Use list to preserve order for proper ID matching
    
    # Strategy 1: Primary target CDATA section
    if target_cdata_match:
        cdata_content = target_cdata_match.group(1)
        print(f"    🔍 Found target CDATA section with 'var osmUrl =' (length: {len(cdata_content)})")
        
        # Extract all Nombre: entries from this specific CDATA section using multiple patterns
        # Pattern 1: Standard <b>Nombre:</b> format
        nombre_pattern_1 = r'<b>Nombre:</b>\s*([^<]+)'
        nombres_1 = re.findall(nombre_pattern_1, cdata_content, re.IGNORECASE)
        
        # Pattern 2: Alternative Nombre: format (without <b> tags)
        nombre_pattern_2 = r'Nombre:\s*([^\n\r,<]+)'
        nombres_2 = re.findall(nombre_pattern_2, cdata_content, re.IGNORECASE)
        
        # Keep all schools in order - don't deduplicate by name since same-named schools
        # are different institutions in different locations with different IDs
        all_nombres_ordered = []
        
        # Process Pattern 1 results in order
        for nombre in nombres_1:
            school_name = html.unescape(nombre.strip())
            if school_name and school_name != "N/A" and len(school_name) > 2:
                all_nombres_ordered.append(school_name)
        
        # Process Pattern 2 results in order (if any)
        for nombre in nombres_2:
            school_name = html.unescape(nombre.strip())
            # Clean up any trailing HTML or unwanted characters
            school_name = re.sub(r'\s*</.*$', '', school_name)  # Remove trailing HTML tags
            school_name = re.sub(r'\s*\|.*$', '', school_name)  # Remove trailing pipe separators
            school_name = school_name.strip()
            
            if school_name and school_name != "N/A" and len(school_name) > 2:
                all_nombres_ordered.append(school_name)
        
        # Add all schools to the main list, preserving order
        for nombre in all_nombres_ordered:
            all_school_names.append(nombre)  # Use list instead of set to preserve order
        
        # Check for same-named schools (these are actually different schools)
        name_counts = {}
        for name in all_nombres_ordered:
            name_counts[name] = name_counts.get(name, 0) + 1
        
        same_named_schools = {name: count for name, count in name_counts.items() if count > 1}
        
        total_raw_matches = len(nombres_1) + len(nombres_2)
        print(f"    🔍 Strategy 1 - Target CDATA: {len(all_nombres_ordered)} schools (ALL kept in order)")
        print(f"        • Pattern 1 (<b>Nombre:</b>): {len(nombres_1)} matches")
        print(f"        • Pattern 2 (Nombre:): {len(nombres_2)} matches")
        if same_named_schools:
            print(f"        • Same-named schools (different locations): {len(same_named_schools)} names")
            for name, count in same_named_schools.items():
                print(f"          - '{name}': {count} schools")
    
    # Strategy 2: Only use other CDATA sections if primary target failed
    if len(all_school_names) == 0:
        print(f"    🔍 Strategy 2 - Fallback to other CDATA sections")
        cdata_pattern = r'//<!\[CDATA\[(.*?)//\]\]>'
        cdata_matches = re.findall(cdata_pattern, page_source, re.DOTALL)
        
        for i, cdata_content in enumerate(cdata_matches):
            # Use both patterns for comprehensive extraction
            nombre_pattern_1 = r'<b>Nombre:</b>\s*([^<]+)'
            nombre_pattern_2 = r'Nombre:\s*([^\n\r,<]+)'
            
            nombres_1 = re.findall(nombre_pattern_1, cdata_content, re.IGNORECASE)
            nombres_2 = re.findall(nombre_pattern_2, cdata_content, re.IGNORECASE)
            
            for nombre in nombres_1:
                school_name = html.unescape(nombre.strip())
                if school_name and school_name != "N/A" and len(school_name) > 2:
                    all_school_names.append(school_name)
            
            for nombre in nombres_2:
                school_name = html.unescape(nombre.strip())
                # Clean up any trailing HTML or unwanted characters
                school_name = re.sub(r'\s*</.*$', '', school_name)
                school_name = re.sub(r'\s*\|.*$', '', school_name)
                school_name = school_name.strip()
                
                if school_name and school_name != "N/A" and len(school_name) > 2:
                    all_school_names.append(school_name)
            
            if len(all_school_names) > 0:
                print(f"    🔍 Strategy 2 - CDATA {i+1}: Found {len(all_school_names)} schools")
                break
    
    # Strategy 3: Fallback to L.marker data if no CDATA worked
    if len(all_school_names) == 0:
        print(f"    🔍 Strategy 3 - Fallback to L.marker data")
        for name in coordinate_data.keys():
            all_school_names.append(name)
        print(f"    🔍 Strategy 3 - L.marker data: Found {len(all_school_names)} schools")
    
    # Strategy 4: Final fallback to dropdown data
    if len(all_school_names) == 0:
        print(f"    🔍 Strategy 4 - Final fallback to dropdown data")
        for name in dropdown_data['schools_lookup'].keys():
            all_school_names.append(name)
        print(f"    🔍 Strategy 4 - Dropdown data: Found {len(all_school_names)} schools")
    
    print(f"    🎯 FINAL EXTRACTION: {len(all_school_names)} schools found (order preserved)")
    
    # Create complete school list using ORDER-BASED matching
    # Schools appear in the same order in CDATA and dropdown
    schools_data = []
    matched_coords = 0
    missing_coords = 0
    
    # Get dropdown schools in order (as list) - use new schools_list that preserves duplicates
    dropdown_schools_ordered = dropdown_data['schools_list']
    
    print(f"    🔄 Matching schools by ORDER: CDATA({len(all_school_names)}) vs Dropdown({len(dropdown_schools_ordered)})")
    
    for i, school_name in enumerate(all_school_names):
        # Start with basic school info
        school = {"Nombre": school_name}
        
        # Match by ORDER/POSITION instead of name
        school_id = None
        if i < len(dropdown_schools_ordered):
            dropdown_name, dropdown_info = dropdown_schools_ordered[i]
            school_id = dropdown_info['school_id']
            
            # Debug: show matching for same-named schools
            if school_name != dropdown_name:
                print(f"    🔍 Order #{i+1}: CDATA='{school_name}' -> Dropdown='{dropdown_name}' (ID: {school_id})")
        
        school['school_id'] = school_id
        
        # Try to get coordinates and details
        if school_name in coordinate_data:
            school.update(coordinate_data[school_name])
            matched_coords += 1
        else:
            # Try partial matching for coordinates
            coord_match = None
            for coord_name, coord_data in coordinate_data.items():
                if (school_name.upper().strip() in coord_name.upper().strip() or 
                    coord_name.upper().strip() in school_name.upper().strip()):
                    coord_match = coord_data
                    matched_coords += 1
                    break
            
            if coord_match:
                school.update(coord_match)
            else:
                # No coordinate data found
                school.update({
                    "Latitud": "MISSING",
                    "Longitud": "MISSING", 
                    "Direccion": "MISSING",
                    "modality_labels": "MISSING"  # Ensure modality_labels is always present
                })
                missing_coords += 1
        
        schools_data.append(school)
    
    # Enhanced reporting
    extraction_stats = {
        'total_dropdown_schools': len(dropdown_data['schools_list']),  # Use schools_list for accurate count
        'total_map_markers': len(coordinate_data),
        'total_cdata_schools': len(all_school_names),
        'schools_with_coords': matched_coords,
        'schools_missing_coords': missing_coords,
        'modalities_lookup': dropdown_data['modalities_lookup'],
        'programs_lookup': dropdown_data['programs_lookup'],
        'html_counter_found': counter_info['counter_found'],
        'html_counter_text': counter_info['counter_text'],
        'html_counter_number': counter_info['counter_number']
    }
    
    # Enhance schools with modality and program matching
    enhanced_schools = []
    for school in schools_data:
        enhanced_school = school.copy()
        
        # School ID should already be set, but double-check
        school_name = school.get('Nombre', '').strip()
        if not enhanced_school.get('school_id'):
            enhanced_school['school_id'] = dropdown_data['schools_lookup'].get(school_name, {}).get('school_id')
        
        # Try to match modalities to get modality IDs
        modality_labels = school.get('modality_labels', '')
        matched_modality_ids = []
        matched_modality_names = []
        matched_program_ids = []
        matched_program_names = []
        if modality_labels and modality_labels != "MISSING":
            modalities_list = [m.strip() for m in modality_labels.split(',')]
            
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
    
    return enhanced_schools, extraction_stats


def scrape_municipality(department_name, municipality_name, municipality_id, max_retries=5):
    """
    Scrape all schools from a specific municipality with enhanced metadata.
    
    Args:
        department_name (str): Name of the department
        municipality_name (str): Name of the municipality  
        municipality_id (int): Municipality ID
        max_retries (int): Maximum number of retry attempts
        
    Returns:
        list: List of school dictionaries with enhanced data
    """
    dept_id = DEPARTMENTS[department_name]['id']
    
    for attempt in range(max_retries):
        driver = create_stealth_driver()
        if not driver:
            print(f"    ❌ Failed to create driver (attempt {attempt + 1}/{max_retries})")
            continue
        
        try:
            print(f"    🔧 FIXED scraping approach for: {municipality_name}")
            
            # Navigate to the education map
            human_like_navigation(driver, "https://serviciosenlinea.mined.gob.ni/", "main website")
            human_like_navigation(driver, "https://serviciosenlinea.mined.gob.ni/mapa-de-la-educacion/", "education map")
            
            # Navigate to department
            department_url = f"https://serviciosenlinea.mined.gob.ni/mapa-de-la-educacion/Departamento.aspx?Departamento={dept_id}"
            human_like_navigation(driver, department_url, f"department {department_name}")
            
            # Navigate to municipality
            municipality_url = f"https://serviciosenlinea.mined.gob.ni/mapa-de-la-educacion/Georreferencia.aspx?Municipio={municipality_id}"
            human_like_navigation(driver, municipality_url, f"municipality {municipality_name}")
            
            # Wait for map data to load
            print("    🗺️  Waiting for map data to load...")
            WebDriverWait(driver, 45).until(lambda d: "L.marker" in d.page_source)
            
            time.sleep(3)  # Extra time for all content to load
            print("    ✅ Map data loaded successfully!")
            
            # Extract all data
            schools_data, extraction_stats = get_school_data_from_page_source(driver.page_source)
            
            if schools_data:
                print(f"    📋 COMPLETE DATA EXTRACTION:")
                print(f"        • Schools from CDATA/map: {extraction_stats['total_cdata_schools']} (primary source)")
                print(f"        • Schools in dropdown: {extraction_stats['total_dropdown_schools']} (for ID matching)")
                print(f"        • Map markers with coords: {extraction_stats['total_map_markers']}")
                print(f"        • Schools with coordinates: {extraction_stats['schools_with_coords']}")
                print(f"        • Schools missing coordinates: {extraction_stats['schools_missing_coords']}")
                print(f"        • Modalities available: {len(extraction_stats['modalities_lookup'])}")
                print(f"        • Programs available: {len(extraction_stats['programs_lookup'])}")
                
                # Display HTML counter information
                if extraction_stats['html_counter_found']:
                    counter_num = extraction_stats['html_counter_number']
                    counter_text = extraction_stats['html_counter_text']
                    print(f"        • HTML Counter: {counter_num} schools ('{counter_text}')")
                    
                    # Compare with our extraction
                    our_count = len(schools_data)
                    if counter_num == our_count:
                        print(f"        ✅ Perfect match: HTML counter = extracted schools = {our_count}!")
                    else:
                        diff = abs(counter_num - our_count)
                        print(f"        ⚠️  Count difference: HTML shows {counter_num}, we extracted {our_count} (diff: {diff})")
                else:
                    print(f"        ⚠️  HTML Counter: Not found")
                
                print(f"    🎉 TOTAL SCHOOLS: {len(schools_data)} from {municipality_name}!")
                
                # Add department and municipality info
                for school in schools_data:
                    school['department'] = department_name
                    school['municipality'] = municipality_name
                    school['dep_id'] = dept_id
                    school['mun_id'] = municipality_id
                
                return schools_data
            else:
                print(f"    ⚠️  No schools found in CDATA/map data (attempt {attempt + 1}/{max_retries})")
                # Log page details for debugging
                page_length = len(driver.page_source) if driver.page_source else 0
                has_marker = "L.marker" in driver.page_source if driver.page_source else False
                print(f"    🔍 Page source length: {page_length}, Contains markers: {has_marker}")
                print(f"    🔍 Dropdown schools found: {extraction_stats.get('total_dropdown_schools', 0)}")
                
        except TimeoutException as e:
            print(f"    ⏰ Timeout waiting for page to load (attempt {attempt + 1}/{max_retries})")
            print(f"    🔍 Timeout details: {str(e)[:100]}...")
        except Exception as e:
            print(f"    ❌ Unexpected error (attempt {attempt + 1}/{max_retries}): {type(e).__name__}: {str(e)[:100]}...")
        finally:
            if driver:
                driver.quit()
        
        if attempt < max_retries - 1:
            wait_time = random.uniform(15, 25)  # Increased wait time
            print(f"    ⏳ Waiting {wait_time:.1f} seconds before retry...")
            time.sleep(wait_time)
    
    # Enhanced failure reporting
    print(f"    💥 FAILED: {municipality_name} after {max_retries} attempts")
    print(f"    🔍 Municipality ID: {municipality_id}, Department ID: {dept_id}")
    print(f"    📋 Possible reasons:")
    print(f"        - Network connectivity issues")
    print(f"        - Website temporarily unavailable")
    print(f"        - No schools registered in this municipality")
    print(f"        - Municipality data not yet available online")
    print(f"        - Browser/driver compatibility issues")
    return None


def scrape_department(department_name, output_dir="data/raw"):
    """
    Scrape all municipalities in a department.
    
    Args:
        department_name (str): Name of the department to scrape
        output_dir (str): Directory to save output files
        
    Returns:
        bool: True if successful, False otherwise
    """
    if department_name not in DEPARTMENTS:
        print(f"❌ Unknown department: {department_name}")
        print(f"Available departments: {', '.join(DEPARTMENTS.keys())}")
        return False
    
    print(f"\n🏛️  SCRAPING DEPARTMENT: {department_name.upper()}")
    print("=" * 60)
    
    department_data = DEPARTMENTS[department_name]
    municipalities = department_data['municipalities']
    all_schools = []
    failed_municipalities = []  # Track failed municipalities
    
    total_municipalities = len(municipalities)
    
    for i, (municipality_name, municipality_id) in enumerate(municipalities.items(), 1):
        print(f"\n📍 Municipality {i}/{total_municipalities}: {municipality_name}")
        print("-" * 40)
        
        schools = scrape_municipality(department_name, municipality_name, municipality_id, max_retries=5)
        
        if schools:
            all_schools.extend(schools)
            print(f"    ✅ Successfully scraped {len(schools)} schools from {municipality_name}")
        else:
            failed_municipalities.append(municipality_name)
            print(f"    ❌ Failed to scrape {municipality_name}")
        
        # Progress update
        print(f"    📊 Total schools collected so far: {len(all_schools)}")
        
        # Save partial results periodically
        if len(all_schools) > 0 and i % 3 == 0:
            partial_file = os.path.join(output_dir, f"partial_{department_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv")
            df_partial = pd.DataFrame(all_schools)
            df_partial.to_csv(partial_file, index=False, encoding='utf-8')
            print(f"    💾 Saved partial results to: {partial_file}")
    
    # Save final results
    if all_schools:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        final_file = os.path.join(output_dir, f"nicaragua_schools_{department_name}_{timestamp}.csv")
        
        df_final = pd.DataFrame(all_schools)
        df_final.to_csv(final_file, index=False, encoding='utf-8')
        
        print(f"\n🎉 DEPARTMENT {department_name.upper()} COMPLETED!")
        print(f"📊 Total schools scraped: {len(all_schools)}")
        print(f"💾 Final results saved to: {final_file}")
        
        # Show failed municipalities summary if any
        if failed_municipalities:
            print(f"\n⚠️  Failed municipalities in {department_name} ({len(failed_municipalities)}):")
            for failed_mun in failed_municipalities:
                print(f"    - {failed_mun}")
        
        return True
    else:
        print(f"\n❌ No schools collected from {department_name}")
        if failed_municipalities:
            print(f"⚠️  All municipalities failed: {', '.join(failed_municipalities)}")
        return False


def scrape_all_departments(output_dir="data/raw"):
    """
    Scrape all departments in Nicaragua and save to a single combined file.
    
    Args:
        output_dir (str): Directory to save output files
        
    Returns:
        bool: True if at least one department was successful
    """
    print("\n🇳🇮 STARTING COMPLETE NICARAGUA SCHOOLS SCRAPING")
    print("=" * 70)
    
    os.makedirs(output_dir, exist_ok=True)
    
    all_schools_complete = []
    successful_departments = []
    failed_departments = []
    failed_municipalities = []  # Track failed municipalities
    
    total_departments = len(DEPARTMENTS)
    
    for i, department_name in enumerate(DEPARTMENTS.keys(), 1):
        print(f"\n🏛️  DEPARTMENT {i}/{total_departments}: {department_name.upper()}")
        print("=" * 70)
        
        # Scrape individual department
        department_data = DEPARTMENTS[department_name]
        municipalities = department_data['municipalities']
        department_schools = []
        
        total_municipalities = len(municipalities)
        
        for j, (municipality_name, municipality_id) in enumerate(municipalities.items(), 1):
            print(f"\n📍 Municipality {j}/{total_municipalities}: {municipality_name}")
            print("-" * 40)
            
            schools = scrape_municipality(department_name, municipality_name, municipality_id, max_retries=5)
            
            if schools:
                department_schools.extend(schools)
                all_schools_complete.extend(schools)
                print(f"    ✅ Successfully scraped {len(schools)} schools from {municipality_name}")
            else:
                failed_municipalities.append(f"{department_name} - {municipality_name}")
                print(f"    ❌ Failed to scrape {municipality_name}")
            
            # Progress update
            print(f"    📊 Total schools collected so far: {len(all_schools_complete)}")
        
        if department_schools:
            successful_departments.append(department_name)
            print(f"    ✅ {department_name} completed successfully ({len(department_schools)} schools)")
        else:
            failed_departments.append(department_name)
            print(f"    ❌ {department_name} failed")
        
        # Save progress after each department
        if all_schools_complete:
            timestamp = datetime.now().strftime("%y%m%d")
            progress_file = os.path.join(output_dir, f"nicaraguan_schools_{timestamp}_progress.csv")
            df_progress = pd.DataFrame(all_schools_complete)
            df_progress.to_csv(progress_file, index=False, encoding='utf-8')
            print(f"    💾 Progress saved: {len(all_schools_complete)} schools in {progress_file}")
        
        # Brief pause between departments
        if i < total_departments:
            print(f"\n⏳ Pausing briefly before next department...")
            time.sleep(random.uniform(30, 60))
    
    # Save final complete file
    if all_schools_complete:
        timestamp = datetime.now().strftime("%y%m%d")
        final_file = os.path.join(output_dir, f"nicaraguan_schools_{timestamp}.csv")
        
        df_final = pd.DataFrame(all_schools_complete)
        df_final.to_csv(final_file, index=False, encoding='utf-8')
        
        print(f"\n🎉 COMPLETE SCRAPING FINISHED!")
        print(f"📊 Total schools collected: {len(all_schools_complete)}")
        print(f"💾 Final file saved: {final_file}")
    
    # Final summary
    print(f"\n🎯 SCRAPING SUMMARY")
    print("=" * 50)
    print(f"✅ Successful departments ({len(successful_departments)}): {', '.join(successful_departments)}")
    if failed_departments:
        print(f"❌ Failed departments ({len(failed_departments)}): {', '.join(failed_departments)}")
    if failed_municipalities:
        print(f"\n⚠️  Failed municipalities ({len(failed_municipalities)}):")
        for failed_mun in failed_municipalities:
            print(f"    - {failed_mun}")
        print(f"\n📋 Possible reasons for municipality failures:")
        print(f"    • Network connectivity issues during scraping")
        print(f"    • Website temporarily unavailable or overloaded")
        print(f"    • No schools currently registered in these municipalities")
        print(f"    • Municipality data not yet available in the online system")
        print(f"    • Browser/driver compatibility issues")
        print(f"    • Rate limiting or anti-bot measures")
    
    return len(successful_departments) > 0


def main():
    """Main function with command line interface."""
    parser = argparse.ArgumentParser(
        description="Nicaragua Schools Scraper - Complete Edition",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main_scraper.py                    # Interactive mode
  python main_scraper.py --all              # Scrape all departments  
  python main_scraper.py --dept Managua     # Scrape specific department
  python main_scraper.py --dept Boaco --output custom_folder
        """
    )
    
    parser.add_argument('--all', action='store_true', 
                       help='Scrape all departments in Nicaragua')
    parser.add_argument('--dept', type=str, 
                       help='Scrape specific department')
    parser.add_argument('--output', type=str, default='data/raw',
                       help='Output directory (default: data/raw)')
    
    args = parser.parse_args()
    
    # Create output directory
    os.makedirs(args.output, exist_ok=True)
    
    print("🇳🇮 Nicaragua Schools Scraper - Complete Edition")
    print("Author: Rony Rodriguez")
    print("=" * 60)
    
    if args.all:
        print("🚀 Starting complete scraping of all departments...")
        success = scrape_all_departments(args.output)
        if success:
            print("\n🎉 Scraping completed! Check the output directory for results.")
        else:
            print("\n❌ Scraping failed. Check the logs for details.")
            
    elif args.dept:
        if args.dept not in DEPARTMENTS:
            print(f"❌ Unknown department: {args.dept}")
            print(f"Available departments: {', '.join(DEPARTMENTS.keys())}")
            return
        
        print(f"🚀 Starting scraping of {args.dept} department...")
        success = scrape_department(args.dept, args.output)
        if success:
            print(f"\n🎉 {args.dept} scraping completed!")
        else:
            print(f"\n❌ {args.dept} scraping failed.")
            
    else:
        # Interactive mode
        print("\n🤖 Interactive Mode")
        print("Choose an option:")
        print("1. Scrape all departments")
        print("2. Scrape specific department")
        print("3. Exit")
        
        choice = input("\nEnter your choice (1-3): ").strip()
        
        if choice == '1':
            confirm = input("This will scrape ALL departments. Continue? (y/N): ").strip().lower()
            if confirm == 'y':
                success = scrape_all_departments(args.output)
                if success:
                    print("\n🎉 Complete scraping finished!")
                else:
                    print("\n❌ Scraping failed.")
            else:
                print("Cancelled.")
                
        elif choice == '2':
            print(f"\nAvailable departments:")
            for i, dept in enumerate(DEPARTMENTS.keys(), 1):
                print(f"{i:2d}. {dept}")
            
            try:
                dept_choice = int(input(f"\nEnter department number (1-{len(DEPARTMENTS)}): "))
                dept_names = list(DEPARTMENTS.keys())
                if 1 <= dept_choice <= len(dept_names):
                    selected_dept = dept_names[dept_choice - 1]
                    print(f"\n🚀 Starting scraping of {selected_dept}...")
                    success = scrape_department(selected_dept, args.output)
                    if success:
                        print(f"\n🎉 {selected_dept} scraping completed!")
                    else:
                        print(f"\n❌ {selected_dept} scraping failed.")
                else:
                    print("Invalid department number.")
            except ValueError:
                print("Invalid input. Please enter a number.")
                
        elif choice == '3':
            print("Goodbye! 👋")
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()
