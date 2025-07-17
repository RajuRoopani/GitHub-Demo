#!/usr/bin/env python3
"""
Example usage of the Health Data Fetcher

This script demonstrates how to use the HealthDataFetcher class programmatically.
"""

from health_data_fetcher import HealthDataFetcher, print_health_data
import json

def main():
    """
    Demonstrate various ways to use the Health Data Fetcher
    """
    print("=== Health Data Fetcher Example ===\n")
    
    # Create fetcher instance with demo mode
    fetcher = HealthDataFetcher(demo_mode=True)
    
    countries = ['usa', 'germany', 'india']
    
    for country in countries:
        print(f"Fetching data for {country.upper()}...")
        
        # Fetch basic health data
        data = fetcher.fetch_health_data(country)
        
        if data:
            # Print formatted data
            print_health_data(data)
            
            # Save to file
            filename = f"{country}_health_data.json"
            with open(filename, 'w') as f:
                json.dump(data, f, indent=2)
            print(f"Data saved to {filename}")
        else:
            print(f"Failed to fetch data for {country}")
        
        print("-" * 50)

if __name__ == "__main__":
    main()