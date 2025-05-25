from playwright.async_api import async_playwright, TimeoutError
import logging
from typing import Optional, Tuple, Dict
import time
from urllib.parse import quote
import asyncio

class WebScraper:
    BASE_URL = "https://www.timeanddate.com/weather"
    
    # Mapping of countries to their timeanddate.com URL codes
    COUNTRY_CODES: Dict[str, str] = {
        "United States": "usa",
        "United Kingdom": "uk",
        "Japan": "japan",
        "France": "france",
        "Germany": "germany",
        "Italy": "italy",
        "Spain": "spain",
        "Canada": "canada",
        "Australia": "australia",
        "China": "china",
        "India": "india",
        "Brazil": "brazil",
        "Russia": "russia",
        "South Korea": "south-korea",
        "Mexico": "mexico",
        "Netherlands": "netherlands",
        "Switzerland": "switzerland",
        "Sweden": "sweden",
        "Singapore": "singapore",
        "United Arab Emirates": "united-arab-emirates"
    }
    
    # Special city URL mappings
    CITY_URL_MAPPINGS: Dict[str, str] = {
        "New York": "new-york",
        "Mexico City": "mexico-city",
        "Sao Paulo": "sao-paulo",
        "Dubai": "dubai"
    }
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.playwright = None
        self.browser = None
        self.context = None

    async def __aenter__(self):
        """Setup Playwright resources"""
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(headless=True)
        self.context = await self.browser.new_context()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Cleanup Playwright resources"""
        await self.browser.close()

    def _get_city_url(self, city: str, country: str) -> str:
        """
        Format city name and return the full URL for timeanddate.com
        
        Args:
            city (str): Name of the city
            country (str): Name of the country
            
        Returns:
            str: Formatted URL for the city
        """
        if country not in self.COUNTRY_CODES:
            raise ValueError(f"Country '{country}' not supported. Supported countries: {list(self.COUNTRY_CODES.keys())}")
            
        # Use special mapping for city if it exists, otherwise format normally
        formatted_city = self.CITY_URL_MAPPINGS.get(city, city.lower().replace(" ", "-"))
        country_code = self.COUNTRY_CODES[country]
        
        return f"{self.BASE_URL}/{country_code}/{formatted_city}"

    async def extract_temperature_data(self, city: str, country: str) -> Optional[Tuple[float, float]]:
        """
        Extract temperature and feels-like data from timeanddate.com
        
        Args:
            city (str): Name of the city
            country (str): Name of the country
            
        Returns:
            Optional[Tuple[float, float]]: Tuple of (temperature, feels_like) or None if data unavailable
        """
        page = None
        try:
            page = await self.context.new_page()
            url = self._get_city_url(city, country)
            
            # Navigate to the page with a shorter timeout and more reliable wait condition
            try:
                await page.goto(url, wait_until="domcontentloaded", timeout=15000)
                # Wait for the temperature element to be visible
                await page.wait_for_selector(".h2", timeout=5000)
            except TimeoutError as e:
                self.logger.error(f"Timeout while loading page for {city}, {country}: {str(e)}")
                return None
            
            # Extract temperature
            temp_element = await page.query_selector(".h2")
            if not temp_element:
                self.logger.error(f"Temperature element not found for {city}, {country}")
                return None
                
            temperature_text = await temp_element.inner_text()
            temperature = float(temperature_text.replace("°C", "").strip())
            
            # Extract feels-like temperature using a more specific selector
            feels_like_element = await page.query_selector("p:has-text('Feels Like:')")
            if not feels_like_element:
                self.logger.error(f"Feels-like element not found for {city}, {country}")
                return None
                
            feels_like_text = await feels_like_element.inner_text()
            # Extract the feels-like temperature from the text
            feels_like = float(feels_like_text.split("Feels Like:")[1].split("°C")[0].strip())
            
            return temperature, feels_like
            
        except Exception as e:
            self.logger.error(f"Error scraping weather data for {city}, {country}: {str(e)}")
            return None
        finally:
            if page:
                await page.close()

    async def scrape_multiple_cities(self, cities_with_countries: list[tuple[str, str]]) -> dict:
        """
        Scrape weather data for multiple cities
        
        Args:
            cities_with_countries (list[tuple[str, str]]): List of (city, country) tuples
            
        Returns:
            dict: Dictionary mapping cities to their temperature data
        """
        results = {}
        for city, country in cities_with_countries:
            # Add delay between requests to be respectful to the website
            await asyncio.sleep(2)
            data = await self.extract_temperature_data(city, country)
            if data:
                results[f"{city}, {country}"] = data
        return results
