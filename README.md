# Nicaragua Schools Data Project

A comprehensive data collection and analysis project focused on Nicaragua's education system. This repository provides tools for scraping school data from Nicaragua's Ministry of Education website and performing detailed analysis of the country's educational infrastructure.

## Overview

This project creates a complete, structured dataset of Nicaragua's schools through automated web scraping of the Ministry of Education's online mapping system. The resulting dataset provides researchers, policymakers, and education professionals with comprehensive information about educational institutions across all 17 departments and 153 municipalities in Nicaragua.

The primary motivation for this work was to address the lack of accessible, structured educational data for Nicaragua. While the Ministry of Education maintains an online mapping system, there was no readily available dataset that researchers could use for systematic analysis of the country's educational infrastructure.

## Dataset Information

The complete dataset includes information for **10,252 schools** across Nicaragua's 17 departments and 153 municipalities. This represents comprehensive coverage of public educational institutions as of July 2025, including schools in remote rural areas that were previously difficult to catalog systematically.

### Data Collection Summary

- **Data Source**: Nicaragua Ministry of Education (MINED) online education map
- **Collection Date**: July 8, 2025
- **Coverage**: Complete national coverage (17 departments, 153 municipalities)
- **Total Schools**: 10,252 educational institutions
- **Data Completeness**: 100% coordinate coverage, complete metadata for all schools
- **File Size**: Approximately 2.8MB CSV file

## Data Quality & Limitations

### Strengths

Recent improvements to the scraping methodology ensure:
- **100% coordinate coverage**: All schools include precise GPS coordinates
- **Complete metadata extraction**: School IDs, modality information, and program details for all entries
- **Accurate school counts**: Perfect match between extracted data and official government counters using order-based matching
- **Duplicate name handling**: Schools with identical names but different locations are properly distinguished through position-based extraction
- **Fresh data collection**: Each municipality scraped with clean browser instances to avoid caching issues

### Limitations

- **Address quality**: Physical addresses vary in detail and standardization across municipalities
- **Coordinate precision**: GPS coordinates may represent approximate locations rather than exact building positions, particularly in rural areas
- **Point-in-time data**: Dataset reflects the state of schools as of July 8, 2025
- **Public schools only**: Private institutions are not included in the Ministry's mapping system
- **Language**: All text data is in Spanish as provided by the source system

### Technical Notes

- **Data format**: CSV with UTF-8 encoding to properly handle Spanish characters and special symbols
- **Methodology**: Order-based extraction ensures proper matching between school names and metadata, solving issues with duplicate school names
- **Browser automation**: Fresh Chrome instances for each municipality prevent data contamination from browser caching

### School Attributes

Each record in the dataset contains the following information:

#### Basic Information
- **Nombre**: Official school name as registered with the ministry
- **Direccion**: Physical address (quality varies by municipality)
- **Latitud/Longitud**: Geographic coordinates for mapping and spatial analysis
- **Modalidades**: Educational modalities offered (primary, secondary, technical, etc.)

#### Enhanced Metadata
- **school_id**: Ministry-assigned school identifier
- **modality_ids**: Numeric modality identifiers (comma-separated)
- **modality_labels**: Human-readable modality names (comma-separated)
- **program_ids**: Educational program identifiers (comma-separated)
- **program_labels**: Human-readable program names (comma-separated)

#### Administrative Information
- **department**: Administrative department where the school is located
- **municipality**: Municipal subdivision within the department
- **dep_id**: Department numeric identifier
- **mun_id**: Municipality numeric identifier

#### Available Program Types
- **1**: EDUCACION INICIAL
- **2**: PRIMARIA
- **3**: SECUNDARIA
- **6**: CEDA
- **7**: ALFABETIZACION
- **20**: EDUCACION ESPECIAL

### Geographic Coverage

The dataset covers Nicaragua's complete administrative structure:

- **17 Departments**: All major administrative divisions included
- **153+ Municipalities**: Complete municipal coverage as of data collection
- **Rural and Urban**: Schools from both metropolitan and remote rural areas

Note that coordinate precision may vary, particularly for rural schools where GPS data might be approximate rather than exact building locations.

## Project Structure

```text
nicaraguan-public-schools/
├── README.md 
├── requirements.txt 
├── r_requirements.txt
├── .gitignore 
│
├── data/ 
│   ├── raw/
│   │   └── nicaraguan_schools_250708.csv
│   ├── processed/ 
│   └── outputs/ 
│
├── scripts/ 
│   ├── python/
│   │   ├── main_scraper.py 
│   │   ├── data_processing.py 
│   │   └── validation.py 
│   └── r/  
│       ├── 01_descstats.R 
│       ├── 02_spatial_analysis.R
│       └── 03_visualizations.R 
│
├── docs/
│   ├── methodology.md        
│   ├── data_dictionary.md    
│   └── analysis_reports/      
│
└── LICENSE
```

## Quick Start

### Prerequisites

- Python 3.8+
- R 4.0+ (for analysis scripts)
- Chrome browser
- Git

### Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/yourusername/nicaraguan-public-schools.git
   cd nicaraguan-public-schools
   ```

2. **Install Python dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

3. **Install R packages** (optional, for analysis):

   ```r
   install.packages(c("tidyverse", "sf", "leaflet", "plotly"))
   ```

### Running the Scraper

The main scraper can be executed with various options:

```bash
# Run the complete scraper for all departments
python scripts/python/main_scraper.py

# Output will be saved in data/raw/ with timestamp
# Example: nicaraguan_schools_250708.csv
```

### Basic Analysis (R)

```r
# Load and explore the data
source("scripts/r/01_descstats.R")

# Perform spatial analysis
source("scripts/r/02_spatial_analysis.R")

# Create visualizations
source("scripts/r/03_visualizations.R")
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Data Source

Data is collected from Nicaragua's Ministry of Education (MINED) public education mapping system. Please respect their terms of service and use this data responsibly for research and educational purposes.

## Research Applications

This dataset enables various types of educational research and analysis:

- **Geographic accessibility**: Analysis of school distribution and access patterns across departments and municipalities
- **Educational equity**: Investigation of resource distribution and educational opportunities across regions
- **Infrastructure planning**: Support for educational infrastructure development and resource allocation decisions
- **Spatial analysis**: GIS-based studies of educational service coverage and geographic gaps
- **Comparative studies**: Baseline data for longitudinal studies of Nicaragua's education system

## Citation

If you use this dataset in your research, please cite this repository and acknowledge the data source:

```text
Nicaragua Schools Dataset (2025). Collected from Nicaragua Ministry of Education online mapping system. 
Available at: [repository URL]
```

## Contributing

Contributions to improve the scraping methodology, data processing, or analysis scripts are welcome. Please follow standard practices for pull requests and ensure that any changes maintain data quality and accuracy.
