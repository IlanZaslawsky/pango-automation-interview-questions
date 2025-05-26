import os
import json
import asyncio
import shutil
import pytest
import pytest_asyncio
from unittest.mock import AsyncMock
from datetime import datetime

from automation_framework.utilities.web_scraper import WebScraper
from automation_framework.utilities.api_helpers import ApiHelper
from automation_framework.utilities.db_helpers import DatabaseHelper
from automation_framework.utilities.config_helpers import ConfigHelper
from automation_framework.utilities.report_generator import ReportGenerator

TEMP_TOLERANCE = 5.0
FEELS_LIKE_TOLERANCE = 5.0

@pytest.fixture
def config():
    return ConfigHelper("automation_framework/tests/test_config.ini")

@pytest.fixture
def api():
    return ApiHelper("automation_framework/tests/test_config.ini")

@pytest.fixture
def db():
    os.makedirs("automation_framework/tests/data", exist_ok=True)
    db_path = "automation_framework/tests/data/test_weather_data.db"
    
    if os.path.exists(db_path):
        os.remove(db_path)
    
    db_helper = DatabaseHelper("automation_framework/tests/test_config.ini")
    db_helper.create_tables()
    
    yield db_helper
    
    if os.path.exists(db_path):
        os.remove(db_path)

@pytest.fixture
def report_generator():
    return ReportGenerator()

@pytest_asyncio.fixture
async def mock_page():
    page = AsyncMock()

    temp = AsyncMock()
    temp.inner_text = AsyncMock(return_value="19.2°C")

    feels_like = AsyncMock()
    feels_like.inner_text = AsyncMock(return_value="Feels Like: 18.48°C")

    page.query_selector.side_effect = lambda sel: {
        ".h2": temp,
        "p:has-text('Feels Like:')": feels_like
    }.get(sel)

    return page

@pytest_asyncio.fixture
async def mock_browser(mock_page):
    browser = AsyncMock()
    browser.new_context = AsyncMock(return_value=browser)
    browser.new_page = AsyncMock(return_value=mock_page)
    return browser

async def collect_weather_data(scraper, api, test_cities):
    web_data = await scraper.scrape_multiple_cities(test_cities)
    api_data = await api.get_weather_data(test_cities)
    return web_data, api_data

def store_weather_data(db, web_data, api_data):
    for city, (temp, feels_like) in web_data.items():
        db.store_weather_data(city, temp, feels_like, "web")
        
    for city, (temp, feels_like) in api_data.items():
        db.store_weather_data(city, temp, feels_like, "api")
        
    for city in set(web_data.keys()) & set(api_data.keys()):
        web_temp = web_data[city][0]
        api_temp = api_data[city][0]
        avg_temp = (web_temp + api_temp) / 2
        db.store_average_temperature(city, avg_temp)

def verify_data_consistency(web_data, api_data, test_status):
    for city in web_data:
        assert city in api_data, f"City {city} missing from API data"
        web_temp, web_feels = web_data[city]
        api_temp, api_feels = api_data[city]
        
        temp_diff = abs(web_temp - api_temp)
        feels_diff = abs(web_feels - api_feels)
        
        if temp_diff > TEMP_TOLERANCE:
            test_status["warnings"].append(
                f"Large temperature difference for {city}: web={web_temp}°C, api={api_temp}°C (diff={temp_diff:.1f}°C)"
            )
            
        if feels_diff > FEELS_LIKE_TOLERANCE:
            test_status["warnings"].append(
                f"Large feels-like difference for {city}: web={web_feels}°C, api={api_feels}°C (diff={feels_diff:.1f}°C)"
            )

def verify_database_records(db):
    web_records = db.get_weather_data("web")
    api_records = db.get_weather_data("api")
    avg_records = db.get_average_temperatures()
    
    assert len(web_records) == 20, f"Expected 20 web records in database, got {len(web_records)}"
    assert len(api_records) == 20, f"Expected 20 API records in database, got {len(api_records)}"
    assert len(avg_records) == 20, f"Expected 20 average temperature records, got {len(avg_records)}"
    
    return web_records, api_records, avg_records

def verify_report_contents(report_path):
    with open(report_path, 'r') as f:
        report_data = json.load(f)
        
    assert "timestamp" in report_data
    assert "discrepancies" in report_data
    assert "statistics" in report_data
    assert "test_status" in report_data
    assert "highest_temperature" in report_data

@pytest.mark.asyncio
async def test_weather_data_pipeline(config, api, db, report_generator, mock_page, mock_browser):
    test_cities = config.get_cities()
    assert len(test_cities) == 20, f"Expected 20 cities, got {len(test_cities)}"
    
    test_status = {"success": True, "errors": [], "warnings": []}
    
    async with WebScraper(config) as scraper:
        scraper.browser = mock_browser
        scraper.context = mock_browser
        
        web_data, api_data = await collect_weather_data(scraper, api, test_cities)
        
        assert len(web_data) == 20, f"Expected 20 web data records, got {len(web_data)}"
        assert len(api_data) == 20, f"Expected 20 API data records, got {len(api_data)}"
        
        store_weather_data(db, web_data, api_data)
        verify_data_consistency(web_data, api_data, test_status)
        web_records, api_records, avg_records = verify_database_records(db)
        
        highest_temp_city = max(avg_records.items(), key=lambda x: x[1])
        test_status["highest_temperature"] = {
            "city": highest_temp_city[0],
            "temperature": highest_temp_city[1]
        }
        
        report_path = report_generator.generate_report(web_data, api_data, test_status)
        assert os.path.exists(report_path), "Report file should be created"
        verify_report_contents(report_path)
        
        print(f"\nTest report generated at: {os.path.abspath(report_path)}")
        print(f"\nCity with highest average temperature: {highest_temp_city[0]} ({highest_temp_city[1]:.1f}°C)")
        
        if test_status["warnings"]:
            print("\nTemperature discrepancies found:")
            for warning in test_status["warnings"]:
                print(f"- {warning}") 