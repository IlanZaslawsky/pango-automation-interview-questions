import pytest
import pytest_asyncio
import os
import json
import asyncio
from datetime import datetime
import shutil
from unittest.mock import AsyncMock, Mock
from automation_framework.utilities.web_scraper import WebScraper
from automation_framework.utilities.api_helpers import ApiHelper
from automation_framework.utilities.db_helpers import DatabaseHelper
from automation_framework.utilities.config_helpers import ConfigHelper
from automation_framework.utilities.report_generator import ReportGenerator

@pytest.fixture
def config():
    """Create a test configuration"""
    return ConfigHelper("automation_framework/tests/test_config.ini")

@pytest.fixture
def api():
    """Create an API helper with test configuration"""
    return ApiHelper("automation_framework/tests/test_config.ini")

@pytest.fixture
def db():
    """Create a database helper with test configuration"""
    # Create test database directory if it doesn't exist
    os.makedirs("automation_framework/tests/data", exist_ok=True)
    
    # Use a test database file
    db_path = "automation_framework/tests/data/test_weather_data.db"
    
    # Remove existing test database if it exists
    if os.path.exists(db_path):
        os.remove(db_path)
    
    # Create and initialize the database
    db_helper = DatabaseHelper("automation_framework/tests/test_config.ini")
    db_helper.create_tables()
    
    yield db_helper
    
    # Cleanup after test
    if os.path.exists(db_path):
        os.remove(db_path)

@pytest.fixture
def report_generator():
    """Create a report generator"""
    return ReportGenerator()

@pytest_asyncio.fixture
async def mock_page():
    """Create a mock page for testing"""
    page = AsyncMock()
    page.goto = AsyncMock()
    page.wait_for_selector = AsyncMock()
    page.query_selector = AsyncMock()
    page.close = AsyncMock()
    
    # Mock the temperature element
    temp_element = AsyncMock()
    temp_element.inner_text = AsyncMock(return_value="18.0°C")
    
    # Mock the feels-like element
    feels_like_element = AsyncMock()
    feels_like_element.inner_text = AsyncMock(return_value="Feels Like: 18.0°C")
    
    # Set up the query_selector to return appropriate elements
    page.query_selector.side_effect = lambda selector: {
        ".h2": temp_element,
        "p:has-text('Feels Like:')": feels_like_element
    }.get(selector)
    
    return page

@pytest_asyncio.fixture
async def mock_browser(mock_page):
    """Create a mock browser for testing"""
    browser = AsyncMock()
    browser.new_context = AsyncMock(return_value=browser)
    browser.new_page = AsyncMock(return_value=mock_page)
    browser.close = AsyncMock()
    return browser

@pytest.mark.asyncio
async def test_weather_data_pipeline(config, api, db, report_generator, mock_page, mock_browser):
    """Test the complete weather data pipeline"""
    test_status = {
        "success": True,
        "errors": [],
        "warnings": []
    }
    
    try:
        # Get all cities from config
        test_cities = config.get_cities()
        if len(test_cities) != 20:
            test_status["warnings"].append(f"Expected 20 cities, got {len(test_cities)}")
        
        # Initialize components
        async with WebScraper() as scraper:
            # Mock the browser and page
            scraper.browser = mock_browser
            scraper.context = mock_browser
            
            # Collect data from both sources
            web_data = await scraper.scrape_multiple_cities(test_cities)
            api_data = await api.get_weather_data(test_cities)
            
            # Verify we got data for all cities
            if len(web_data) != 20:
                test_status["warnings"].append(f"Expected 20 web data records, got {len(web_data)}")
            if len(api_data) != 20:
                test_status["warnings"].append(f"Expected 20 API data records, got {len(api_data)}")
            
            # Store data in database
            for city, (temp, feels_like) in web_data.items():
                db.store_weather_data(city, temp, feels_like, "web")
                
            for city, (temp, feels_like) in api_data.items():
                db.store_weather_data(city, temp, feels_like, "api")
                
            # Verify database storage
            web_records = db.get_weather_data("web")
            api_records = db.get_weather_data("api")
            
            if len(web_records) != 20:
                test_status["warnings"].append(f"Expected 20 web records in database, got {len(web_records)}")
            if len(api_records) != 20:
                test_status["warnings"].append(f"Expected 20 API records in database, got {len(api_records)}")
            
            # Verify data consistency
            for city, (temp, feels_like) in web_data.items():
                if (temp, feels_like) != (18.0, 18.0):
                    test_status["warnings"].append(f"Invalid web data for {city}: got {(temp, feels_like)}, expected (18.0, 18.0)")
                
            for city, (temp, feels_like) in api_data.items():
                if (temp, feels_like) != (18.0, 18.0):
                    test_status["warnings"].append(f"Invalid API data for {city}: got {(temp, feels_like)}, expected (18.0, 18.0)")
            
            # Generate report with test status
            report_path = report_generator.generate_report(web_data, api_data, test_status)
            assert os.path.exists(report_path), "Report file should be created"
            
            # Verify report contents
            with open(report_path, 'r') as f:
                report_data = json.load(f)
                
            assert "timestamp" in report_data
            assert "discrepancies" in report_data
            assert "statistics" in report_data
            assert "test_status" in report_data
            
            # Clean up
            if os.path.exists(report_path):
                os.remove(report_path)
                
    except Exception as e:
        test_status["success"] = False
        test_status["errors"].append(str(e))
        # Still generate a report with error information
        report_path = report_generator.generate_report(
            web_data if 'web_data' in locals() else {},
            api_data if 'api_data' in locals() else {},
            test_status
        )
        if os.path.exists(report_path):
            os.remove(report_path)
        raise 