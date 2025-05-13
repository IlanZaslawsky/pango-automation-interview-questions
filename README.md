# Weather API Testing & Analysis Project

## Overview
Design and implement a testing and analysis solution that compares real-time temperature readings from a public website and an external API, stores and analyzes the data, and generates a discrepancy report.

---

## Test Case: City Temperature Discrepancy Analysis

1. **Cities**  
   - Select **20** random cities.

2. **Data Sources**  
   - **Website**: scrape current temperature from [timeanddate.com](https://www.timeanddate.com/weather/).  
   - **API**: fetch temperature data from OpenWeatherMap using the endpoint:  
     ```
     https://api.openweathermap.org/data/2.5/weather?q={city name}&appid={API key}
     ```

3. **Data Extraction**  
   - **Web Scraping**  
     - Use Selenium or Playwright to retrieve the displayed “temperature” and “feels_like” values for each city.
   - **API Call**  
     - Parse the JSON response to extract “temp” and “feels_like.”

4. **Database Integration**  
   - Insert each city’s:
     - `temperature_web`
     - `feels_like_web`
     - `temperature_api`
     - `feels_like_api`
   - Create a computed column `avg_temperature` that averages the web and API temperatures.
   - Use the existing database schema from prior tasks for consistency.

5. **Reporting**  
   - After data collection, generate a report (CSV or HTML) highlighting:
     - Cities where the difference between web and API temperatures exceeds a configurable threshold.
     - Summary statistics (mean, max, min discrepancy).

---

## Estimated Effort & Submission

- **Submission**:  
  1. Push your code, configuration, and report(s) to a **GitHub repository**.  
  2. Include a brief README explaining how to set up, run tests, and view reports.
