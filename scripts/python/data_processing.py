"""
Data Processing Utilities for Nicaragua Schools Dataset
Author: Nicaragua Schools Data Project
Date: July 2025

This module provides utility functions for cleaning, validating, and processing
the Nicaragua schools dataset collected from MINED.
"""

import pandas as pd
import re
import html
from typing import List, Dict, Tuple, Optional
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class NicaraguaSchoolsProcessor:
    """Main class for processing Nicaragua schools data"""
    
    def __init__(self):
        self.nicaragua_bounds = {
            'lat_min': 10.5, 'lat_max': 15.2,
            'lng_min': -87.9, 'lng_max': -82.6
        }
        
    def clean_text_field(self, text: str) -> str:
        """Clean and standardize text fields"""
        if pd.isna(text) or text == '':
            return ''
        
        # Decode HTML entities
        text = html.unescape(str(text))
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        # Fix common encoding issues
        text = text.replace('Ã±', 'ñ').replace('Ã¡', 'á').replace('Ã©', 'é')
        text = text.replace('Ã­', 'í').replace('Ã³', 'ó').replace('Ãº', 'ú')
        
        return text
    
    def validate_coordinates(self, lat: float, lng: float) -> bool:
        """Validate if coordinates are within Nicaragua's bounds"""
        if pd.isna(lat) or pd.isna(lng):
            return False
            
        return (self.nicaragua_bounds['lat_min'] <= lat <= self.nicaragua_bounds['lat_max'] and
                self.nicaragua_bounds['lng_min'] <= lng <= self.nicaragua_bounds['lng_max'])
    
    def parse_modalidades(self, modalidades: str) -> List[str]:
        """Parse and standardize educational modalities"""
        if pd.isna(modalidades) or modalidades == '':
            return []
        
        # Split by common separators
        modalities = re.split(r'[,;|]+', str(modalidades))
        
        # Clean and standardize each modality
        cleaned_modalities = []
        for modality in modalities:
            modality = self.clean_text_field(modality)
            if modality:
                # Standardize common variations
                modality = modality.replace('Educacion', 'Educación')
                modality = modality.replace('Primaria Regular', 'Primaria')
                modality = modality.replace('Secundaria Regular', 'Secundaria')
                cleaned_modalities.append(modality)
        
        return cleaned_modalities
    
    def clean_dataset(self, df: pd.DataFrame) -> pd.DataFrame:
        """Clean the entire dataset"""
        logger.info(f"Starting data cleaning for {len(df)} records")
        
        # Create a copy to avoid modifying original
        cleaned_df = df.copy()
        
        # Clean text fields
        text_fields = ['Nombre', 'Direccion', 'Department', 'Municipality']
        for field in text_fields:
            if field in cleaned_df.columns:
                cleaned_df[field] = cleaned_df[field].apply(self.clean_text_field)
        
        # Clean and validate coordinates
        if 'Latitud' in cleaned_df.columns and 'Longitud' in cleaned_df.columns:
            # Convert to numeric, coercing errors to NaN
            cleaned_df['Latitud'] = pd.to_numeric(cleaned_df['Latitud'], errors='coerce')
            cleaned_df['Longitud'] = pd.to_numeric(cleaned_df['Longitud'], errors='coerce')
            
            # Add validation flag
            cleaned_df['valid_coordinates'] = cleaned_df.apply(
                lambda row: self.validate_coordinates(row['Latitud'], row['Longitud']), 
                axis=1
            )
        
        # Clean school codes
        if 'Codigo' in cleaned_df.columns:
            cleaned_df['Codigo'] = cleaned_df['Codigo'].apply(
                lambda x: self.clean_text_field(str(x)) if pd.notna(x) else ''
            )
        
        # Parse modalidades into standardized format
        if 'Modalidades' in cleaned_df.columns:
            cleaned_df['modalidades_parsed'] = cleaned_df['Modalidades'].apply(self.parse_modalidades)
            cleaned_df['modalidades_count'] = cleaned_df['modalidades_parsed'].apply(len)
        
        # Remove exact duplicates
        initial_count = len(cleaned_df)
        cleaned_df = cleaned_df.drop_duplicates()
        duplicate_count = initial_count - len(cleaned_df)
        
        if duplicate_count > 0:
            logger.info(f"Removed {duplicate_count} duplicate records")
        
        logger.info(f"Data cleaning complete. Final dataset: {len(cleaned_df)} records")
        
        return cleaned_df
    
    def generate_data_quality_report(self, df: pd.DataFrame) -> Dict:
        """Generate a comprehensive data quality report"""
        report = {
            'total_records': len(df),
            'missing_values': {},
            'coordinate_quality': {},
            'text_quality': {},
            'modalities_analysis': {}
        }
        
        # Missing values analysis
        for col in df.columns:
            missing_count = df[col].isna().sum()
            report['missing_values'][col] = {
                'count': int(missing_count),
                'percentage': round(missing_count / len(df) * 100, 2)
            }
        
        # Coordinate quality
        if 'Latitud' in df.columns and 'Longitud' in df.columns:
            valid_coords = df.apply(
                lambda row: self.validate_coordinates(row['Latitud'], row['Longitud']), 
                axis=1
            ).sum()
            
            report['coordinate_quality'] = {
                'total_with_coords': int((~df['Latitud'].isna() & ~df['Longitud'].isna()).sum()),
                'valid_coords': int(valid_coords),
                'invalid_coords': int((~df['Latitud'].isna() & ~df['Longitud'].isna()).sum() - valid_coords)
            }
        
        # Text quality (empty or very short fields)
        text_fields = ['Nombre', 'Direccion']
        for field in text_fields:
            if field in df.columns:
                empty_count = (df[field].isna() | (df[field].str.len() < 3)).sum()
                report['text_quality'][field] = {
                    'empty_or_short': int(empty_count),
                    'percentage': round(empty_count / len(df) * 100, 2)
                }
        
        # Modalities analysis
        if 'modalidades_parsed' in df.columns:
            all_modalities = []
            for modalities_list in df['modalidades_parsed']:
                all_modalities.extend(modalities_list)
            
            modalities_counts = pd.Series(all_modalities).value_counts()
            report['modalities_analysis'] = {
                'unique_modalities': len(modalities_counts),
                'most_common': modalities_counts.head(10).to_dict()
            }
        
        return report


def load_latest_dataset(data_dir: str = "data") -> pd.DataFrame:
    """Load the most recent Nicaragua schools dataset"""
    import os
    import glob
    
    pattern = os.path.join(data_dir, "nicaraguan_schools*.csv")
    csv_files = glob.glob(pattern)
    
    if not csv_files:
        raise FileNotFoundError(f"No Nicaragua schools CSV files found in {data_dir}")
    
    # Get the most recent file
    latest_file = max(csv_files, key=os.path.getmtime)
    
    logger.info(f"Loading data from: {os.path.basename(latest_file)}")
    
    return pd.read_csv(latest_file, encoding='utf-8')


def save_processed_data(df: pd.DataFrame, output_path: str, prefix: str = "processed"):
    """Save processed data with timestamp"""
    import os
    from datetime import datetime
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{prefix}_nicaragua_schools_{timestamp}.csv"
    full_path = os.path.join(output_path, filename)
    
    df.to_csv(full_path, index=False, encoding='utf-8')
    logger.info(f"Processed data saved to: {filename}")
    
    return full_path


# Example usage
if __name__ == "__main__":
    # Load raw data
    raw_data = load_latest_dataset()
    
    # Initialize processor
    processor = NicaraguaSchoolsProcessor()
    
    # Clean data
    cleaned_data = processor.clean_dataset(raw_data)
    
    # Generate quality report
    quality_report = processor.generate_data_quality_report(cleaned_data)
    
    # Print summary
    print(f"Data processing complete!")
    print(f"Total records: {quality_report['total_records']}")
    print(f"Valid coordinates: {quality_report['coordinate_quality'].get('valid_coords', 'N/A')}")
    
    # Save processed data
    save_processed_data(cleaned_data, "data/outputs", "cleaned")
