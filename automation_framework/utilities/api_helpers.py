import requests
import logging
from typing import Dict, Optional, Tuple, List
from .config_helpers import ConfigHelper

class ApiHelper:
    def __init__(self, config_path: str):
        self.config = ConfigHelper(config_path)
        self.api_key = self.config.get_api_key()
        self.logger = logging.getLogger(__name__)
        self.base_url = self.config.get_api_base_url()

    def get_current_weather(self, city: str) -> Optional[Dict]:
        """
        Get current weather data for a city from OpenWeatherMap API
        
        Args:
            city (str): Name of the city
            
        Returns:
            Optional[Dict]: Weather data dictionary or None if request fails
        """
        try:
            city_id = self.config.get_city_id(city)
            url = f"{self.base_url}?id={city_id}&appid={self.api_key}&units=metric"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Error fetching weather data for {city}: {str(e)}")
            return None

    def extract_temperature_data(self, city: str) -> Optional[Tuple[float, float]]:
        """
        Extract temperature and feels_like data from API response
        
        Args:
            city (str): Name of the city
            
        Returns:
            Optional[Tuple[float, float]]: Tuple of (temperature, feels_like) or None if data unavailable
        """
        weather_data = self.get_current_weather(city)
        
        if not weather_data or 'main' not in weather_data:
            self.logger.error(f"Invalid weather data received for {city}")
            return None
            
        try:
            main_data = weather_data['main']
            temperature = float(main_data['temp'])
            feels_like = float(main_data['feels_like'])
            return temperature, feels_like
        except (KeyError, ValueError) as e:
            self.logger.error(f"Error extracting temperature data for {city}: {str(e)}")
            return None

    async def get_weather_data(self, cities: List[Tuple[str, str]]) -> Dict[str, Tuple[float, float]]:
        """
        Get weather data for multiple cities
        
        Args:
            cities (List[Tuple[str, str]]): List of (city, country) tuples
            
        Returns:
            Dict[str, Tuple[float, float]]: Dictionary mapping cities to their temperature data
        """
        results = {}
        for city, country in cities:
            city_key = f"{city}, {country}"
            temp_data = self.extract_temperature_data(city)
            if temp_data:
                results[city_key] = temp_data
        return results

    def validate_api_key(self) -> bool:
        """
        Validate the API key by making a test request
        
        Returns:
            bool: True if API key is valid, False otherwise
        """
        try:
            # Using London as a test city
            city_id = self.config.get_city_id("London")
            response = requests.get(
                f"{self.base_url}?id={city_id}&appid={self.api_key}",
                timeout=5
            )
            return response.status_code == 200
        except requests.exceptions.RequestException:
            return False
