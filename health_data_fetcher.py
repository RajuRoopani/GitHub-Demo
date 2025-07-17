#!/usr/bin/env python3
"""
Health Data Fetcher by Country

This script fetches health data for specific countries using various global health APIs.
It provides access to COVID-19 data, general health indicators, and demographic information.

APIs Used:
- Disease.sh API for COVID-19 data
- REST Countries API for country information
- World Bank API for health indicators (optional)

Author: Health Data Fetcher
License: MIT
"""

import requests
import json
import argparse
import sys
from typing import Dict, Any, Optional, List
from datetime import datetime


class HealthDataFetcher:
    """
    A class to fetch health data for different countries using various APIs.
    """
    
    def __init__(self, demo_mode: bool = False):
        self.demo_mode = demo_mode
        self.base_urls = {
            'disease_sh': 'https://disease.sh/v3/covid-19',
            'rest_countries': 'https://restcountries.com/v3.1',
            'worldbank': 'https://api.worldbank.org/v2/country'
        }
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Health-Data-Fetcher/1.0'
        })
        
        # Sample data for demo mode
        self.sample_data = {
            'usa': {
                'covid': {
                    'country': 'USA',
                    'countryInfo': {'iso2': 'US'},
                    'population': 331002651,
                    'updated': 1705315800000,
                    'cases': 103436829,
                    'deaths': 1127152,
                    'recovered': 100781036,
                    'active': 1528641,
                    'casesPerOneMillion': 312045,
                    'deathsPerOneMillion': 3402,
                    'testsPerOneMillion': 2735000,
                    'critical': 1500
                },
                'country_info': {
                    'region': 'Americas',
                    'subregion': 'Northern America',
                    'capital': ['Washington, D.C.'],
                    'languages': {'eng': 'English'}
                }
            },
            'germany': {
                'covid': {
                    'country': 'Germany',
                    'countryInfo': {'iso2': 'DE'},
                    'population': 83783942,
                    'updated': 1705315800000,
                    'cases': 38437756,
                    'deaths': 174979,
                    'recovered': 37800000,
                    'active': 462777,
                    'casesPerOneMillion': 458745,
                    'deathsPerOneMillion': 2088,
                    'testsPerOneMillion': 1450000,
                    'critical': 1200
                },
                'country_info': {
                    'region': 'Europe',
                    'subregion': 'Western Europe',
                    'capital': ['Berlin'],
                    'languages': {'deu': 'German'}
                }
            },
            'india': {
                'covid': {
                    'country': 'India',
                    'countryInfo': {'iso2': 'IN'},
                    'population': 1380004385,
                    'updated': 1705315800000,
                    'cases': 45035179,
                    'deaths': 533625,
                    'recovered': 44463473,
                    'active': 38081,
                    'casesPerOneMillion': 32634,
                    'deathsPerOneMillion': 387,
                    'testsPerOneMillion': 580000,
                    'critical': 800
                },
                'country_info': {
                    'region': 'Asia',
                    'subregion': 'Southern Asia',
                    'capital': ['New Delhi'],
                    'languages': {'hin': 'Hindi', 'eng': 'English'}
                }
            }
        }
    
    def validate_country_code(self, country: str) -> bool:
        """
        Validate if the country code/name exists by trying to fetch COVID data.
        
        Args:
            country (str): Country name or ISO code
            
        Returns:
            bool: True if valid, False otherwise
        """
        try:
            # Try to validate using COVID API first as it's more reliable
            url = f"{self.base_urls['disease_sh']}/countries/{country}"
            response = self.session.get(url, timeout=10)
            if response.status_code == 200:
                return True
            
            # Fallback to REST Countries API
            url = f"{self.base_urls['rest_countries']}/name/{country}"
            response = self.session.get(url, timeout=10)
            return response.status_code == 200
        except requests.RequestException:
            return False
    
    def get_covid_data(self, country: str) -> Optional[Dict[str, Any]]:
        """
        Fetch COVID-19 data for a specific country.
        
        Args:
            country (str): Country name or ISO code
            
        Returns:
            Optional[Dict[str, Any]]: COVID-19 data or None if error
        """
        if self.demo_mode:
            # Return sample data for demo mode
            country_lower = country.lower()
            if country_lower in self.sample_data:
                return self.sample_data[country_lower]['covid']
            else:
                print(f"Demo mode: Available countries are: {', '.join(self.sample_data.keys())}")
                return None
        
        try:
            url = f"{self.base_urls['disease_sh']}/countries/{country}"
            response = self.session.get(url, timeout=10)
            
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Error fetching COVID data: {response.status_code}")
                return None
                
        except requests.RequestException as e:
            print(f"Network error fetching COVID data: {e}")
            return None
    
    def get_country_info(self, country: str) -> Optional[Dict[str, Any]]:
        """
        Fetch general country information including health-related demographics.
        
        Args:
            country (str): Country name or ISO code
            
        Returns:
            Optional[Dict[str, Any]]: Country information or None if error
        """
        if self.demo_mode:
            # Return sample data for demo mode
            country_lower = country.lower()
            if country_lower in self.sample_data:
                return self.sample_data[country_lower]['country_info']
            else:
                return None
        
        try:
            url = f"{self.base_urls['rest_countries']}/name/{country}"
            response = self.session.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if data:
                    return data[0]  # Take first match
            else:
                print(f"Error fetching country info: {response.status_code}")
                return None
                
        except requests.RequestException as e:
            print(f"Network error fetching country info: {e}")
            return None
    
    def get_vaccination_data(self, country: str) -> Optional[Dict[str, Any]]:
        """
        Fetch vaccination data for a specific country.
        
        Args:
            country (str): Country name or ISO code
            
        Returns:
            Optional[Dict[str, Any]]: Vaccination data or None if error
        """
        try:
            url = f"{self.base_urls['disease_sh']}/vaccine/coverage/countries/{country}"
            response = self.session.get(url, timeout=10)
            
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Error fetching vaccination data: {response.status_code}")
                return None
                
        except requests.RequestException as e:
            print(f"Network error fetching vaccination data: {e}")
            return None
    
    def format_health_data(self, covid_data: Dict[str, Any], 
                          country_info: Dict[str, Any],
                          vaccination_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Format and combine health data from multiple sources.
        
        Args:
            covid_data (Dict[str, Any]): COVID-19 data
            country_info (Dict[str, Any]): Country information
            vaccination_data (Optional[Dict[str, Any]]): Vaccination data
            
        Returns:
            Dict[str, Any]: Formatted health data
        """
        formatted_data = {
            'country': covid_data.get('country', 'Unknown'),
            'country_code': covid_data.get('countryInfo', {}).get('iso2', 'Unknown'),
            'population': covid_data.get('population', 0),
            'updated': datetime.fromtimestamp(covid_data.get('updated', 0) / 1000).isoformat(),
            'covid_statistics': {
                'total_cases': covid_data.get('cases', 0),
                'total_deaths': covid_data.get('deaths', 0),
                'total_recovered': covid_data.get('recovered', 0),
                'active_cases': covid_data.get('active', 0),
                'cases_per_million': covid_data.get('casesPerOneMillion', 0),
                'deaths_per_million': covid_data.get('deathsPerOneMillion', 0),
                'tests_per_million': covid_data.get('testsPerOneMillion', 0),
                'critical_cases': covid_data.get('critical', 0)
            },
            'demographics': {
                'region': country_info.get('region', 'Unknown'),
                'subregion': country_info.get('subregion', 'Unknown'),
                'capital': country_info.get('capital', ['Unknown'])[0] if country_info.get('capital') else 'Unknown',
                'languages': list(country_info.get('languages', {}).values()) if country_info.get('languages') else []
            }
        }
        
        # Add vaccination data if available
        if vaccination_data and isinstance(vaccination_data, dict):
            formatted_data['vaccination'] = {
                'total_vaccinations': vaccination_data.get('timeline', {}).get('total', 0),
                'people_vaccinated': vaccination_data.get('timeline', {}).get('people_vaccinated', 0),
                'people_fully_vaccinated': vaccination_data.get('timeline', {}).get('people_fully_vaccinated', 0)
            }
        
        return formatted_data
    
    def fetch_health_data(self, country: str, include_vaccination: bool = False) -> Optional[Dict[str, Any]]:
        """
        Fetch comprehensive health data for a country.
        
        Args:
            country (str): Country name or ISO code
            include_vaccination (bool): Whether to include vaccination data
            
        Returns:
            Optional[Dict[str, Any]]: Comprehensive health data or None if error
        """
        # Fetch COVID data first as it's more reliable for validation
        covid_data = self.get_covid_data(country)
        if not covid_data:
            print(f"Failed to fetch COVID data for {country}")
            return None
        
        # Fetch country info (less critical, provide defaults if fails)
        country_info = self.get_country_info(country)
        if not country_info:
            print(f"Warning: Could not fetch detailed country info for {country}")
            # Create minimal country info from COVID data
            country_info = {
                'region': 'Unknown',
                'subregion': 'Unknown',
                'capital': ['Unknown'],
                'languages': {}
            }
        
        # Fetch vaccination data if requested
        vaccination_data = None
        if include_vaccination:
            vaccination_data = self.get_vaccination_data(country)
            if not vaccination_data:
                print(f"Warning: Could not fetch vaccination data for {country}")
        
        # Format and return data
        return self.format_health_data(covid_data, country_info, vaccination_data)


def print_health_data(data: Dict[str, Any], verbose: bool = False):
    """
    Print formatted health data to console.
    
    Args:
        data (Dict[str, Any]): Health data to print
        verbose (bool): Whether to print detailed information
    """
    print(f"\n=== Health Data for {data['country']} ===")
    print(f"Country Code: {data['country_code']}")
    print(f"Population: {data['population']:,}")
    print(f"Region: {data['demographics']['region']} ({data['demographics']['subregion']})")
    print(f"Capital: {data['demographics']['capital']}")
    print(f"Last Updated: {data['updated']}")
    
    print(f"\n--- COVID-19 Statistics ---")
    covid = data['covid_statistics']
    print(f"Total Cases: {covid['total_cases']:,}")
    print(f"Total Deaths: {covid['total_deaths']:,}")
    print(f"Total Recovered: {covid['total_recovered']:,}")
    print(f"Active Cases: {covid['active_cases']:,}")
    print(f"Cases per Million: {covid['cases_per_million']:,}")
    print(f"Deaths per Million: {covid['deaths_per_million']:,}")
    
    if verbose:
        print(f"Tests per Million: {covid['tests_per_million']:,}")
        print(f"Critical Cases: {covid['critical_cases']:,}")
        print(f"Languages: {', '.join(data['demographics']['languages'])}")
    
    if 'vaccination' in data:
        print(f"\n--- Vaccination Data ---")
        vacc = data['vaccination']
        print(f"Total Vaccinations: {vacc['total_vaccinations']:,}")
        print(f"People Vaccinated: {vacc['people_vaccinated']:,}")
        print(f"Fully Vaccinated: {vacc['people_fully_vaccinated']:,}")


def main():
    """
    Main function to handle command line arguments and execute the script.
    """
    parser = argparse.ArgumentParser(
        description='Fetch health data for specific countries',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python health_data_fetcher.py usa
  python health_data_fetcher.py "United States" --verbose
  python health_data_fetcher.py germany --vaccination --json
  python health_data_fetcher.py india --output health_data.json
        """
    )
    
    parser.add_argument('country', help='Country name or ISO code')
    parser.add_argument('--demo', action='store_true',
                       help='Use demo mode with sample data (useful for testing)')
    parser.add_argument('--vaccination', action='store_true', 
                       help='Include vaccination data')
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='Show detailed information')
    parser.add_argument('--json', action='store_true',
                       help='Output data in JSON format')
    parser.add_argument('--output', '-o', help='Output file path')
    
    args = parser.parse_args()
    
    # Create fetcher instance
    fetcher = HealthDataFetcher(demo_mode=args.demo)
    
    # Fetch data
    if args.demo:
        print(f"Fetching health data for {args.country} (Demo Mode)...")
    else:
        print(f"Fetching health data for {args.country}...")
    data = fetcher.fetch_health_data(args.country, args.vaccination)
    
    if not data:
        print("Failed to fetch health data")
        sys.exit(1)
    
    # Output data
    if args.json:
        json_output = json.dumps(data, indent=2)
        if args.output:
            with open(args.output, 'w') as f:
                f.write(json_output)
            print(f"Data saved to {args.output}")
        else:
            print(json_output)
    else:
        print_health_data(data, args.verbose)
        
        if args.output:
            with open(args.output, 'w') as f:
                json.dump(data, f, indent=2)
            print(f"\nData also saved to {args.output}")


if __name__ == "__main__":
    main()