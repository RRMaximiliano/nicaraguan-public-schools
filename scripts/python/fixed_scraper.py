#!/usr/bin/env python3
"""
Fixed Nicaragua schools scraper with correct regex patterns.
"""

import pandas as pd
import re
import html
import time
import random
import os
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains

# Test with the full first department (all municipalities in Boaco)
FIXED_TEST = {
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
}

def get_stealth_chrome_options():
    """Enhanced stealth Chrome options to avoid detection."""
    options = webdriver.ChromeOptions()
    
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    
    # Human-like user agent
    options.add_argument("--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    options.add_argument("--disable-web-security")
    options.add_argument("--allow-running-insecure-content")
    options.add_argument("--disable-features=VizDisplayCompositor")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-plugins")
    options.add_argument("--disable-default-apps")
    options.add_argument("--disable-sync")
    
    return options


def create_stealth_driver():
    """Create a stealth driver with enhanced anti-detection measures."""
    options = get_stealth_chrome_options()
    
    try:
        import chromedriver_autoinstaller
        chromedriver_autoinstaller.install()
    except ImportError:
        print("chromedriver-autoinstaller not found. Make sure ChromeDriver is in PATH.")
    
    driver = webdriver.Chrome(options=options)
    
    # Execute stealth scripts
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    driver.execute_script("Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3, 4, 5]})")
    driver.execute_script("Object.defineProperty(navigator, 'languages', {get: () => ['en-US', 'en']})")
    
    return driver


def human_like_navigation(driver, url, description=""):
    """Navigate to a URL with human-like behavior."""
    print(f"    🌐 Navigating to: {description}")
    driver.get(url)
    
    delay = random.uniform(2, 5)
    print(f"    👀 Reading page for {delay:.1f} seconds...")
    time.sleep(delay)
    
    try:
        actions = ActionChains(driver)
        actions.move_by_offset(random.randint(100, 300), random.randint(100, 300))
        actions.perform()
    except:
        pass


def get_school_data_from_page_source(page_source):
    """
    Extract school data from the page source using FIXED regex patterns.
    """
    # Fixed pattern to match the actual format in the page
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
        
        # Store the school data with department and municipality IDs
        schools_data.append({
            "Nombre": name,
            "Latitud": lat,
            "Longitud": lon,
            "Direccion": address,
            "Modalidades": ", ".join(modalities)
        })
    
    return schools_data


def fixed_municipality_scraper(department_name, municipality_name, municipality_id):
    """Fixed scraper with correct regex patterns."""
    driver = None
    try:
        print(f"🔧 FIXED scraping approach for: {municipality_name}")
        
        driver = create_stealth_driver()
        
        # Navigation steps
        human_like_navigation(driver, "https://serviciosenlinea.mined.gob.ni/", "main website")
        human_like_navigation(driver, "https://serviciosenlinea.mined.gob.ni/mapa-de-la-educacion/", "education map")
        
        dept_id = FIXED_TEST[department_name]['id']
        department_url = f"https://serviciosenlinea.mined.gob.ni/mapa-de-la-educacion/Departamento.aspx?Departamento={dept_id}"
        human_like_navigation(driver, department_url, f"department {department_name}")
        
        time.sleep(random.uniform(5, 10))
        
        municipality_url = f"https://serviciosenlinea.mined.gob.ni/mapa-de-la-educacion/Georreferencia.aspx?Municipio={municipality_id}"
        human_like_navigation(driver, municipality_url, f"municipality {municipality_name}")
        
        print(f"    🗺️  Waiting for map data to load...")
        try:
            WebDriverWait(driver, 45).until(lambda d: "L.marker" in d.page_source)
            print("    ✅ Map data loaded successfully!")
            
            page_source = driver.page_source
            schools = get_school_data_from_page_source(page_source)
            
            if schools:
                print(f"    🎉 Found {len(schools)} schools!")
                for school in schools:
                    school["department"] = department_name
                    school["municipality"] = municipality_name
                    school["dep_id"] = dept_id
                    school["mun_id"] = municipality_id
                return schools, "SUCCESS"
            else:
                return [], "No schools found"
                
        except TimeoutException:
            print(f"    ⏰ Timeout waiting for map data")
            return None, "Timeout"
            
    except Exception as e:
        print(f"    ❌ Error: {e}")
        return None, f"Error: {e}"
    finally:
        if driver:
            try:
                driver.quit()
            except:
                pass


def main():
    """Test the fixed approach with all municipalities in the first department."""
    print("🔧 FIXED NICARAGUA SCHOOLS SCRAPER")
    print("Testing first department (Boaco) with all municipalities")
    print("=" * 60)
    
    start_time = time.time()
    all_schools = []
    
    for department_name, department_data in FIXED_TEST.items():
        print(f"\n📍 Processing Department: {department_name}")
        print(f"   Department ID: {department_data['id']}")
        print(f"   Municipalities: {len(department_data['municipalities'])}")
        print("-" * 40)
        
        for municipality_name, municipality_id in department_data["municipalities"].items():
            print(f"\n🏘️  Testing: {municipality_name}, {department_name}")
            
            schools, status = fixed_municipality_scraper(
                department_name, municipality_name, municipality_id
            )
            
            print(f"📊 RESULT: {status}")
            if schools:
                print(f"📚 Schools found: {len(schools)}")
                if len(schools) > 0:
                    print(f"📝 First school: {schools[0]['Nombre']}")
                    all_schools.extend(schools)
                    print(f"📈 Total schools so far: {len(all_schools)}")
            
            # Add delay between municipalities
            delay = random.uniform(15, 25)
            print(f"⏱️  Waiting {delay:.1f} seconds before next municipality...")
            time.sleep(delay)
    
    # Save all results
    if all_schools:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"data/boaco_department_{timestamp}.csv"
        
        os.makedirs("data", exist_ok=True)
        
        df = pd.DataFrame(all_schools)
        df.to_csv(filename, index=False, encoding="utf-8")
        print(f"\n💾 Saved {len(all_schools)} schools to: {filename}")
    
    elapsed_time = time.time() - start_time
    print(f"\n⏱️  Total time: {elapsed_time/60:.1f} minutes")
    print(f"🎉 First department test completed with {len(all_schools)} schools!")


if __name__ == "__main__":
    print("🚀 Starting fixed scraper...")
    try:
        main()
    except Exception as e:
        print(f"❌ Error in main: {e}")
        import traceback
        traceback.print_exc()
