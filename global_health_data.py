#!/usr/bin/env python3
"""
Global Health Data Fetcher

This script fetches global health data by country using the World Bank API.
It provides various health indicators such as life expectancy, infant mortality rate,
health expenditure, and other key health statistics.

Usage:
    python global_health_data.py [country_code]

Example:
    python global_health_data.py US
    python global_health_data.py BR
    python global_health_data.py IN
"""

import requests
import json
import sys
from typing import Dict, List, Optional, Any
import argparse
from datetime import datetime


class GlobalHealthDataFetcher:
    """
    A class to fetch global health data from the World Bank API.
    """
    
    def __init__(self):
        self.base_url = "https://api.worldbank.org/v2"
        self.format = "json"
        
        # Common health indicators from World Bank
        self.health_indicators = {
            "SP.DYN.LE00.IN": "Life expectancy at birth, total (years)",
            "SP.DYN.IMRT.IN": "Mortality rate, infant (per 1,000 live births)",
            "SH.XPD.CHEX.PC.CD": "Current health expenditure per capita (current US$)",
            "SH.XPD.CHEX.GD.ZS": "Current health expenditure (% of GDP)",
            "SP.DYN.CDRT.IN": "Death rate, crude (per 1,000 people)",
            "SP.DYN.CBRT.IN": "Birth rate, crude (per 1,000 people)",
            "SH.STA.MMRT": "Maternal mortality ratio (per 100,000 live births)",
            "SH.DTH.MORT": "Mortality rate, under-5 (per 1,000 live births)",
            "SP.DYN.LE00.MA.IN": "Life expectancy at birth, male (years)",
            "SP.DYN.LE00.FE.IN": "Life expectancy at birth, female (years)"
        }
    
    def get_country_info(self, country_code: str) -> Optional[Dict[str, Any]]:
        """
        Get basic country information.
        
        Args:
            country_code: ISO 3166-1 alpha-2 country code (e.g., 'US', 'BR', 'IN')
            
        Returns:
            Dictionary containing country information or None if not found
        """
        try:
            url = f"{self.base_url}/countries/{country_code}?format={self.format}"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            if len(data) > 1 and data[1]:
                country_info = data[1][0]
                return {
                    "name": country_info.get("name", "Unknown"),
                    "code": country_info.get("iso2Code", country_code),
                    "capital": country_info.get("capitalCity", "Unknown"),
                    "region": country_info.get("region", {}).get("value", "Unknown"),
                    "income_level": country_info.get("incomeLevel", {}).get("value", "Unknown")
                }
        except (requests.RequestException, KeyError, IndexError) as e:
            print(f"Error fetching country info: {e}")
            return None
    
    def get_health_indicator(self, country_code: str, indicator_code: str, 
                           years: int = 5) -> List[Dict[str, Any]]:
        """
        Get health indicator data for a specific country.
        
        Args:
            country_code: ISO 3166-1 alpha-2 country code
            indicator_code: World Bank indicator code
            years: Number of most recent years to fetch
            
        Returns:
            List of dictionaries containing indicator data
        """
        try:
            url = f"{self.base_url}/countries/{country_code}/indicators/{indicator_code}"
            params = {
                "format": self.format,
                "per_page": years,
                "date": f"{datetime.now().year - years}:{datetime.now().year}"
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            if len(data) > 1 and data[1]:
                results = []
                for item in data[1]:
                    if item.get("value") is not None:
                        results.append({
                            "year": item.get("date"),
                            "value": item.get("value"),
                            "indicator": self.health_indicators.get(indicator_code, indicator_code)
                        })
                return sorted(results, key=lambda x: x["year"], reverse=True)
        except (requests.RequestException, KeyError, IndexError) as e:
            print(f"Error fetching indicator {indicator_code}: {e}")
            return []
    
    def get_all_health_data(self, country_code: str) -> Dict[str, Any]:
        """
        Get comprehensive health data for a country.
        
        Args:
            country_code: ISO 3166-1 alpha-2 country code
            
        Returns:
            Dictionary containing all health indicators and country info
        """
        print(f"Fetching health data for country: {country_code}")
        
        # Get country information
        country_info = self.get_country_info(country_code)
        if not country_info:
            return {"error": f"Country '{country_code}' not found"}
        
        # Get health indicators
        health_data = {}
        for indicator_code, indicator_name in self.health_indicators.items():
            data = self.get_health_indicator(country_code, indicator_code)
            if data:
                health_data[indicator_name] = data
        
        return {
            "country_info": country_info,
            "health_indicators": health_data,
            "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    
    def format_output(self, data: Dict[str, Any]) -> str:
        """
        Format the health data for display.
        
        Args:
            data: Dictionary containing health data
            
        Returns:
            Formatted string for display
        """
        if "error" in data:
            return f"Error: {data['error']}"
        
        output = []
        country_info = data.get("country_info", {})
        
        # Country information
        output.append("=" * 60)
        output.append(f"GLOBAL HEALTH DATA FOR {country_info.get('name', 'Unknown').upper()}")
        output.append("=" * 60)
        output.append(f"Country Code: {country_info.get('code', 'Unknown')}")
        output.append(f"Capital: {country_info.get('capital', 'Unknown')}")
        output.append(f"Region: {country_info.get('region', 'Unknown')}")
        output.append(f"Income Level: {country_info.get('income_level', 'Unknown')}")
        output.append(f"Data Retrieved: {data.get('last_updated', 'Unknown')}")
        output.append("")
        
        # Health indicators
        health_indicators = data.get("health_indicators", {})
        for indicator_name, indicator_data in health_indicators.items():
            output.append(f"{indicator_name}:")
            if indicator_data:
                for item in indicator_data[:3]:  # Show last 3 years
                    value = item["value"]
                    if isinstance(value, float):
                        value = f"{value:.2f}"
                    output.append(f"  {item['year']}: {value}")
            else:
                output.append("  No data available")
            output.append("")
        
        return "\n".join(output)


def main():
    """
    Main function to run the global health data fetcher.
    """
    parser = argparse.ArgumentParser(
        description="Fetch global health data by country using World Bank API",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python global_health_data.py US          # Get data for United States
  python global_health_data.py BR          # Get data for Brazil
  python global_health_data.py IN          # Get data for India
  python global_health_data.py --list      # List common country codes
        """
    )
    
    parser.add_argument(
        "country_code",
        nargs="?",
        help="ISO 3166-1 alpha-2 country code (e.g., US, BR, IN, GB, DE)"
    )
    
    parser.add_argument(
        "--list",
        action="store_true",
        help="Show common country codes"
    )
    
    parser.add_argument(
        "--output",
        choices=["text", "json"],
        default="text",
        help="Output format (default: text)"
    )
    
    args = parser.parse_args()
    
    if args.list:
        print("Common Country Codes:")
        print("US - United States")
        print("CA - Canada")
        print("GB - United Kingdom")
        print("DE - Germany")
        print("FR - France")
        print("IT - Italy")
        print("ES - Spain")
        print("JP - Japan")
        print("CN - China")
        print("IN - India")
        print("BR - Brazil")
        print("AU - Australia")
        print("ZA - South Africa")
        print("NG - Nigeria")
        print("EG - Egypt")
        return
    
    if not args.country_code:
        parser.print_help()
        return
    
    # Validate country code format
    if len(args.country_code) != 2:
        print("Error: Country code must be 2 characters (ISO 3166-1 alpha-2)")
        print("Use --list to see common country codes")
        return
    
    # Fetch data
    fetcher = GlobalHealthDataFetcher()
    data = fetcher.get_all_health_data(args.country_code.upper())
    
    # Output results
    if args.output == "json":
        print(json.dumps(data, indent=2))
    else:
        print(fetcher.format_output(data))


if __name__ == "__main__":
    main()