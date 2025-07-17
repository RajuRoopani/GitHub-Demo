# Health Data Fetcher by Country

A Python script that fetches health data for specific countries using various global health APIs. This tool provides access to COVID-19 statistics, vaccination data, and general health-related demographic information.

## Features

- **COVID-19 Data**: Get real-time COVID-19 statistics including cases, deaths, recoveries, and testing data
- **Country Information**: Fetch demographic and geographic information relevant to health analysis
- **Vaccination Data**: Access vaccination statistics (optional)
- **Multiple Output Formats**: Display data in human-readable format or JSON
- **Error Handling**: Robust error handling with informative messages
- **CLI Interface**: Easy-to-use command line interface

## APIs Used

- **Disease.sh API**: For COVID-19 data and vaccination statistics
- **REST Countries API**: For country information and demographics
- **World Bank API**: For additional health indicators (future enhancement)

## Installation

1. Clone this repository:
```bash
git clone https://github.com/RajuRoopani/GitHub-Demo.git
cd GitHub-Demo
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage

```bash
python health_data_fetcher.py [country_name]
```

### Examples

**Test with demo data:**
```bash
python health_data_fetcher.py usa --demo
```

**Fetch basic health data for USA:**
```bash
python health_data_fetcher.py usa
```

**Fetch detailed data with vaccination information:**
```bash
python health_data_fetcher.py "United States" --vaccination --verbose
```

**Output data in JSON format:**
```bash
python health_data_fetcher.py germany --json
```

**Save data to file:**
```bash
python health_data_fetcher.py india --output health_data.json
```

**Get help:**
```bash
python health_data_fetcher.py --help
```

### Command Line Options

- `country`: Country name or ISO code (required)
- `--demo`: Use demo mode with sample data (useful for testing without internet)
- `--vaccination`: Include vaccination data in the output
- `--verbose, -v`: Show detailed information
- `--json`: Output data in JSON format
- `--output, -o`: Save output to specified file

## Sample Output

### Human-Readable Format
```
=== Health Data for United States ===
Country Code: US
Population: 331,002,651
Region: Americas (Northern America)
Capital: Washington, D.C.
Last Updated: 2024-01-15T10:30:00.000Z

--- COVID-19 Statistics ---
Total Cases: 103,436,829
Total Deaths: 1,127,152
Total Recovered: 100,781,036
Active Cases: 1,528,641
Cases per Million: 312,045
Deaths per Million: 3,402
```

### JSON Format
```json
{
  "country": "USA",
  "country_code": "US",
  "population": 331002651,
  "updated": "2024-01-15T10:30:00.000Z",
  "covid_statistics": {
    "total_cases": 103436829,
    "total_deaths": 1127152,
    "total_recovered": 100781036,
    "active_cases": 1528641,
    "cases_per_million": 312045,
    "deaths_per_million": 3402
  },
  "demographics": {
    "region": "Americas",
    "subregion": "Northern America",
    "capital": "Washington, D.C.",
    "languages": ["English"]
  }
}
```

## Supported Countries

The script supports all countries available in the REST Countries API. You can use:
- Full country names (e.g., "United States", "Germany", "India")
- ISO country codes (e.g., "US", "DE", "IN")
- Common abbreviations (e.g., "USA", "UK")

## Error Handling

The script includes comprehensive error handling for:
- Invalid country names or codes
- Network connectivity issues
- API rate limiting
- Data parsing errors
- File I/O operations

## Data Sources

- **COVID-19 Data**: [Disease.sh](https://disease.sh/) - Real-time COVID-19 statistics
- **Country Information**: [REST Countries](https://restcountries.com/) - Country data and demographics
- **Vaccination Data**: [Disease.sh Vaccine API](https://disease.sh/docs/#/COVID-19%3A%20Vaccine) - Vaccination statistics

## Rate Limiting

The APIs used have rate limits:
- Disease.sh: No strict rate limit, but please be respectful
- REST Countries: No rate limit for normal usage

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Disclaimer

This tool is for educational and informational purposes only. Health data should be verified from official sources before making any health-related decisions.

## Future Enhancements

- [ ] Add World Bank health indicators
- [ ] Implement caching for repeated requests
- [ ] Add historical data analysis
- [ ] Create web interface
- [ ] Add more visualization options
- [ ] Implement data export to CSV/Excel
- [ ] Add comparative analysis between countries