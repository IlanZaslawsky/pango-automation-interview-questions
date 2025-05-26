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

## Setup Instructions

1. Clone the repository
2. Copy the template config file:
   ```bash
   cp automation_framework/config/config.ini.template automation_framework/config/config.ini
   ```
3. Set up your environment variables:
   ```bash
   # For Linux/Mac
   export OPENWEATHER_API_KEY=your_api_key_here
   
   # For Windows (Command Prompt)
   set OPENWEATHER_API_KEY=your_api_key_here
   
   # For Windows (PowerShell)
   $env:OPENWEATHER_API_KEY="your_api_key_here"
   ```

## Usage

### Running the Tests
```bash
pytest automation_framework/tests/test_weather_pipeline.py -v
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
│   ├── config.ini.template  # Template configuration file
│   └── config.ini          # Local configuration (gitignored)
├── logs/                   # Application logs
├── reports/               # Generated reports (gitignored)
├── tests/
│   └── test_weather_pipeline.py
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

## Logging
Logs are stored in the `automation_framework/logs` directory.

## Report Generation

Test reports are generated in the `automation_framework/reports` directory. Each report includes:
- Timestamp
- Temperature discrepancies between web and API data
- Statistical analysis
- Test execution status
- City with highest average temperature
