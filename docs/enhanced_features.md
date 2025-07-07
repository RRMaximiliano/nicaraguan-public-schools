# Enhanced Nicaragua Schools Scraper

## New Features Added

The Nicaragua Schools Scraper has been enhanced to extract additional metadata from the Ministry of Education's dropdown menus. This provides valuable identifiers that can be used for linking with other MINED databases and for more detailed analysis.

## What's New

### 1. School ID Extraction
- **Source**: "Buscar Centros Educativos" dropdown menu  
- **Example**: `<option value="2694">PEDRO JOAQUIN CHAMORRO CARDENAL</option>`
- **Field**: `school_id` (e.g., "2694")
- **Purpose**: Official MINED school identifier for database linking

### 2. Modality ID Extraction  
- **Source**: "Buscar por Modalidad" dropdown menu
- **Example**: `<option value="3">PRIMARIA REGULAR</option>`
- **Field**: `modality_ids` (e.g., "3,12" for multiple modalities)
- **Purpose**: Official modality classifications used by MINED

### 3. Program ID Extraction
- **Source**: "Buscar por Programa Educativo" dropdown menu  
- **Example**: `<option value="3">SECUNDARIA</option>`
- **Field**: `program_ids` (e.g., "3,6" for multiple programs)
- **Purpose**: Educational program classifications

## Enhanced Data Structure

The scraped data now includes these additional fields:

```csv
Nombre,Direccion,Latitud,Longitud,Modalidades,department,municipality,dep_id,mun_id,school_id,modality_ids,program_ids
"PEDRO JOAQUIN CHAMORRO CARDENAL","Barrio Centro","12.4692","-85.6658","PRIMARIA REGULAR","Boaco","Boaco",11,100,"2694","3","1"
```

## Technical Implementation

### Matching Strategy
The scraper uses a multi-level matching approach:

1. **Exact Name Match**: Tries to match school names exactly
2. **Partial Match**: Uses substring matching for similar names
3. **Normalized Match**: Removes common words like "CENTRO ESCOLAR" for better matching
4. **Modality Mapping**: Maps extracted modalities to dropdown options

## Recent Improvements (January 2025)

### Fixed Modality ID Matching
The modality matching algorithm has been improved to provide more accurate results:

**Previous Issue**: Schools were getting multiple modality IDs due to over-matching
- Example: "SECUNDARIA REGULAR" would get IDs: 30,13,5 (incorrect)

**Current Solution**: Exact matching with fallback to careful partial matching
- Example: "SECUNDARIA REGULAR" now gets ID: 5 (correct)

**Matching Strategy**:
1. **Exact Match**: First attempts exact string match (case-insensitive)
2. **Careful Partial Match**: If no exact match, uses substring matching only for significant substrings (>3 characters)
3. **Duplicate Prevention**: Each modality in a school gets matched only once

### Added Program Labels
The scraper now extracts both program IDs and their corresponding labels:

**New Fields**:
- `program_ids`: Numeric identifiers (e.g., "2,3,6")
- `program_labels`: Human-readable names (e.g., "PRIMARIA,SECUNDARIA,CEDA")

**Available Program Types**:
- ID 1: EDUCACION INICIAL
- ID 2: PRIMARIA  
- ID 3: SECUNDARIA
- ID 6: CEDA
- ID 7: ALFABETIZACION
- ID 20: EDUCACION ESPECIAL

### Enhanced Data Quality
The improvements ensure that:
- Each school has accurate, specific modality assignments
- Program information includes both machine-readable IDs and human-readable labels
- Matching is more precise and reduces false positives
- Data integrity is maintained across all educational levels

## Data Quality Considerations

- **Coverage**: Not all schools may have exact matches in dropdowns
- **Accuracy**: Matching is best-effort and may have some false positives
- **Completeness**: Some municipalities may have incomplete dropdown data
- **Validation**: Results should be validated against known school records

## Usage Examples

### Basic Usage
```python
# The enhanced scraper works the same way as before
schools = scrape_municipality_with_retry("Boaco", "Boaco", 100)

# But now includes additional fields
for school in schools:
    print(f"School: {school['Nombre']}")
    print(f"School ID: {school['school_id']}")
    print(f"Modality IDs: {school['modality_ids']}")
    print(f"Program IDs: {school['program_ids']}")
```

### Testing
```bash
# Test the enhanced functionality
python test_enhanced_scraper.py
```

### Full Scraping
```bash
# Run with enhanced features on all municipalities
python scripts/python/nicaragua_schools_scraper.py
```

## Benefits of Enhanced Data

### 1. Database Linking
- Link schools with other MINED databases using school_id
- Cross-reference with enrollment data, teacher assignments, etc.
- Build comprehensive educational data warehouse

### 2. Analysis Capabilities
- Group schools by official modality classifications
- Analyze program distribution across regions
- Track changes in educational offerings over time

### 3. Data Validation
- Verify school classifications against official records
- Identify inconsistencies in educational offerings
- Quality assurance for policy decisions

## Known Limitations

### Matching Challenges
- School names may vary between map markers and dropdown lists
- Some schools might not appear in all dropdown menus
- Manual verification recommended for critical applications

### Performance Impact
- Slightly slower due to HTML parsing
- Minimal impact on overall scraping time
- BeautifulSoup dependency added

### Data Completeness
- Dropdown data availability varies by municipality
- Some rural areas may have limited metadata
- Coverage improves for larger municipalities

## Future Enhancements

### Potential Improvements
- Machine learning for better name matching
- Integration with other MINED data sources
- Historical tracking of ID changes
- Automated validation against official records

### Data Enrichment
- Teacher count and qualifications
- Infrastructure details
- Student enrollment numbers
- Budget and resource allocation

## Troubleshooting

### Common Issues
1. **Missing BeautifulSoup**: Install with `pip install beautifulsoup4`
2. **Low match rates**: Check school name variations in dropdowns
3. **Empty dropdown data**: Some municipalities may have incomplete forms

### Debugging
- Check `data/raw/` for dropdown metadata files
- Review console output for match statistics
- Validate results against known school records

## Contributing

When contributing enhancements:
- Maintain backward compatibility
- Test on multiple municipalities
- Document any new matching strategies
- Consider performance implications

The enhanced scraper maintains all existing functionality while adding valuable metadata extraction capabilities. This makes the dataset more useful for research, policy analysis, and integration with other educational databases.
