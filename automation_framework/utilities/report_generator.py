import json
import os
from datetime import datetime
from typing import Dict, Tuple, List

class ReportGenerator:
    def __init__(self, reports_dir="automation_framework/reports"):
        self.reports_dir = reports_dir
        os.makedirs(reports_dir, exist_ok=True)

    def generate_report(self, web_data: Dict[str, Tuple[float, float]], 
                       api_data: Dict[str, Tuple[float, float]],
                       test_status: Dict = None) -> str:
        """
        Generate a report comparing web and API weather data
        
        Args:
            web_data (Dict[str, Tuple[float, float]]): Web scraped temperature data
            api_data (Dict[str, Tuple[float, float]]): API temperature data
            test_status (Dict): Test execution status and warnings
            
        Returns:
            str: Path to the generated report file
        """
        discrepancies = []
        for city in set(web_data.keys()) & set(api_data.keys()):
            web_temp, web_feels = web_data[city]
            api_temp, api_feels = api_data[city]
            
            temp_diff = abs(web_temp - api_temp)
            feels_diff = abs(web_feels - api_feels)
            
            if temp_diff > 0 or feels_diff > 0:
                discrepancies.append({
                    "city": city,
                    "web_temperature": web_temp,
                    "api_temperature": api_temp,
                    "temperature_difference": temp_diff,
                    "web_feels_like": web_feels,
                    "api_feels_like": api_feels,
                    "feels_like_difference": feels_diff
                })
        
        if discrepancies:
            temp_diffs = [d["temperature_difference"] for d in discrepancies]
            feels_diffs = [d["feels_like_difference"] for d in discrepancies]
            
            statistics = {
                "temperature": {
                    "mean_difference": sum(temp_diffs) / len(temp_diffs),
                    "max_difference": max(temp_diffs),
                    "min_difference": min(temp_diffs)
                },
                "feels_like": {
                    "mean_difference": sum(feels_diffs) / len(feels_diffs),
                    "max_difference": max(feels_diffs),
                    "min_difference": min(feels_diffs)
                }
            }
        else:
            statistics = {
                "temperature": {"mean_difference": 0, "max_difference": 0, "min_difference": 0},
                "feels_like": {"mean_difference": 0, "max_difference": 0, "min_difference": 0}
            }
        
        avg_temperatures = {}
        for city in set(web_data.keys()) & set(api_data.keys()):
            web_temp = web_data[city][0]
            api_temp = api_data[city][0]
            avg_temperatures[city] = (web_temp + api_temp) / 2
        
        highest_temp_city = max(avg_temperatures.items(), key=lambda x: x[1])
        
        report_data = {
            "timestamp": datetime.now().isoformat(),
            "discrepancies": discrepancies,
            "statistics": statistics,
            "test_status": test_status or {
                "success": True,
                "errors": [],
                "warnings": []
            },
            "highest_temperature": {
                "city": highest_temp_city[0],
                "temperature": highest_temp_city[1]
            }
        }
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_path = os.path.join(self.reports_dir, f"weather_report_{timestamp}.json")
        
        with open(report_path, 'w') as f:
            json.dump(report_data, f, indent=2)
            
        return report_path
