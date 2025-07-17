# Health Data Fetcher

A Python script that fetches health data for specific countries using various global health APIs.

## Features

- Fetches health data from World Bank Health Data API
- Retrieves additional indicators from WHO Global Health Observatory API
- Supports country name input with automatic country code resolution
- Provides formatted output with key health indicators
- Includes error handling and validation
- Supports output to file

## Installation

1. Clone the repository
2. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Basic Usage

```bash
python health_data_fetcher.py "United States"
```

### Demo Mode (with sample data)

```bash
python health_data_fetcher.py "United States" --demo
```

### Save output to file

```bash
python health_data_fetcher.py "India" --output india_health_data.txt
```

### Combined demo and file output

```bash
python health_data_fetcher.py "Germany" --demo --output germany_health.txt
```

### Help

```bash
python health_data_fetcher.py --help
```

## Health Indicators

The script fetches the following health indicators:

### World Bank Indicators
- Life Expectancy at Birth
- Mortality Rate, Under-5
- Maternal Mortality Ratio
- Current Health Expenditure (% of GDP)
- Total Population

### WHO Indicators
- Life Expectancy at Birth
- Adult Mortality Rate
- Under-five Mortality Rate

## Example Output

```
============================================================
HEALTH DATA FOR UNITED STATES
============================================================
Report generated on: 2024-01-15 10:30:45

WORLD BANK HEALTH INDICATORS:
----------------------------------------
• Life Expectancy at Birth: 76.4 (2021)
• Mortality Rate, Under-5: 6.5 (2021)
• Maternal Mortality Ratio: 23.8 (2020)
• Current Health Expenditure (% of GDP): 17.83% (2020)
• Total Population: 331,893,745 (2021)

WHO HEALTH INDICATORS:
----------------------------------------
• Life Expectancy at Birth: 76.4 (2021)
• Adult Mortality Rate: 140.2 (2021)
• Under-five Mortality Rate: 6.5 (2021)

============================================================
```

## API Sources

- **World Bank Health Data API**: Provides comprehensive health and demographic indicators
- **WHO Global Health Observatory API**: Offers additional health metrics and indicators
- **REST Countries API**: Used for country name to ISO code conversion

## Error Handling

The script includes comprehensive error handling for:
- Invalid country names
- API connection issues
- Missing data
- Network timeouts

**Note:** If the APIs are not accessible due to network restrictions, use the `--demo` flag to run with sample data.

## Requirements

- Python 3.6+
- requests library
- Internet connection for API access

## License

This project is licensed under the MIT License.