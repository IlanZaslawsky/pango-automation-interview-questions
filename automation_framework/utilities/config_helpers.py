import configparser
from typing import Dict, List, Tuple
import os

class ConfigHelper:
    def __init__(self, config_path: str):
        self.config = configparser.ConfigParser()
        self.config.read(config_path)

    def get_api_key(self) -> str:
        api_key = os.getenv('OPENWEATHER_API_KEY')
        if not api_key:
            raise ValueError("OPENWEATHER_API_KEY environment variable is not set")
        return api_key

    def get_db_name(self) -> str:
        return self.config.get('Database', 'DB_NAME')

    def get_temperature_threshold(self) -> float:
        return self.config.getfloat('Analysis', 'TEMPERATURE_THRESHOLD')

    def get_cities(self) -> List[Tuple[str, str]]:
        cities = []
        for city, country in self.config['Cities'].items():
            if city != 'DEFAULT':
                cities.append((city.strip(), country.strip()))
        return cities

    def get_log_level(self) -> str:
        return self.config.get('Logging', 'LOG_LEVEL')

    def get_log_file(self) -> str:
        return self.config.get('Logging', 'LOG_FILE')

    def get_country_codes(self) -> Dict[str, str]:
        return {country.strip(): code.strip() for country, code in self.config['CountryCodes'].items()}

    def get_api_base_url(self) -> str:
        return self.config.get('API', 'BASE_URL', fallback='https://api.openweathermap.org/data/2.5/weather')

    def get_city_id(self, city: str) -> str:
        return self.config.get('CityIDs', city) 