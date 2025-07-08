"""
Data Validation Tools for Nicaragua Schools Dataset
Author: Rony Rodriguez
Date: July 2025

This module provides validation functions to ensure data quality and consistency
in the Nicaragua schools dataset.
"""

import pandas as pd
import re
from typing import List, Dict, Tuple, Set
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SchoolDataValidator:
    """Comprehensive validator for Nicaragua schools data"""
    
    def __init__(self):
        # Known departments in Nicaragua
        self.valid_departments = {
            'Boaco', 'Carazo', 'Chinandega', 'Chontales', 'Estelí', 'Granada',
            'Jinotega', 'León', 'Madriz', 'Managua', 'Masaya', 'Matagalpa',
            'Nueva Segovia', 'RACCS', 'RACCN', 'Río San Juan', 'Rivas'
        }
        
        # Nicaragua coordinate boundaries
        self.nicaragua_bounds = {
            'lat_min': 10.5, 'lat_max': 15.2,
            'lng_min': -87.9, 'lng_max': -82.6
        }
        
        # Common educational modalities
        self.valid_modalities = {
            'Primaria', 'Secundaria', 'Preescolar', 'Educación de Jóvenes y Adultos',
            'Educación Especial', 'Educación Técnica', 'Normal', 'Universidad'
        }
        
    def validate_school_code(self, codigo: str) -> Tuple[bool, str]:
        """Validate school code format"""
        if pd.isna(codigo) or codigo == '':
            return False, "School code is empty"
        
        # Basic format check (department-municipality-school pattern)
        code_pattern = r'^\d{2}-\d{3}-\d{4}$'
        if not re.match(code_pattern, str(codigo)):
            return False, f"Invalid code format: {codigo}"
        
        return True, "Valid"
    
    def validate_coordinates(self, lat: float, lng: float) -> Tuple[bool, str]:
        """Validate geographic coordinates"""
        if pd.isna(lat) or pd.isna(lng):
            return False, "Missing coordinates"
        
        try:
            lat, lng = float(lat), float(lng)
        except (ValueError, TypeError):
            return False, "Invalid coordinate format"
        
        # Check if within Nicaragua bounds
        if not (self.nicaragua_bounds['lat_min'] <= lat <= self.nicaragua_bounds['lat_max']):
            return False, f"Latitude {lat} outside Nicaragua bounds"
        
        if not (self.nicaragua_bounds['lng_min'] <= lng <= self.nicaragua_bounds['lng_max']):
            return False, f"Longitude {lng} outside Nicaragua bounds"
        
        return True, "Valid"
    
    def validate_department(self, department: str) -> Tuple[bool, str]:
        """Validate department name"""
        if pd.isna(department) or department == '':
            return False, "Department is empty"
        
        department_clean = str(department).strip()
        
        if department_clean not in self.valid_departments:
            # Check for common variations
            close_matches = [d for d in self.valid_departments 
                           if d.lower() in department_clean.lower() or 
                           department_clean.lower() in d.lower()]
            
            if close_matches:
                return False, f"Department '{department_clean}' not standard. Did you mean: {close_matches[0]}?"
            else:
                return False, f"Unknown department: {department_clean}"
        
        return True, "Valid"
    
    def validate_school_name(self, nombre: str) -> Tuple[bool, str]:
        """Validate school name"""
        if pd.isna(nombre) or nombre == '':
            return False, "School name is empty"
        
        nombre_clean = str(nombre).strip()
        
        if len(nombre_clean) < 3:
            return False, f"School name too short: '{nombre_clean}'"
        
        # Check for suspicious patterns
        if re.match(r'^\d+$', nombre_clean):
            return False, f"School name appears to be only numbers: '{nombre_clean}'"
        
        return True, "Valid"
    
    def validate_modalities(self, modalidades: str) -> Tuple[bool, str]:
        """Validate educational modalities"""
        if pd.isna(modalidades) or modalidades == '':
            return True, "No modalities specified"  # This might be acceptable
        
        # Split and clean modalities
        modality_list = re.split(r'[,;|]+', str(modalidades))
        modality_list = [m.strip() for m in modality_list if m.strip()]
        
        unknown_modalities = []
        for modality in modality_list:
            # Check if modality matches any known modality (case insensitive, partial match)
            if not any(known.lower() in modality.lower() or modality.lower() in known.lower() 
                      for known in self.valid_modalities):
                unknown_modalities.append(modality)
        
        if unknown_modalities:
            return False, f"Unknown modalities: {unknown_modalities}"
        
        return True, "Valid"
    
    def validate_record(self, record: pd.Series) -> Dict[str, Tuple[bool, str]]:
        """Validate a complete school record"""
        validations = {}
        
        # Validate school code
        if 'Codigo' in record:
            validations['codigo'] = self.validate_school_code(record['Codigo'])
        
        # Validate coordinates
        if 'Latitud' in record and 'Longitud' in record:
            validations['coordinates'] = self.validate_coordinates(
                record['Latitud'], record['Longitud']
            )
        
        # Validate department
        if 'Department' in record:
            validations['department'] = self.validate_department(record['Department'])
        
        # Validate school name
        if 'Nombre' in record:
            validations['nombre'] = self.validate_school_name(record['Nombre'])
        
        # Validate modalities
        if 'Modalidades' in record:
            validations['modalidades'] = self.validate_modalities(record['Modalidades'])
        
        return validations
    
    def validate_dataset(self, df: pd.DataFrame) -> Dict[str, any]:
        """Validate entire dataset and return comprehensive report"""
        logger.info(f"Starting validation of {len(df)} records")
        
        validation_report = {
            'total_records': len(df),
            'validation_summary': {},
            'error_details': [],
            'statistics': {},
            'recommendations': []
        }
        
        # Track validation results
        validation_results = {
            'codigo': {'valid': 0, 'invalid': 0, 'errors': []},
            'coordinates': {'valid': 0, 'invalid': 0, 'errors': []},
            'department': {'valid': 0, 'invalid': 0, 'errors': []},
            'nombre': {'valid': 0, 'invalid': 0, 'errors': []},
            'modalidades': {'valid': 0, 'invalid': 0, 'errors': []}
        }
        
        # Validate each record
        for idx, record in df.iterrows():
            record_validations = self.validate_record(record)
            
            for field, (is_valid, message) in record_validations.items():
                if is_valid:
                    validation_results[field]['valid'] += 1
                else:
                    validation_results[field]['invalid'] += 1
                    validation_results[field]['errors'].append({
                        'row': idx,
                        'message': message,
                        'value': record.get(field.title(), 'N/A')
                    })
        
        # Generate summary
        for field, results in validation_results.items():
            total = results['valid'] + results['invalid']
            if total > 0:
                validation_report['validation_summary'][field] = {
                    'valid_count': results['valid'],
                    'invalid_count': results['invalid'],
                    'valid_percentage': round(results['valid'] / total * 100, 2),
                    'error_sample': results['errors'][:5]  # Show first 5 errors
                }
        
        # Additional statistics
        validation_report['statistics'] = {
            'duplicate_codes': len(df) - len(df.drop_duplicates(subset=['Codigo'])),
            'missing_coordinates': df[['Latitud', 'Longitud']].isna().any(axis=1).sum(),
            'empty_names': df['Nombre'].isna().sum() if 'Nombre' in df.columns else 0,
            'unique_departments': df['Department'].nunique() if 'Department' in df.columns else 0,
            'unique_municipalities': df['Municipality'].nunique() if 'Municipality' in df.columns else 0
        }
        
        # Generate recommendations
        self._generate_recommendations(validation_report)
        
        logger.info("Validation complete")
        return validation_report
    
    def _generate_recommendations(self, report: Dict) -> None:
        """Generate recommendations based on validation results"""
        recommendations = []
        
        # Check coordinate quality
        coord_stats = report['validation_summary'].get('coordinates', {})
        if coord_stats.get('valid_percentage', 100) < 95:
            recommendations.append(
                f"Coordinate quality is {coord_stats.get('valid_percentage', 0)}%. "
                "Consider reviewing and correcting invalid coordinates."
            )
        
        # Check department consistency
        dept_stats = report['validation_summary'].get('department', {})
        if dept_stats.get('invalid_count', 0) > 0:
            recommendations.append(
                f"Found {dept_stats.get('invalid_count', 0)} invalid department names. "
                "Standardize department names to match official list."
            )
        
        # Check for duplicates
        if report['statistics']['duplicate_codes'] > 0:
            recommendations.append(
                f"Found {report['statistics']['duplicate_codes']} duplicate school codes. "
                "Review and remove or correct duplicates."
            )
        
        # Check name quality
        name_stats = report['validation_summary'].get('nombre', {})
        if name_stats.get('valid_percentage', 100) < 98:
            recommendations.append(
                "Some school names appear to be invalid or too short. "
                "Review name quality and standardization."
            )
        
        report['recommendations'] = recommendations


def run_validation_report(csv_file: str, output_file: str = None) -> Dict:
    """Run complete validation on a CSV file and optionally save report"""
    
    # Load data
    logger.info(f"Loading data from {csv_file}")
    df = pd.read_csv(csv_file, encoding='utf-8')
    
    # Run validation
    validator = SchoolDataValidator()
    report = validator.validate_dataset(df)
    
    # Print summary
    print("\n=== VALIDATION SUMMARY ===")
    print(f"Total records: {report['total_records']}")
    
    for field, stats in report['validation_summary'].items():
        print(f"{field.title()}: {stats['valid_percentage']}% valid "
              f"({stats['invalid_count']} invalid)")
    
    print(f"\nStatistics:")
    print(f"- Duplicate codes: {report['statistics']['duplicate_codes']}")
    print(f"- Missing coordinates: {report['statistics']['missing_coordinates']}")
    print(f"- Unique departments: {report['statistics']['unique_departments']}")
    print(f"- Unique municipalities: {report['statistics']['unique_municipalities']}")
    
    if report['recommendations']:
        print("\nRecommendations:")
        for i, rec in enumerate(report['recommendations'], 1):
            print(f"{i}. {rec}")
    
    # Save report if requested
    if output_file:
        import json
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        logger.info(f"Validation report saved to {output_file}")
    
    return report


# Example usage
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        csv_file = sys.argv[1]
        output_file = sys.argv[2] if len(sys.argv) > 2 else None
        run_validation_report(csv_file, output_file)
    else:
        print("Usage: python validation.py <csv_file> [output_report.json]")
        print("Example: python validation.py data/nicaraguan_schools.csv validation_report.json")
