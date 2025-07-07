# Data Collection Methodology

This document describes the methodology used to collect Nicaragua's school data from the Ministry of Education's online mapping system.

## Overview

The Nicaragua Schools Scraper uses automated web scraping techniques to extract comprehensive school information from the Ministry of Education's (MINED) publicly available online education map. This methodology ensures systematic and reliable data collection across all 17 departments and 153+ municipalities in Nicaragua.

## Data Source

**Primary Source**: Nicaragua Ministry of Education Online Education Map
- **URL Pattern**: `https://mined.gob.ni/mapa-educativo/[department]/[municipality]`
- **Technology**: Interactive Leaflet.js map with marker-based school data
- **Update Frequency**: Real-time from MINED database
- **Public Access**: Freely available without authentication

## Technical Approach

### Web Scraping Technology Stack

- **Browser Automation**: Selenium WebDriver with Chrome
- **Data Processing**: Python with pandas, regex, and BeautifulSoup
- **Error Handling**: Comprehensive timeout and exception management
- **Data Validation**: Real-time verification during extraction

### Key Technical Innovation

The scraper implements a **fresh browser instance strategy** to overcome a critical caching issue:

**Problem**: The original map system would cache the first municipality's data and display it for all subsequent municipalities, regardless of the URL.

**Solution**: Create a new Chrome browser instance for each municipality, ensuring clean state and accurate data extraction.

## Data Collection Process

### 1. Department and Municipality Mapping

```python
DEPARTMENTS = {
    "Department_Name": {
        "id": unique_id,
        "municipalities": {
            "Municipality_Name": municipality_id,
            # ... additional municipalities
        }
    }
}
```

### 2. Systematic Iteration

1. **Department Loop**: Iterate through all 17 departments
2. **Municipality Loop**: For each municipality within a department:
   - Create fresh Chrome browser instance
   - Navigate to municipality-specific URL
   - Wait for JavaScript content to load
   - Extract school data
   - Close browser instance
   - Apply 2-second delay (server respect)

### 3. Data Extraction Process

#### Step 3.1: Page Loading
```python
# Navigate to municipality URL
driver.get(f"https://mined.gob.ni/mapa-educativo/{dept_id}/{muni_id}")

# Wait for JavaScript-rendered content
WebDriverWait(driver, 30).until(
    EC.presence_of_element_located((By.CLASS_NAME, "leaflet-marker-icon"))
)
```

#### Step 3.2: Content Extraction
```python
# Extract page source after JavaScript execution
page_source = driver.page_source

# Parse HTML content
soup = BeautifulSoup(page_source, 'html.parser')
```

#### Step 3.3: School Data Parsing
Using regex patterns to extract school information from map markers:

```python
# Extract school codes
codigo_pattern = r'<strong>Codigo:\s*</strong>\s*([^<]+)'

# Extract school names  
nombre_pattern = r'<strong>Nombre:\s*</strong>\s*([^<]+)'

# Extract addresses
direccion_pattern = r'<strong>Direccion:\s*</strong>\s*([^<]+)'

# Extract coordinates from marker positioning
lat_lng_pattern = r'L\.marker\(\[([^,]+),\s*([^\]]+)\]'

# Extract educational modalities
modalidades_pattern = r'<strong>Modalidades:\s*</strong>\s*([^<]+)'
```

## Quality Assurance

### Data Validation

1. **Coordinate Validation**: Ensure coordinates fall within Nicaragua's boundaries
2. **Format Consistency**: Standardize text formatting and encoding
3. **Completeness Checks**: Verify all required fields are populated
4. **Duplicate Detection**: Identify and handle duplicate records

### Error Handling

- **Timeout Management**: 30-second waits for page loading
- **Network Resilience**: Retry logic for failed requests
- **Resource Cleanup**: Proper browser instance disposal
- **Progress Tracking**: Detailed logging for monitoring

### Performance Optimization

- **Chrome Options**: Optimized for speed and reliability
- **Memory Management**: Fresh instances prevent memory leaks
- **Respectful Scraping**: 2-second delays between municipalities
- **Efficient Parsing**: Compiled regex patterns for speed

## Ethical Considerations

### Compliance
- **Public Data**: Only accessing publicly available information
- **Terms Respect**: Following website terms of service
- **Server Load**: Implementing delays to minimize server impact
- **No Authentication**: Not accessing restricted areas

### Data Usage
- **Educational Purpose**: Data used for research and analysis
- **Attribution**: Proper credit to original data source
- **No Commercial Use**: Respecting public data access intent

## Limitations and Considerations

### Technical Limitations
- **JavaScript Dependency**: Requires full browser rendering
- **Network Dependent**: Requires stable internet connection
- **Browser Dependent**: Requires Chrome browser installation

### Data Limitations
- **Snapshot Nature**: Data reflects point-in-time state
- **Source Accuracy**: Limited by original data quality
- **Address Standardization**: Varies across municipalities
- **Coordinate Precision**: May vary for rural locations

## Output Format

The scraper generates CSV files with the following structure:

```csv
Codigo,Nombre,Direccion,Latitud,Longitud,Modalidades,Department,Municipality
05-015-0001,Instituto Nacional Eliseo Picado,Barrio San Judas...,12.1364,-86.2514,Primaria Secundaria,Managua,Managua
```

## Reproducibility

### Environment Requirements
- Python 3.8+
- Chrome browser (latest version)
- Required Python packages (see requirements.txt)
- Stable internet connection

### Execution
```bash
python scripts/python/nicaragua_schools_scraper.py
```

### Expected Runtime
- **Complete scraping**: 6-8 hours for all municipalities
- **Per municipality**: 30-60 seconds average
- **Data volume**: ~15,000 school records

This methodology ensures comprehensive, accurate, and ethically collected data about Nicaragua's educational infrastructure, suitable for research, policy analysis, and educational planning purposes.
