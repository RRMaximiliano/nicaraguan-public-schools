# Nicaragua Schools Data Project

A comprehensive data collection and analysis project focused on Nicaragua's education system. This repository provides tools for scraping school data from Nicaragua's Ministry of Education website and performing detailed data analysis.

## Overview

This project was developed to create a complete dataset of Nicaragua's schools and provide analytical insights into the country's educational infrastructure. The repository includes web scraping tools, data processing scripts, and analysis capabilities that should be useful for researchers, policymakers, and education professionals working on Central American education systems.

The main motivation behind this work came from the need to have a centralized, clean dataset of educational institutions across Nicaragua. While the Ministry of Education provides an online mapping system, there wasn't a readily available structured dataset that researchers could easily use for analysis.

## Dataset Information

The complete dataset includes information for approximately 15,000 schools across Nicaragua. This represents what we believe to be near-complete coverage of public educational institutions as of July 2025, though some remote rural schools might occasionally be missing from the original government database.

### School Attributes

Each record in the dataset contains the following information:

- **Nombre**: Official school name as registered with the ministry
- **Direccion**: Physical address (quality varies by municipality)
- **Latitud/Longitud**: Geographic coordinates for mapping and spatial analysis
- **Modalidades**: Educational modalities offered (primary, secondary, technical, etc.)
- **Department**: Administrative department where the school is located
- **Municipality**: Municipal subdivision within the department

### Geographic Coverage

The dataset covers Nicaragua's complete administrative structure:

- **17 Departments**: All major administrative divisions included
- **153+ Municipalities**: Complete municipal coverage as of data collection
- **Rural and Urban**: Schools from both metropolitan and remote rural areas

Note that coordinate precision may vary, particularly for rural schools where GPS data might be approximate rather than exact building locations.

## 🏗️ Project Structure

```
nicaraguan-public-schools/
├── README.md 
├── requirements.txt 
├── .gitignore 
│
├── data/ 
│   ├── raw/
│   ├── processed/ 
│   └── outputs/ 
│
├── scripts/ 
│   ├── python/
│   │   ├── nicaragua_schools_scraper.py 
│   │   ├── data_processing.py 
│   │   └── validation.py 
│   └── r/  
│       ├── exploratory_analysis.R 
│       ├── spatial_analysis.R
│       └── visualizations.R 
│
├── docs/
    ├── methodology.md        
    ├── data_dictionary.md    
    └── analysis_reports/      
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

```bash
# Run the complete scraper
python scripts/python/nicaragua_schools_scraper.py

# Results will be saved in data/raw/
```

### Basic Analysis (R)

```r
# Load and explore the data
source("scripts/r/exploratory_analysis.R")

# Create visualizations
source("scripts/r/visualizations.R")
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Data Source

Data is collected from Nicaragua's Ministry of Education (MINED) public education mapping system. Please respect their terms of service and use this data responsibly for research and educational purposes.
