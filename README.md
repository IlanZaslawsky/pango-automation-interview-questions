# Weather API Testing & Analysis Project

## Overview
This project implements an automated system for comparing weather data from timeanddate.com and OpenWeatherMap API. It collects temperature data from both sources, stores it in a database, and generates reports highlighting discrepancies.

## Features
- Web scraping using Playwright
- OpenWeatherMap API integration
- SQLite database storage
- Configurable temperature discrepancy analysis
- JSON report generation
- Comprehensive test suite

## Prerequisites
- Python 3.8+
- OpenWeatherMap API key
- Playwright browsers

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd pango-automation-interview-questions
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Install Playwright browsers:
```bash
playwright install
```

5. Configure the API key:
   - Copy `automation_framework/config/config.ini.example` to `automation_framework/config/config.ini`
   - Add your OpenWeatherMap API key to the `[API]` section

## Usage

### Running the Tests
```bash
pytest automation_framework/tests/
```

### Running the Pipeline
```bash
python -m automation_framework.main
```

### Viewing Reports
Reports are generated in JSON format and stored in the `automation_framework/reports` directory. Each report includes:
- Timestamp of data collection
- Temperature discrepancy threshold
- List of cities with significant temperature differences
- Statistical analysis (mean, max, min discrepancies)

## Project Structure
```
automation_framework/
├── config/
│   └── config.ini          # Configuration file
├── logs/                   # Application logs
├── reports/               # Generated reports
├── tests/
│   ├── test_weather_pipeline.py  # End-to-end tests
│   └── test_config.ini    # Test configuration
└── utilities/
    ├── api_helpers.py     # OpenWeatherMap API integration
    ├── config_helpers.py  # Configuration management
    ├── db_helpers.py      # Database operations
    ├── report_generator.py # Report generation
    └── web_scraper.py     # Web scraping functionality
```

## Configuration
The `config.ini` file allows you to customize:
- API settings
- Database configuration
- Temperature discrepancy threshold
- List of cities to monitor
- Logging settings

## Error Handling
The system handles various error scenarios:
- Network connectivity issues
- Invalid API responses
- Database connection problems
- Web scraping failures

## Logging
Logs are stored in the `automation_framework/logs` directory with different levels:
- INFO: Normal operation
- WARNING: Non-critical issues
- ERROR: Critical failures

## Contributing
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License
[Your chosen license]
