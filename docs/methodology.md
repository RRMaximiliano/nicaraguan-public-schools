# Data Collection Methodology

This document describes the methodology used to collect Nicaragua's school data from the Ministry of Education's online mapping system.

## Overview

The Nicaragua Schools Scraper uses automated web scraping techniques to extract comprehensive school information from the Ministry of Education's (MINED) publicly available online education map. This methodology ensures systematic and reliable data collection across all 17 departments and 153+ municipalities in Nicaragua, resulting in a dataset of 10,252 schools with complete metadata coverage.

## Data Source

**Primary Source**: Nicaragua Ministry of Education Online Education Map
- **URL Pattern**: `https://mined.gob.ni/mapa-educativo/[department]/[municipality]`
- **Technology**: Interactive Leaflet.js map with marker-based school data
- **Update Frequency**: Real-time from MINED database
- **Public Access**: Freely available without authentication
- **Data Collection Date**: July 8, 2025

## Technical Approach

### Web Scraping Technology Stack

- **Browser Automation**: Selenium WebDriver with Chrome
- **Data Processing**: Python with pandas, regex, and html parsing
- **Error Handling**: Comprehensive timeout and exception management
- **Data Validation**: Real-time verification during extraction
- **Output Format**: CSV with UTF-8 encoding for international characters

### Enhanced Data Extraction Methodology

The scraper implements **order-based matching** to handle complex data extraction scenarios that were identified during development:

**Challenge**: Some schools have identical names but are located in different areas with different school IDs and metadata.

**Solution**: 
1. Extract schools from JavaScript CDATA sections (preserving insertion order)
2. Extract school dropdown information (preserving DOM order)
3. Match schools by position/order instead of name-based matching
4. Handle duplicate names as distinct institutions with unique metadata

**Results**: 
- 100% coordinate coverage across all 10,252 schools
- Perfect match between HTML counters and extracted school counts
- Complete metadata extraction including modality IDs, program IDs, and labels
- Reliable handling of schools with identical names but different locations

### Critical Technical Innovation: Fresh Browser Instances

The scraper implements a **fresh browser instance strategy** to overcome a critical caching issue discovered during development:

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

## Results and Validation

### Final Dataset Statistics (July 8, 2025)

- **Total schools extracted**: 10,252
- **Geographic coverage**: 17 departments, 153 municipalities
- **Data completeness**: 100% for all fields
- **Coordinate coverage**: 100% (all schools have valid GPS coordinates)
- **Metadata completeness**: 100% (all schools have modality and program information)
- **File size**: 2.8MB CSV file

### Data Validation Results

- **Count verification**: Extracted school counts match official government counters for each municipality
- **Coordinate validation**: All coordinates fall within Nicaragua's geographic boundaries
- **Duplicate handling**: Schools with identical names properly distinguished by position-based matching
- **Encoding verification**: UTF-8 encoding preserves Spanish characters and special symbols
- **Data consistency**: Systematic field formatting across all records

### Known Data Variations

- **Address detail**: Rural school addresses may be less specific than urban schools
- **Coordinate precision**: Some coordinates may represent approximate rather than exact locations
- **Modality complexity**: Some schools have multiple educational modalities with complex labeling

## Reproducibility

### Environment Requirements

- Python 3.8+
- Chrome browser (latest version)
- Required Python packages (see requirements.txt)
- Stable internet connection

### Execution

```bash
python scripts/python/main_scraper.py
```

### Expected Runtime

- **Complete scraping**: 6-8 hours for all municipalities
- **Per municipality**: 30-60 seconds average
- **Final dataset**: 10,252 school records
- **Output format**: CSV with UTF-8 encoding

This methodology ensures comprehensive, accurate, and ethically collected data about Nicaragua's educational infrastructure, suitable for research, policy analysis, and educational planning purposes.
