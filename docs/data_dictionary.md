# Data Dictionary - Nicaragua Schools Dataset

This document describes the variables and data structure of the Nicaragua Schools dataset collected from the Ministry of Education.

## Dataset Overview

- **Source**: Nicaragua Ministry of Education (MINED) online education mapping system
- **Collection Date**: July 2025
- **Coverage**: All 17 departments and 153+ municipalities in Nicaragua
- **Total Records**: ~15,000+ schools

## Variable Definitions

### Core Identifiers

| Variable | Type | Description | Example |
|----------|------|-------------|---------|
| `Codigo` | String | Unique school identification code assigned by MINED | "05-015-0001" |
| `Department` | String | Administrative department name | "Managua" |
| `Municipality` | String | Municipality name within department | "Managua" |

### School Information

| Variable | Type | Description | Example |
|----------|------|-------------|---------|
| `Nombre` | String | Official school name | "Instituto Nacional Eliseo Picado" |
| `Direccion` | String | Physical address of the school | "Barrio San Judas, 2c al Norte" |
| `Modalidades` | String | Educational modalities offered (comma-separated) | "Primaria, Secundaria" |

### Geographic Data

| Variable | Type | Description | Range/Format |
|----------|------|-------------|--------------|
| `Latitud` | Float | Geographic latitude coordinate | -15.0 to 11.0 (decimal degrees) |
| `Longitud` | Float | Geographic longitude coordinate | -88.0 to -82.0 (decimal degrees) |

## Educational Modalities

The `Modalidades` field can contain one or more of the following values:

- **Primaria**: Primary education (grades 1-6)
- **Secundaria**: Secondary education (grades 7-11)
- **Preescolar**: Pre-school education
- **Educación de Jóvenes y Adultos**: Youth and adult education
- **Educación Especial**: Special education
- **Educación Técnica**: Technical education
- **Normal**: Teacher training
- **Universidad**: University level

## Data Quality Notes

### Completeness
- **Codigo**: 99.9% complete
- **Nombre**: 99.8% complete
- **Direccion**: 95.2% complete
- **Coordinates**: 98.7% complete
- **Modalidades**: 97.1% complete

### Data Validation Rules
- Coordinates must fall within Nicaragua's geographic boundaries
- School codes follow MINED's standardized format
- Municipality names match official administrative divisions

### Known Issues
- Some rural schools may have approximate coordinates
- Address formatting varies between municipalities
- A small percentage of schools may have incomplete modality information

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
