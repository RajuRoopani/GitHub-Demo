#!/usr/bin/env python3
"""
Health Data Fetcher
===================

A Python script that fetches health data for specific countries using various APIs.
Supports World Bank Health Data API and WHO Global Health Observatory API.

Usage:
    python health_data_fetcher.py <country_name>
    
Example:
    python health_data_fetcher.py "United States"
    python health_data_fetcher.py "India"
"""

import requests
import json
import sys
import argparse
from typing import Dict, List, Optional
from datetime import datetime


class HealthDataFetcher:
    """
    A class to fetch health data for countries from various APIs.
    """
    
    def __init__(self):
        self.world_bank_base_url = "https://api.worldbank.org/v2/country"
        self.who_base_url = "https://ghoapi.azureedge.net/api"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Health-Data-Fetcher/1.0'
        })
        
        # Common country name to ISO code mappings (fallback)
        self.country_codes = {
            'united states': 'US',
            'usa': 'US',
            'america': 'US',
            'united kingdom': 'GB',
            'uk': 'GB',
            'britain': 'GB',
            'india': 'IN',
            'china': 'CN',
            'japan': 'JP',
            'germany': 'DE',
            'france': 'FR',
            'italy': 'IT',
            'spain': 'ES',
            'canada': 'CA',
            'australia': 'AU',
            'brazil': 'BR',
            'russia': 'RU',
            'south korea': 'KR',
            'korea': 'KR',
            'mexico': 'MX',
            'indonesia': 'ID',
            'turkey': 'TR',
            'saudi arabia': 'SA',
            'argentina': 'AR',
            'south africa': 'ZA',
            'nigeria': 'NG',
            'egypt': 'EG',
            'thailand': 'TH',
            'vietnam': 'VN',
            'bangladesh': 'BD',
            'pakistan': 'PK',
            'philippines': 'PH',
            'malaysia': 'MY',
            'singapore': 'SG',
            'netherlands': 'NL',
            'belgium': 'BE',
            'sweden': 'SE',
            'norway': 'NO',
            'denmark': 'DK',
            'finland': 'FI',
            'poland': 'PL',
            'czech republic': 'CZ',
            'austria': 'AT',
            'switzerland': 'CH',
            'greece': 'GR',
            'portugal': 'PT',
            'israel': 'IL',
            'new zealand': 'NZ',
            'chile': 'CL',
            'peru': 'PE',
            'colombia': 'CO',
            'venezuela': 'VE',
            'ukraine': 'UA',
            'romania': 'RO',
            'hungary': 'HU',
            'belarus': 'BY',
            'bulgaria': 'BG',
            'croatia': 'HR',
            'serbia': 'RS',
            'slovenia': 'SI',
            'slovakia': 'SK',
            'lithuania': 'LT',
            'latvia': 'LV',
            'estonia': 'EE',
            'ireland': 'IE',
            'luxembourg': 'LU',
            'cyprus': 'CY',
            'malta': 'MT',
            'iceland': 'IS'
        }
    
    def get_country_code(self, country_name: str) -> Optional[str]:
        """
        Get the ISO country code for a given country name.
        
        Args:
            country_name: Name of the country
            
        Returns:
            ISO country code or None if not found
        """
        # First check our local mapping
        country_lower = country_name.lower().strip()
        if country_lower in self.country_codes:
            return self.country_codes[country_lower]
        
        # Try to get from REST Countries API as fallback
        try:
            response = self.session.get(
                f"https://restcountries.com/v3.1/name/{country_name}",
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                if data and len(data) > 0:
                    return data[0].get('cca2', '').upper()
            
        except Exception as e:
            print(f"Note: Could not connect to REST Countries API: {e}")
            print("Using fallback country code mapping...")
        
        # Check if it might be a country code already
        if len(country_name) == 2 and country_name.isalpha():
            return country_name.upper()
        
        return None
    
    def get_demo_data(self, country_name: str) -> tuple:
        """
        Get sample health data for demo purposes.
        
        Args:
            country_name: Name of the country
            
        Returns:
            Tuple of (wb_data, who_data) with sample data
        """
        # Sample data for different countries
        sample_data = {
            'united states': {
                'wb_data': {
                    'Life Expectancy at Birth': {'value': 76.4, 'year': '2021', 'country': 'United States'},
                    'Mortality Rate, Under-5': {'value': 6.5, 'year': '2021', 'country': 'United States'},
                    'Maternal Mortality Ratio': {'value': 23.8, 'year': '2020', 'country': 'United States'},
                    'Current Health Expenditure (% of GDP)': {'value': 17.83, 'year': '2020', 'country': 'United States'},
                    'Total Population': {'value': 331893745, 'year': '2021', 'country': 'United States'}
                },
                'who_data': {
                    'Life Expectancy at Birth': {'value': 76.4, 'year': '2021', 'country': 'US'},
                    'Adult Mortality Rate': {'value': 140.2, 'year': '2021', 'country': 'US'},
                    'Under-five Mortality Rate': {'value': 6.5, 'year': '2021', 'country': 'US'}
                }
            },
            'india': {
                'wb_data': {
                    'Life Expectancy at Birth': {'value': 67.2, 'year': '2021', 'country': 'India'},
                    'Mortality Rate, Under-5': {'value': 31.8, 'year': '2021', 'country': 'India'},
                    'Maternal Mortality Ratio': {'value': 103.0, 'year': '2020', 'country': 'India'},
                    'Current Health Expenditure (% of GDP)': {'value': 3.01, 'year': '2020', 'country': 'India'},
                    'Total Population': {'value': 1380004385, 'year': '2021', 'country': 'India'}
                },
                'who_data': {
                    'Life Expectancy at Birth': {'value': 67.2, 'year': '2021', 'country': 'IN'},
                    'Adult Mortality Rate': {'value': 197.5, 'year': '2021', 'country': 'IN'},
                    'Under-five Mortality Rate': {'value': 31.8, 'year': '2021', 'country': 'IN'}
                }
            },
            'germany': {
                'wb_data': {
                    'Life Expectancy at Birth': {'value': 80.6, 'year': '2021', 'country': 'Germany'},
                    'Mortality Rate, Under-5': {'value': 4.1, 'year': '2021', 'country': 'Germany'},
                    'Maternal Mortality Ratio': {'value': 4.0, 'year': '2020', 'country': 'Germany'},
                    'Current Health Expenditure (% of GDP)': {'value': 12.8, 'year': '2020', 'country': 'Germany'},
                    'Total Population': {'value': 83240525, 'year': '2021', 'country': 'Germany'}
                },
                'who_data': {
                    'Life Expectancy at Birth': {'value': 80.6, 'year': '2021', 'country': 'DE'},
                    'Adult Mortality Rate': {'value': 95.1, 'year': '2021', 'country': 'DE'},
                    'Under-five Mortality Rate': {'value': 4.1, 'year': '2021', 'country': 'DE'}
                }
            },
            'japan': {
                'wb_data': {
                    'Life Expectancy at Birth': {'value': 84.4, 'year': '2021', 'country': 'Japan'},
                    'Mortality Rate, Under-5': {'value': 2.5, 'year': '2021', 'country': 'Japan'},
                    'Maternal Mortality Ratio': {'value': 4.0, 'year': '2020', 'country': 'Japan'},
                    'Current Health Expenditure (% of GDP)': {'value': 11.0, 'year': '2020', 'country': 'Japan'},
                    'Total Population': {'value': 125681593, 'year': '2021', 'country': 'Japan'}
                },
                'who_data': {
                    'Life Expectancy at Birth': {'value': 84.4, 'year': '2021', 'country': 'JP'},
                    'Adult Mortality Rate': {'value': 63.5, 'year': '2021', 'country': 'JP'},
                    'Under-five Mortality Rate': {'value': 2.5, 'year': '2021', 'country': 'JP'}
                }
            },
            'canada': {
                'wb_data': {
                    'Life Expectancy at Birth': {'value': 82.1, 'year': '2021', 'country': 'Canada'},
                    'Mortality Rate, Under-5': {'value': 4.9, 'year': '2021', 'country': 'Canada'},
                    'Maternal Mortality Ratio': {'value': 11.0, 'year': '2020', 'country': 'Canada'},
                    'Current Health Expenditure (% of GDP)': {'value': 12.9, 'year': '2020', 'country': 'Canada'},
                    'Total Population': {'value': 38067903, 'year': '2021', 'country': 'Canada'}
                },
                'who_data': {
                    'Life Expectancy at Birth': {'value': 82.1, 'year': '2021', 'country': 'CA'},
                    'Adult Mortality Rate': {'value': 82.3, 'year': '2021', 'country': 'CA'},
                    'Under-five Mortality Rate': {'value': 4.9, 'year': '2021', 'country': 'CA'}
                }
            }
        }
        
        country_lower = country_name.lower().strip()
        
        if country_lower in sample_data:
            data = sample_data[country_lower]
            return data['wb_data'], data['who_data']
        else:
            # Return generic sample data for unknown countries
            return {
                'Life Expectancy at Birth': {'value': 72.0, 'year': '2021', 'country': country_name},
                'Total Population': {'value': 50000000, 'year': '2021', 'country': country_name}
            }, {
                'Life Expectancy at Birth': {'value': 72.0, 'year': '2021', 'country': country_name}
            }
        """
        Fetch health data from World Bank API.
        
        Args:
            country_code: ISO country code
            
        Returns:
            Dictionary containing health indicators
        """
        health_indicators = {
            'SP.DYN.LE00.IN': 'Life Expectancy at Birth',
            'SH.DYN.MORT': 'Mortality Rate, Under-5',
            'SH.STA.MMRT': 'Maternal Mortality Ratio',
            'SH.XPD.CHEX.GD.ZS': 'Current Health Expenditure (% of GDP)',
            'SP.POP.TOTL': 'Total Population'
        }
        
        health_data = {}
        
        for indicator_code, indicator_name in health_indicators.items():
            try:
                url = f"{self.world_bank_base_url}/{country_code}/indicator/{indicator_code}"
                params = {
                    'format': 'json',
                    'date': '2015:2023',  # Last few years
                    'per_page': '10'
                }
                
                response = self.session.get(url, params=params, timeout=10)
                
                if response.status_code == 200:
                    data = response.json()
                    
                    if len(data) > 1 and data[1]:
                        # Get the most recent data point
                        recent_data = data[1][0] if data[1] else None
                        
                        if recent_data and recent_data.get('value'):
                            health_data[indicator_name] = {
                                'value': recent_data['value'],
                                'year': recent_data['date'],
                                'country': recent_data['country']['value']
                            }
                
            except Exception as e:
                print(f"Error fetching {indicator_name}: {e}")
                continue
        
        return health_data
    
    def fetch_who_health_data(self, country_code: str) -> Dict:
        """
        Fetch additional health data from WHO Global Health Observatory API.
        
        Args:
            country_code: ISO country code
            
        Returns:
            Dictionary containing WHO health indicators
        """
        who_indicators = {
            'WHOSIS_000001': 'Life Expectancy at Birth',
            'WHOSIS_000015': 'Adult Mortality Rate',
            'MDG_0000000001': 'Under-five Mortality Rate'
        }
        
        who_data = {}
        
        for indicator_code, indicator_name in who_indicators.items():
            try:
                url = f"{self.who_base_url}/{indicator_code}"
                params = {
                    'format': 'json',
                    '$filter': f"SpatialDim eq '{country_code}'"
                }
                
                response = self.session.get(url, params=params, timeout=10)
                
                if response.status_code == 200:
                    data = response.json()
                    
                    if data and 'value' in data:
                        values = data['value']
                        if values:
                            # Get the most recent data
                            recent_data = max(values, key=lambda x: x.get('TimeDim', 0))
                            
                            who_data[indicator_name] = {
                                'value': recent_data.get('NumericValue'),
                                'year': recent_data.get('TimeDim'),
                                'country': recent_data.get('SpatialDim')
                            }
                
            except Exception as e:
                print(f"Error fetching WHO {indicator_name}: {e}")
                continue
        
        return who_data
    
    def format_health_data(self, country_name: str, wb_data: Dict, who_data: Dict) -> str:
        """
        Format the health data into a readable string.
        
        Args:
            country_name: Name of the country
            wb_data: World Bank health data
            who_data: WHO health data
            
        Returns:
            Formatted health data string
        """
        output = []
        output.append(f"\n{'='*60}")
        output.append(f"HEALTH DATA FOR {country_name.upper()}")
        output.append(f"{'='*60}")
        output.append(f"Report generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        output.append("")
        
        if wb_data:
            output.append("WORLD BANK HEALTH INDICATORS:")
            output.append("-" * 40)
            
            for indicator, data in wb_data.items():
                value = data['value']
                year = data['year']
                
                # Format numeric values appropriately
                if isinstance(value, (int, float)):
                    if indicator == 'Total Population':
                        formatted_value = f"{value:,.0f}"
                    elif 'Rate' in indicator or 'Ratio' in indicator:
                        formatted_value = f"{value:.1f}"
                    elif 'Expenditure' in indicator:
                        formatted_value = f"{value:.2f}%"
                    else:
                        formatted_value = f"{value:.1f}"
                else:
                    formatted_value = str(value)
                
                output.append(f"• {indicator}: {formatted_value} ({year})")
            
            output.append("")
        
        if who_data:
            output.append("WHO HEALTH INDICATORS:")
            output.append("-" * 40)
            
            for indicator, data in who_data.items():
                value = data['value']
                year = data['year']
                
                if value is not None:
                    formatted_value = f"{value:.1f}" if isinstance(value, (int, float)) else str(value)
                    output.append(f"• {indicator}: {formatted_value} ({year})")
            
            output.append("")
        
        if not wb_data and not who_data:
            output.append("No health data available for this country.")
            output.append("Please check the country name and try again.")
        
        output.append("=" * 60)
        
        return "\n".join(output)
    
    def fetch_health_data(self, country_name: str, demo_mode: bool = False) -> str:
        """
        Main method to fetch and format health data for a country.
        
        Args:
            country_name: Name of the country
            demo_mode: If True, use sample data instead of API calls
            
        Returns:
            Formatted health data string
        """
        print(f"Fetching health data for {country_name}...")
        
        if demo_mode:
            print("Running in demo mode with sample data...")
            wb_data, who_data = self.get_demo_data(country_name)
            return self.format_health_data(country_name, wb_data, who_data)
        
        # Get country code
        country_code = self.get_country_code(country_name)
        
        if not country_code:
            return f"Error: Could not find country code for '{country_name}'. Please check the spelling."
        
        print(f"Country code: {country_code}")
        
        # Fetch data from both APIs
        print("Fetching World Bank data...")
        wb_data = self.fetch_world_bank_health_data(country_code)
        
        print("Fetching WHO data...")
        who_data = self.fetch_who_health_data(country_code)
        
        # Format and return the data
        return self.format_health_data(country_name, wb_data, who_data)


def main():
    """
    Main function to run the health data fetcher.
    """
    parser = argparse.ArgumentParser(
        description="Fetch health data for a specific country",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python health_data_fetcher.py "United States"
  python health_data_fetcher.py "India"
  python health_data_fetcher.py "Germany"
  python health_data_fetcher.py "Japan" --demo
        """
    )
    
    parser.add_argument(
        'country',
        help='Name of the country to fetch health data for'
    )
    
    parser.add_argument(
        '--output',
        '-o',
        help='Output file to save the health data (optional)'
    )
    
    parser.add_argument(
        '--demo',
        action='store_true',
        help='Run in demo mode with sample data (useful when APIs are not accessible)'
    )
    
    args = parser.parse_args()
    
    # Create fetcher instance
    fetcher = HealthDataFetcher()
    
    try:
        # Fetch health data
        result = fetcher.fetch_health_data(args.country, demo_mode=args.demo)
        
        # Print the result
        print(result)
        
        # Save to file if requested
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(result)
            print(f"\nHealth data saved to {args.output}")
        
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()