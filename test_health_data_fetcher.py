#!/usr/bin/env python3
"""
Simple tests for the Health Data Fetcher

This script provides basic tests to verify the functionality works correctly.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from health_data_fetcher import HealthDataFetcher

def test_demo_mode():
    """Test demo mode functionality"""
    print("Testing demo mode...")
    
    fetcher = HealthDataFetcher(demo_mode=True)
    
    # Test valid countries
    valid_countries = ['usa', 'germany', 'india']
    for country in valid_countries:
        data = fetcher.fetch_health_data(country)
        assert data is not None, f"Failed to fetch data for {country}"
        assert data['country'], f"No country name returned for {country}"
        assert data['population'] > 0, f"Invalid population for {country}"
        assert 'covid_statistics' in data, f"No COVID statistics for {country}"
        print(f"✓ {country} data fetched successfully")
    
    # Test invalid country
    invalid_data = fetcher.fetch_health_data('invalidcountry')
    assert invalid_data is None, "Should return None for invalid country"
    print("✓ Invalid country handled correctly")
    
    print("Demo mode tests passed!\n")

def test_data_structure():
    """Test the structure of returned data"""
    print("Testing data structure...")
    
    fetcher = HealthDataFetcher(demo_mode=True)
    data = fetcher.fetch_health_data('usa')
    
    # Check required fields
    required_fields = ['country', 'country_code', 'population', 'updated', 'covid_statistics', 'demographics']
    for field in required_fields:
        assert field in data, f"Missing required field: {field}"
    
    # Check COVID statistics structure
    covid_fields = ['total_cases', 'total_deaths', 'total_recovered', 'active_cases', 'cases_per_million', 'deaths_per_million']
    for field in covid_fields:
        assert field in data['covid_statistics'], f"Missing COVID field: {field}"
    
    # Check demographics structure
    demo_fields = ['region', 'subregion', 'capital', 'languages']
    for field in demo_fields:
        assert field in data['demographics'], f"Missing demographic field: {field}"
    
    print("✓ Data structure is correct")
    print("Data structure tests passed!\n")

def test_formatting():
    """Test data formatting functions"""
    print("Testing data formatting...")
    
    fetcher = HealthDataFetcher(demo_mode=True)
    
    # Test with sample data
    covid_data = {
        'country': 'Test Country',
        'countryInfo': {'iso2': 'TC'},
        'population': 1000000,
        'updated': 1705315800000,
        'cases': 100000,
        'deaths': 1000,
        'recovered': 95000,
        'active': 4000,
        'casesPerOneMillion': 100000,
        'deathsPerOneMillion': 1000,
        'testsPerOneMillion': 500000,
        'critical': 100
    }
    
    country_info = {
        'region': 'Test Region',
        'subregion': 'Test Subregion',
        'capital': ['Test Capital'],
        'languages': {'test': 'Test Language'}
    }
    
    formatted_data = fetcher.format_health_data(covid_data, country_info)
    
    assert formatted_data['country'] == 'Test Country'
    assert formatted_data['population'] == 1000000
    assert formatted_data['covid_statistics']['total_cases'] == 100000
    assert formatted_data['demographics']['region'] == 'Test Region'
    
    print("✓ Data formatting works correctly")
    print("Formatting tests passed!\n")

def main():
    """Run all tests"""
    print("=== Health Data Fetcher Tests ===\n")
    
    try:
        test_demo_mode()
        test_data_structure()
        test_formatting()
        
        print("🎉 All tests passed!")
        return 0
        
    except AssertionError as e:
        print(f"❌ Test failed: {e}")
        return 1
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())