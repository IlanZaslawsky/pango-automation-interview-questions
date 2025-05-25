import configparser
from typing import Dict, List, Tuple
import os

class ConfigHelper:
    def __init__(self, config_path: str = "automation_framework/config/config.ini"):
        self.config = configparser.ConfigParser()
        self.config_path = config_path
        self.load_config()

    def load_config(self) -> None:
        """Load configuration from file"""
        if not os.path.exists(self.config_path):
            raise FileNotFoundError(f"Configuration file not found: {self.config_path}")
        self.config.read(self.config_path)

    def get_api_key(self) -> str:
        """Get OpenWeatherMap API key"""
        api_key = self.config.get("API", "API_KEY")
        if api_key == "your_api_key_here":
            raise ValueError("Please set your OpenWeatherMap API key in config.ini")
        return api_key

    def get_db_name(self) -> str:
        """Get database name"""
        return self.config.get("Database", "DB_NAME")

    def get_temperature_threshold(self) -> float:
        """Get temperature discrepancy threshold"""
        return self.config.getfloat("Analysis", "TEMPERATURE_THRESHOLD")

    def get_cities(self) -> List[Tuple[str, str]]:
        """Get list of cities and their countries"""
        cities = []
        for city, country in self.config["Cities"].items():
            cities.append((city.strip(), country.strip()))
        return cities

    def get_log_config(self) -> Dict[str, str]:
        """Get logging configuration"""
        return {
            "level": self.config.get("Logging", "LOG_LEVEL"),
            "file": self.config.get("Logging", "LOG_FILE")
        } 