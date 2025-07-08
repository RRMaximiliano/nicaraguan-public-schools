# Data Dictionary - Nicaragua Schools Dataset

This document describes the variables and data structure of the Nicaragua Schools dataset collected from the Ministry of Education.

## Dataset Overview

- **Source**: Nicaragua Ministry of Education (MINED) online education mapping system
- **Collection Date**: July 8, 2025
- **Coverage**: All 17 departments and 153 municipalities in Nicaragua
- **Total Records**: 10,252 schools
- **Data Quality**: 100% coordinate coverage, complete metadata for all schools
- **File Format**: CSV with UTF-8 encoding

## Variable Definitions

### Core Identifiers

| Variable | Type | Description | Example |
|----------|------|-------------|---------|
| `school_id` | String | Unique school identification number assigned by MINED | "4407" |
| `department` | String | Administrative department name | "Managua" |
| `municipality` | String | Municipality name within department | "Managua" |
| `dep_id` | Integer | Department numeric identifier | 8 |
| `mun_id` | Integer | Municipality numeric identifier | 80 |

### School Information

| Variable | Type | Description | Example |
|----------|------|-------------|---------|
| `Nombre` | String | Official school name | "Instituto Nacional Eliseo Picado" |
| `Direccion` | String | Physical address of the school | "Barrio San Judas, 2c al Norte" |

### Enhanced Metadata

| Variable | Type | Description | Example |
|----------|------|-------------|---------|
| `modality_ids` | String | Numeric modality identifiers (comma-separated) | "3,14" |
| `modality_labels` | String | Human-readable modality names (comma-separated) | "SECUNDARIA,PRIMARIA MULTIGRADO" |
| `program_ids` | String | Educational program identifiers (comma-separated) | "2,3" |
| `program_labels` | String | Human-readable program names (comma-separated) | "PRIMARIA,SECUNDARIA" |

### Geographic Data

| Variable | Type | Description | Range/Format |
|----------|------|-------------|--------------|
| `Latitud` | Float | Geographic latitude coordinate | 10.0 to 15.0 (decimal degrees) |
| `Longitud` | Float | Geographic longitude coordinate | -88.0 to -82.0 (decimal degrees) |

## Educational Modalities & Programs

### Available Modality Types (Most Common)

| ID | Label | Description | Frequency |
|----|-------|-------------|-----------|
| 14 | PRIMARIA MULTIGRADO | Multi-grade primary education | High |
| 10 | PREESCOLAR COMUNITARIO MULTINIVEL | Community pre-school multiple levels | High |
| 3 | SECUNDARIA REGULAR | Regular secondary education | Medium |
| 11 | PREESCOLAR FORMAL MULTINIVEL | Formal pre-school multiple levels | Medium |
| 2 | PREESCOLAR FORMAL | Formal pre-school | Medium |
| 102 | EBA | Adult basic education (Educación Básica de Adultos) | Low |
| 5 | PRIMARIA REGULAR | Regular primary education | Medium |

*Note: Actual dataset contains 30+ different modality types. This table shows the most frequently occurring ones.*

### Available Program Types (Most Common)

| ID | Label | Description | Frequency |
|----|-------|-------------|-----------|
| 2 | PRIMARIA | Primary education | Very High |
| 3 | SECUNDARIA | Secondary education | High |
| 1 | EDUCACION INICIAL | Early childhood education | Medium |
| 5 | (Various Labels) | Mixed educational programs | Low |
| 11 | (Various Labels) | Specialized programs | Low |

*Note: Program mapping is complex with some inconsistencies in the source data. Primary and secondary education represent the majority of schools.*

## Data Quality Summary

### Completeness (July 2025)

- **school_id**: 100% complete
- **Nombre**: 100% complete  
- **Direccion**: 100% complete
- **Coordinates**: 100% complete
- **modality_labels**: 100% complete
- **modality_ids**: 100% complete
- **program_labels**: 100% complete
- **program_ids**: 100% complete

### Data Validation Features

- All coordinates verified within Nicaragua's geographic boundaries
- School IDs validated against Ministry dropdown data
- Municipality names match official administrative divisions
- Perfect match between extracted data and official government counters
- Order-based matching ensures same-named schools are properly distinguished

## Usage Guidelines

### For Analysis
- Use `Department` and `Municipality` for geographic aggregation
- Coordinates are suitable for mapping and spatial analysis
- `Modalidades` requires parsing for categorical analysis

### For Visualization
- Coordinate precision is suitable for mapping at municipality level
- School density maps should account for population distribution
- Modality analysis should consider rural/urban contexts

## Update Frequency

This dataset represents a snapshot of Nicaragua's educational infrastructure as of July 2025. The Ministry of Education updates their records regularly, so periodic re-scraping may be necessary for current analysis.

## Related Documentation

- `methodology.md`: Details about data collection process
- `README.md`: Project overview and usage instructions
- Source scripts in `scripts/python/`: Implementation details
