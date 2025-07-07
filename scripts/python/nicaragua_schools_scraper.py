# Import necessary libraries
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

# This dictionary contains all the departments and their municipalities with their corresponding IDs.
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

# # Function to get Chrome options with anti-detection measures
def get_chrome_options():
    """
    Configure Chrome options with additional anti-detection measures.
    """
    options = webdriver.ChromeOptions()
    
    # Basic options
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    
    # Add random user agent to avoid detection
    user_agents = [
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    ]
    
    options.add_argument(f"--user-agent={random.choice(user_agents)}")
    
    # Additional stealth options
    options.add_argument("--disable-features=VizDisplayCompositor")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-plugins")
    options.add_argument("--disable-images")  # Faster loading
    
    # Caching prevention
    options.add_argument("--disable-cache")
    options.add_argument("--disable-application-cache")
    options.add_argument("--disable-offline-load-stale-cache")
    options.add_argument("--disk-cache-size=0")
    options.add_argument("--disable-background-networking")
    options.add_argument("--disable-default-apps")
    options.add_argument("--disable-sync")
    options.add_argument("--disable-translate")
    options.add_argument("--hide-scrollbars")
    options.add_argument("--metrics-recording-only")
    options.add_argument("--mute-audio")
    options.add_argument("--no-default-browser-check")
    options.add_argument("--no-first-run")
    options.add_argument("--safebrowsing-disable-auto-update")
    options.add_argument("--start-maximized")
    options.add_argument("--disable-background-timer-throttling")
    options.add_argument("--disable-renderer-backgrounding")
    options.add_argument("--disable-backgrounding-occluded-windows")
    
    return options


def create_stealth_driver():
    """
    Create a Chrome driver with stealth configuration and anti-detection measures.
    """
    options = get_chrome_options()
    
    try:
        # Install chromedriver if needed
        try:
            import chromedriver_autoinstaller
            chromedriver_autoinstaller.install()
        except ImportError:
            print("chromedriver-autoinstaller not found. Make sure ChromeDriver is in PATH.")
        
        driver = webdriver.Chrome(options=options)
        
        # Execute stealth script to hide automation
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        return driver
        
    except Exception as e:
        print(f"Failed to create Chrome driver: {e}")
        return None


def adaptive_delay(attempt_number, base_delay=5):
    """
    Implement adaptive delay with exponential backoff and jitter.
    """
    delay = base_delay * (2 ** min(attempt_number, 3))  # Cap at 8x base delay
    jitter = random.uniform(0.5, 1.5)  # Add randomness
    final_delay = delay * jitter
    
    print(f"    Waiting {final_delay:.1f} seconds (attempt {attempt_number + 1})...")
    time.sleep(final_delay)


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
        
        # Store the school data
        schools_data.append({
            "Nombre": name,
            "Latitud": lat,
            "Longitud": lon,
            "Direccion": address,
            "Modalidades": ", ".join(modalities)
        })
    
    return schools_data


def human_like_navigation(driver, url, description=""):
    """Navigate to a URL with human-like behavior."""
    print(f"    🌐 Navigating to: {description}")
    driver.get(url)
    
    delay = random.uniform(2, 5)
    print(f"    👀 Reading page for {delay:.1f} seconds...")
    time.sleep(delay)
    
    try:
        from selenium.webdriver.common.action_chains import ActionChains
        actions = ActionChains(driver)
        actions.move_by_offset(random.randint(100, 300), random.randint(100, 300))
        actions.perform()
    except:
        pass


def scrape_municipality_with_retry(department_name, municipality_name, municipality_id, max_retries=3):
    """
    Scrape a single municipality using the PROVEN WORKING approach.
    """
    for attempt in range(max_retries):
        driver = None
        try:
            print(f"    🔧 FIXED scraping approach for: {municipality_name}")
            
            # Create fresh driver for each attempt
            driver = create_stealth_driver()
            if not driver:
                continue
            
            # Use the proven working navigation sequence
            human_like_navigation(driver, "https://serviciosenlinea.mined.gob.ni/", "main website")
            human_like_navigation(driver, "https://serviciosenlinea.mined.gob.ni/mapa-de-la-educacion/", "education map")
            
            dept_id = DEPARTMENTS[department_name]['id']
            department_url = f"https://serviciosenlinea.mined.gob.ni/mapa-de-la-educacion/Departamento.aspx?Departamento={dept_id}"
            human_like_navigation(driver, department_url, f"department {department_name}")
            
            time.sleep(random.uniform(5, 10))
            
            municipality_url = f"https://serviciosenlinea.mined.gob.ni/mapa-de-la-educacion/Georreferencia.aspx?Municipio={municipality_id}"
            human_like_navigation(driver, municipality_url, f"municipality {municipality_name}")
            
            print(f"    🗺️  Waiting for map data to load...")
            WebDriverWait(driver, 45).until(lambda d: "L.marker" in d.page_source)
            print("    ✅ Map data loaded successfully!")
            
            page_source = driver.page_source
            schools = get_school_data_from_page_source(page_source)
            
            if schools:
                print(f"    🎉 Found {len(schools)} schools!")
                for school in schools:
                    school["department"] = department_name
                    school["municipality"] = municipality_name
                    school["dep_id"] = DEPARTMENTS[department_name]['id']
                    school["mun_id"] = municipality_id
                
                return schools
            else:
                print(f"    --> No schools found in page source")
                return []
                
        except TimeoutException:
            print(f"    --> Timeout waiting for {municipality_name} (attempt {attempt + 1})")
            if attempt < max_retries - 1:
                adaptive_delay(attempt, base_delay=10)
        except WebDriverException as e:
            print(f"    --> WebDriver error for {municipality_name}: {e}")
            if attempt < max_retries - 1:
                adaptive_delay(attempt, base_delay=5)
        except Exception as e:
            print(f"    --> Unexpected error for {municipality_name}: {e}")
            if attempt < max_retries - 1:
                adaptive_delay(attempt, base_delay=5)
        finally:
            if driver:
                try:
                    driver.quit()
                except:
                    pass
    
    print(f"    --> Failed to scrape {municipality_name} after {max_retries} attempts")
    return None

    return schools_data


def main():
    """
    Main function to scrape school data from ALL departments using the proven working approach.
    """
    all_schools = []
    failed_municipalities = []
    
    print("🇳🇮 NICARAGUA SCHOOLS SCRAPER - FULL COUNTRY")
    print("Using PROVEN WORKING approach from successful Boaco test")
    print("� Processing ALL 17 departments and 153 municipalities")
    print("=" * 80)
    
    start_time = time.time()
    total_municipalities = sum(len(dept["municipalities"]) for dept in DEPARTMENTS.values())
    processed = 0
    
    print(f"📊 Total departments: {len(DEPARTMENTS)}")
    print(f"📊 Total municipalities: {total_municipalities}")
    print(f"📅 Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("🚀 Starting full country scrape...")
    
    for dept_num, (department_name, department_data) in enumerate(DEPARTMENTS.items(), 1):
        print(f"\n{'='*80}")
        print(f"📍 Department {dept_num}/{len(DEPARTMENTS)}: {department_name}")
        print(f"   🆔 Department ID: {department_data['id']}")
        print(f"   🏘️  Municipalities: {len(department_data['municipalities'])}")
        print(f"{'='*80}")
        
        department_schools = []
        
        for mun_num, (municipality_name, municipality_id) in enumerate(department_data["municipalities"].items(), 1):
            processed += 1
            print(f"\n🏘️  Municipality {mun_num}/{len(department_data['municipalities'])}: {municipality_name}")
            print(f"   📊 Overall progress: {processed}/{total_municipalities} ({processed/total_municipalities*100:.1f}%)")
            print(f"   � Municipality ID: {municipality_id}")
            print("-" * 60)
            
            # Scrape with the proven working approach
            schools = scrape_municipality_with_retry(
                department_name, municipality_name, municipality_id, max_retries=3
            )
            
            if schools is not None:
                department_schools.extend(schools)
                all_schools.extend(schools)
                print(f"    ✅ SUCCESS: {len(schools)} schools added")
                print(f"    📈 Department total: {len(department_schools)}")
                print(f"    📈 Country total: {len(all_schools)}")
            else:
                failed_municipalities.append(f"{department_name} - {municipality_name}")
                print(f"    ❌ FAILED: Could not scrape {municipality_name}")
            
            # Respectful delay between municipalities (same as successful test)
            if processed < total_municipalities:
                delay = random.uniform(15, 25)  # Same delay as successful test
                print(f"    ⏱️  Waiting {delay:.1f} seconds before next municipality...")
                time.sleep(delay)
        
        print(f"\n📊 Department {department_name} Summary:")
        print(f"   ✅ Schools collected: {len(department_schools)}")
        print(f"   📈 Country total so far: {len(all_schools)}")
        
        # Save intermediate results after each department
        if all_schools:
            timestamp = datetime.now().strftime("%H%M%S")
            temp_filename = f"data/nicaraguan_schools_partial_{datetime.now().strftime('%y%m%d')}_{timestamp}.csv"
            os.makedirs("data", exist_ok=True)
            df = pd.DataFrame(all_schools)
            df.to_csv(temp_filename, index=False, encoding="utf-8")
            print(f"   💾 Partial results saved: {temp_filename}")
    
    # Final results processing
    elapsed_time = time.time() - start_time
    print(f"\n" + "=" * 80)
    print("🎉 SCRAPING COMPLETE")
    print("=" * 80)
    print(f"⏱️  Total time: {elapsed_time/60:.1f} minutes")
    print(f"✅ Successfully processed: {processed - len(failed_municipalities)}/{total_municipalities} municipalities")
    
    if failed_municipalities:
        print(f"\n❌ FAILED MUNICIPALITIES ({len(failed_municipalities)}):")
        for failed in failed_municipalities:
            print(f"  - {failed}")
    
    if all_schools:
        # Final save with proper column order
        df = pd.DataFrame(all_schools)
        df = df[['department', 'municipality', 'dep_id', 'mun_id', 'Nombre', 'Direccion', 'Latitud', 'Longitud', 'Modalidades']]
        
        # Create data directory if it doesn't exist
        data_dir = "data"
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
        
        # Save final results with timestamp
        timestamp = datetime.now().strftime("%y%m%d")
        csv_filename = os.path.join(data_dir, f"nicaraguan_schools_complete_{timestamp}.csv")
        df.to_csv(csv_filename, index=False, encoding="utf-8")
        print(f"\n💾 FINAL DATA saved to: {csv_filename}")
        
        # Display comprehensive summary statistics
        print("\n" + "=" * 80)
        print("📊 FINAL SUMMARY STATISTICS")
        print("=" * 80)
        print(f"🏫 Total schools found: {len(df)}")
        print(f"🏛️  Total departments: {len(df['department'].unique())}")
        print(f"🏘️  Total municipalities: {len(df['municipality'].unique())}")
        
        print(f"\n📋 Schools by department:")
        department_counts = df['department'].value_counts().sort_index()
        for dept, count in department_counts.items():
            print(f"   {dept}: {count} schools")
        
        print(f"\n🏆 Top 10 municipalities by school count:")
        municipality_counts = df['municipality'].value_counts().head(10)
        for muni, count in municipality_counts.items():
            dept = df[df['municipality'] == muni]['department'].iloc[0]
            print(f"   {muni} ({dept}): {count} schools")
        
        # Verify data quality
        unique_counts = len(df['municipality'].value_counts().unique())
        if unique_counts > 10:  # Good indicator of varied data
            print(f"\n✅ DATA QUALITY: Excellent - {unique_counts} different school counts across municipalities!")
        else:
            print(f"\n⚠️  DATA QUALITY: Check needed - only {unique_counts} different school counts")
        
        # Save failed municipalities for potential retry
        if failed_municipalities:
            retry_filename = os.path.join(data_dir, f"failed_municipalities_{timestamp}.txt")
            with open(retry_filename, 'w') as f:
                f.write("Failed municipalities that need retry:\n")
                for failed in failed_municipalities:
                    f.write(f"{failed}\n")
            print(f"\n📝 Failed municipalities list: {retry_filename}")
        
    else:
        print("\n❌ No school data was found!")
    
    print(f"\n🎉 Full country scrape completed in {elapsed_time/60:.1f} minutes!")


if __name__ == "__main__":
    main()
