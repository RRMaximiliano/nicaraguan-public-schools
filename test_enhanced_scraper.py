#!/usr/bin/env python3
"""
Test script for the enhanced Nicaragua Schools Scraper
Tests the new functionality to extract school IDs, modality IDs, and program IDs
"""

import sys
import os
import pandas as pd
from datetime import datetime

# Add the scripts directory to path
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(script_dir, 'scripts'))

from python.enhanced_scraper import (
    test_enhanced_scraper as run_enhanced_test
)
from python.nicaragua_schools_scraper import DEPARTMENTS

def test_enhanced_scraper():
    """
    Test the enhanced scraper on Boaco municipality to verify new features work.
    """
    print("Testing Enhanced Nicaragua Schools Scraper")
    print("=" * 50)
    print("Testing on: Boaco Department, Boaco Municipality")
    print("New features being tested:")
    print("- School ID extraction from dropdown")
    print("- Modality ID extraction from dropdown")  
    print("- Program ID extraction from dropdown")
    print()
    
    department_name = "Boaco"
    municipality_name = "Boaco"
    municipality_id = DEPARTMENTS[department_name]['municipalities'][municipality_name]
    
    print(f"Department: {department_name}")
    print(f"Municipality: {municipality_name}")
    print(f"Municipality ID: {municipality_id}")
    print()
    
    # Run the enhanced scraper
    print("Starting enhanced scraping...")
    result = run_enhanced_test(department_name, municipality_name)
    
    if result is None:
        print("❌ Scraping failed!")
        return False
    
    schools, dropdown_data = result
    
    if not schools:
        print("❌ No schools found!")
        return False
    
    print(f"✅ Successfully scraped {len(schools)} schools!")
    print()
    
    # Analyze the enhanced data
    schools_with_ids = sum(1 for school in schools if school.get('school_id'))
    schools_with_modality_ids = sum(1 for school in schools if school.get('modality_ids'))
    schools_with_program_ids = sum(1 for school in schools if school.get('program_ids'))
    
    print("Enhanced Data Analysis:")
    print(f"- Schools with School IDs: {schools_with_ids}/{len(schools)} ({schools_with_ids/len(schools)*100:.1f}%)")
    print(f"- Schools with Modality IDs: {schools_with_modality_ids}/{len(schools)} ({schools_with_modality_ids/len(schools)*100:.1f}%)")
    print(f"- Schools with Program IDs: {schools_with_program_ids}/{len(schools)} ({schools_with_program_ids/len(schools)*100:.1f}%)")
    print()
    
    # Show sample enhanced data
    print("Sample Enhanced School Data:")
    print("-" * 30)
    for i, school in enumerate(schools[:3]):
        print(f"School {i+1}:")
        print(f"  Name: {school.get('Nombre', 'N/A')}")
        print(f"  Address: {school.get('Direccion', 'N/A')}")
        print(f"  Coordinates: {school.get('Latitud', 'N/A')}, {school.get('Longitud', 'N/A')}")
        print(f"  Modalities: {school.get('Modalidades', 'N/A')}")
        print(f"  School ID: {school.get('school_id', 'Not found')}")
        print(f"  Modality IDs: {school.get('modality_ids', 'Not found')}")
        print(f"  Program IDs: {school.get('program_ids', 'Not found')}")
        print(f"  Department ID: {school.get('dep_id', 'N/A')}")
        print(f"  Municipality ID: {school.get('mun_id', 'N/A')}")
        print()
    
    # Save test results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f"data/raw/enhanced_test_{department_name}_{municipality_name}_{timestamp}.csv"
    
    try:
        df = pd.DataFrame(schools)
        df.to_csv(output_file, index=False, encoding='utf-8')
        print(f"✅ Test results saved to: {output_file}")
    except Exception as e:
        print(f"❌ Failed to save results: {e}")
    
    # Check if we have the enhanced columns
    sample_school = schools[0]
    required_enhanced_fields = ['school_id', 'modality_ids', 'program_ids']
    has_enhanced_fields = all(field in sample_school for field in required_enhanced_fields)
    
    if has_enhanced_fields:
        print("✅ Enhanced fields are present in the data!")
        return True
    else:
        print("❌ Enhanced fields are missing from the data!")
        return False


if __name__ == "__main__":
    success = test_enhanced_scraper()
    if success:
        print("\n🎉 Enhanced scraper test completed successfully!")
        print("The scraper now extracts school IDs, modality IDs, and program IDs!")
    else:
        print("\n💥 Enhanced scraper test failed!")
        print("Please check the implementation and try again.")
    
    print("\nNext steps:")
    print("1. If test successful, run the full scraper on all municipalities")
    print("2. The enhanced data will include:")
    print("   - school_id: Ministry-assigned school identifier")
    print("   - modality_ids: Educational modality identifiers")
    print("   - program_ids: Educational program identifiers")
    print("3. These IDs can be used for linking with other MINED databases")
