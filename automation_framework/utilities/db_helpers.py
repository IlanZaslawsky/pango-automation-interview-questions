import sqlite3
from datetime import datetime
from .config_helpers import ConfigHelper
import os

class DatabaseHelper:
    def __init__(self, config_path):
        # Load configuration
        config = ConfigHelper(config_path)
        db_name = config.get_db_name()
        
        # Ensure the database directory exists
        db_dir = os.path.dirname(db_name)
        if db_dir:
            os.makedirs(db_dir, exist_ok=True)
            
        # Register datetime adapter
        sqlite3.register_adapter(datetime, lambda dt: dt.isoformat())
        
        # Connect to database
        self.conn = sqlite3.connect(db_name)
        self.create_tables()

    def create_tables(self):
        # Create tables if they don't exist
        with self.conn:
            self.conn.execute('''CREATE TABLE IF NOT EXISTS weather_data (
                city TEXT PRIMARY KEY,
                temperature_web REAL,
                feels_like_web REAL,
                temperature_api REAL,
                feels_like_api REAL,
                avg_temperature REAL,
                timestamp TEXT DEFAULT CURRENT_TIMESTAMP
            )''')

    def store_weather_data(self, city, temperature, feels_like, source):
        """
        Store weather data from either web or API source
        """
        timestamp = datetime.now()
        
        with self.conn:
            if source == "web":
                self.conn.execute('''
                    INSERT OR REPLACE INTO weather_data 
                    (city, temperature_web, feels_like_web, timestamp)
                    VALUES (?, ?, ?, ?)
                ''', (city, temperature, feels_like, timestamp))
            elif source == "api":
                self.conn.execute('''
                    UPDATE weather_data 
                    SET temperature_api = ?, feels_like_api = ?, timestamp = ?
                    WHERE city = ?
                ''', (temperature, feels_like, timestamp, city))

    def get_weather_data(self, source=None):
        """
        Retrieve weather data for a specific source or all data
        """
        if source == "web":
            cursor = self.conn.execute('SELECT city, temperature_web, feels_like_web FROM weather_data')
        elif source == "api":
            cursor = self.conn.execute('SELECT city, temperature_api, feels_like_api FROM weather_data')
        else:
            cursor = self.conn.execute('SELECT * FROM weather_data')
        return list(cursor.fetchall())  # Convert cursor to list

    def get_temperature_discrepancies(self, threshold):
        """
        Get cities where temperature difference exceeds the threshold
        """
        cursor = self.conn.execute('''
            SELECT city, 
                   temperature_web, 
                   temperature_api,
                   ABS(temperature_web - temperature_api) as difference
            FROM weather_data
            WHERE ABS(temperature_web - temperature_api) > ?
        ''', (threshold,))
        return list(cursor.fetchall())  # Convert cursor to list

    def get_statistics(self):
        """
        Get summary statistics for temperature discrepancies
        """
        cursor = self.conn.execute('''
            SELECT 
                AVG(ABS(temperature_web - temperature_api)) as mean_discrepancy,
                MAX(ABS(temperature_web - temperature_api)) as max_discrepancy,
                MIN(ABS(temperature_web - temperature_api)) as min_discrepancy
            FROM weather_data
        ''')
        return cursor.fetchone()

    def close(self):
        """
        Close the database connection
        """
        self.conn.close()

