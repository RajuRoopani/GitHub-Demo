#!/usr/bin/env python3
"""
Test script for health_data_fetcher.py with sample data.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from health_data_fetcher import HealthDataFetcher

def test_country_code_lookup():
    """Test the country code lookup functionality."""
    print("Testing country code lookup...")
    
    fetcher = HealthDataFetcher()
    
    test_cases = [
        ("United States", "US"),
        ("usa", "US"),
        ("India", "IN"),
        ("Germany", "DE"),
        ("United Kingdom", "GB"),
        ("Japan", "JP"),
        ("Canada", "CA"),
        ("Australia", "AU"),
        ("France", "FR"),
        ("Brazil", "BR")
    ]
    
    for country_name, expected_code in test_cases:
        code = fetcher.get_country_code(country_name)
        status = "✓" if code == expected_code else "✗"
        print(f"{status} {country_name} -> {code} (expected: {expected_code})")
    
    print()

def test_data_formatting():
    """Test the data formatting functionality with sample data."""
    print("Testing data formatting with sample data...")
    
    fetcher = HealthDataFetcher()
    
    # Sample World Bank data
    sample_wb_data = {
        'Life Expectancy at Birth': {
            'value': 76.4,
            'year': '2021',
            'country': 'United States'
        },
        'Mortality Rate, Under-5': {
            'value': 6.5,
            'year': '2021',
            'country': 'United States'
        },
        'Maternal Mortality Ratio': {
            'value': 23.8,
            'year': '2020',
            'country': 'United States'
        },
        'Current Health Expenditure (% of GDP)': {
            'value': 17.83,
            'year': '2020',
            'country': 'United States'
        },
        'Total Population': {
            'value': 331893745,
            'year': '2021',
            'country': 'United States'
        }
    }
    
    # Sample WHO data
    sample_who_data = {
        'Life Expectancy at Birth': {
            'value': 76.4,
            'year': '2021',
            'country': 'US'
        },
        'Adult Mortality Rate': {
            'value': 140.2,
            'year': '2021',
            'country': 'US'
        },
        'Under-five Mortality Rate': {
            'value': 6.5,
            'year': '2021',
            'country': 'US'
        }
    }
    
    formatted_data = fetcher.format_health_data("United States", sample_wb_data, sample_who_data)
    print(formatted_data)
    
    # Test with empty data
    print("\n" + "="*50)
    print("Testing with no data available:")
    empty_formatted = fetcher.format_health_data("Unknown Country", {}, {})
    print(empty_formatted)

def create_sample_data_demo():
    """Create a demo with sample data for different countries."""
    print("Creating sample data demo...")
    
    fetcher = HealthDataFetcher()
    
    # Sample data for different countries
    sample_data = {
        'United States': {
            'wb_data': {
                'Life Expectancy at Birth': {'value': 76.4, 'year': '2021', 'country': 'United States'},
                'Mortality Rate, Under-5': {'value': 6.5, 'year': '2021', 'country': 'United States'},
                'Maternal Mortality Ratio': {'value': 23.8, 'year': '2020', 'country': 'United States'},
                'Current Health Expenditure (% of GDP)': {'value': 17.83, 'year': '2020', 'country': 'United States'},
                'Total Population': {'value': 331893745, 'year': '2021', 'country': 'United States'}
            },
            'who_data': {
                'Life Expectancy at Birth': {'value': 76.4, 'year': '2021', 'country': 'US'},
                'Adult Mortality Rate': {'value': 140.2, 'year': '2021', 'country': 'US'}
            }
        },
        'India': {
            'wb_data': {
                'Life Expectancy at Birth': {'value': 67.2, 'year': '2021', 'country': 'India'},
                'Mortality Rate, Under-5': {'value': 31.8, 'year': '2021', 'country': 'India'},
                'Maternal Mortality Ratio': {'value': 103.0, 'year': '2020', 'country': 'India'},
                'Current Health Expenditure (% of GDP)': {'value': 3.01, 'year': '2020', 'country': 'India'},
                'Total Population': {'value': 1380004385, 'year': '2021', 'country': 'India'}
            },
            'who_data': {
                'Life Expectancy at Birth': {'value': 67.2, 'year': '2021', 'country': 'IN'},
                'Adult Mortality Rate': {'value': 197.5, 'year': '2021', 'country': 'IN'}
            }
        },
        'Germany': {
            'wb_data': {
                'Life Expectancy at Birth': {'value': 80.6, 'year': '2021', 'country': 'Germany'},
                'Mortality Rate, Under-5': {'value': 4.1, 'year': '2021', 'country': 'Germany'},
                'Maternal Mortality Ratio': {'value': 4.0, 'year': '2020', 'country': 'Germany'},
                'Current Health Expenditure (% of GDP)': {'value': 12.8, 'year': '2020', 'country': 'Germany'},
                'Total Population': {'value': 83240525, 'year': '2021', 'country': 'Germany'}
            },
            'who_data': {
                'Life Expectancy at Birth': {'value': 80.6, 'year': '2021', 'country': 'DE'},
                'Adult Mortality Rate': {'value': 95.1, 'year': '2021', 'country': 'DE'}
            }
        }
    }
    
    for country_name, data in sample_data.items():
        formatted = fetcher.format_health_data(country_name, data['wb_data'], data['who_data'])
        print(formatted)
        print("\n" + "="*80 + "\n")

def main():
    """Run all tests."""
    print("Health Data Fetcher - Test Suite")
    print("="*50)
    
    test_country_code_lookup()
    test_data_formatting()
    
    print("\n" + "="*80)
    print("SAMPLE DATA DEMO")
    print("="*80)
    create_sample_data_demo()

if __name__ == "__main__":
    main()