# Weather API Testing and Analysis Project

## Test Cases


### 1. Utilize Weather Data for Multiple Cities via City ID Parameter

Example API Endpoint:

```
https://api.openweathermap.org/data/2.5/weather?id={city id}&appid={API key}
```

- Insert temperature and feels_like responses for each city into the database.
- Create a new database column for the average temperature of each city.
- Assert that data inserted into the database matches the API response.
- Print the city with the highest average temperature.

### 2. Dynamic API Key and Base URL Configuration

- Implement configuration management to dynamically retrieve the API KEY and BASE URL from `config.ini` for API calls.

### 3. Web Question: City Temperature Discrepancy Analysis

- Conduct comparative temperature analysis for at least 20 cities using:
  - [timeanddate.com](https://www.timeanddate.com/weather/)
  - [OpenWeatherMap API](https://openweathermap.org/current)

Example API Endpoint:

```
https://api.openweathermap.org/data/2.5/weather?q={city name}&appid={API key}
```

- Identify an appropriate API to obtain city names for testing.
- Employ Selenium for extracting temperature data from the website.
- Use the existing database from previous tasks for data consistency.

Upon completion, generate a concise report highlighting cities with notable temperature discrepancies between the sources.

---

## Project Enhancement Tasks - Advanced Implementation (Required)

You must implement at least **two** of the following enhancements:

- **Smarter Error Handling:**
  - Implement predictive error detection using AI-driven anomaly detection. Include tests demonstrating proactive error identification.

- **Intelligent Logging:**
  - Upgrade logs with AI-based analysis to automatically highlight trends, anomalies, and insights, making debugging and monitoring more effective.

- **Dynamic Test Data:**
  - Generate adaptive, scenario-based test data dynamically to ensure comprehensive test coverage and adaptability.

- **Evolving Data Storage:**
  - Extend the database to include historical weather data. Implement analytical queries or visualizations to derive valuable insights from historical trends.

- **Adaptive Web Scraping:**
  - Enhance scraper robustness with adaptive scraping techniques capable of dynamically adjusting to changes in website structure.

- **Insightful Reporting:**
  - Present analysis results through interactive and visually engaging dashboards powered by AI-driven insights and visualization techniques.

- **Event-Driven Messaging:**
  - Integrate event-driven architecture to efficiently handle asynchronous data updates and notifications.

- **Support different types of CI/CD:**
  - Integrate CI/CD pipelines such as Bitbucket Pipelines and GitHub Actions to streamline automated testing and deployment.

---

## Time and Submission

- This home task is expected to take approximately **2 hours**.
- Your responses and completed tasks must be submitted via a GitHub project repository.

