import requests
import logging
from typing import Dict, Optional, Tuple, List
from .config_helpers import ConfigHelper

class ApiHelper:
    BASE_URL = "https://api.openweathermap.org/data/2.5/weather"
    
    def __init__(self, config_path: str):
        config = ConfigHelper(config_path)
        self.api_key = config.get_api_key()
        self.logger = logging.getLogger(__name__)

    def get_current_weather(self, city: str) -> Optional[Dict]:
        """
        Get current weather data for a city from OpenWeatherMap API
        
        Args:
            city (str): Name of the city
            
        Returns:
            Optional[Dict]: Weather data dictionary or None if request fails
        """
        try:
            url = f"{self.BASE_URL}?q={city}&appid={self.api_key}&units=metric"
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
            response = requests.get(
                f"{self.BASE_URL}?q=London&appid={self.api_key}",
                timeout=5
            )
            return response.status_code == 200
        except requests.exceptions.RequestException:
            return False
