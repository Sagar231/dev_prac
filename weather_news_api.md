
---

# **Project Documentation: Weather and News Data Fetching, Saving, and Visualization**

## **Overview**
This Python project fetches real-time weather data for a specified city and news articles on a specified topic using APIs. It saves the data in an Excel file with separate sheets for weather and news data and visualizes the information using bar charts. The project is structured into several functions for modularity, making it easy to understand and maintain.

---

## **Code Breakdown**

### **1. Importing Required Libraries**
```python
import requests
import pandas as pd
import datetime
import matplotlib.pyplot as plt
import seaborn as sns
```
- `requests`: Used for making HTTP requests to fetch data from the APIs.
- `pandas`: Used for handling and manipulating data, especially for saving data to an Excel file.
- `datetime`: Provides date and time functionalities.
- `matplotlib.pyplot` and `seaborn`: Libraries used for data visualization.

---

### **2. API Keys and File Path**
```python
# Replace these with your actual API keys
WEATHER_API_KEY = 'your_weather_api_key'
NEWS_API_KEY = 'your_news_api_key'
EXCEL_FILE = 'data2.xlsx'
```
- **API Keys**: Both APIs (Weather and News) require API keys for access. Replace `'your_weather_api_key'` and `'your_news_api_key'` with valid API keys.
- **File Path**: `EXCEL_FILE` defines the filename for saving data in Excel format.

---

### **3. Fetching Weather Data**
```python
def get_weather_data(city: str):
    """
    Fetches the current weather data for a given city using OpenWeatherMap API.
    """
    base_url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric'
    
    try:
        response = requests.get(base_url)
        response.raise_for_status()  # Raises an exception for HTTP errors
        weather_data = response.json()  # Parses the response JSON
        print(f"Weather data for {city} fetched successfully.")
        return weather_data
    except requests.exceptions.RequestException as e:
        print(f"Error fetching weather data: {e}")
        return None
```
- **Parameters**:
  - `city` (string): Name of the city for which to get weather data.
- **Functionality**:
  - Constructs the request URL using `city` and `WEATHER_API_KEY`.
  - Sends a GET request to fetch data and checks for errors.
  - If successful, returns parsed JSON data; otherwise, it prints an error message.

---

### **4. Fetching News Data**
```python
def get_news_data(query: str, language: str = 'en'):
    """
    Fetches the top news articles based on a search query using News API.
    """
    base_url = f'https://newsapi.org/v2/everything?q={query}&language={language}&apiKey={NEWS_API_KEY}'
    
    try:
        response = requests.get(base_url)
        response.raise_for_status()  # Raises an exception for HTTP errors
        news_data = response.json()  # Parses the response JSON
        print(f"News data for '{query}' fetched successfully.")
        return news_data
    except requests.exceptions.RequestException as e:
        print(f"Error fetching news data: {e}")
        return None
```
- **Parameters**:
  - `query` (string): Keyword to search for in news articles.
  - `language` (string, optional): Language of the news (default is `'en'` for English).
- **Functionality**:
  - Constructs the request URL with `query`, `language`, and `NEWS_API_KEY`.
  - Sends a GET request to fetch data and checks for errors.
  - If successful, returns parsed JSON data; otherwise, it prints an error message.

---

### **5. Saving Data to Excel**
```python
def save_data_to_excel(weather_data: dict, news_data: dict):
    """
    Saves weather and news data to an Excel file.
    """
    # Process weather data
    weather_df = pd.DataFrame([{
        "City": weather_data.get("name"),
        "Temperature (°C)": weather_data["main"]["temp"],
        "Humidity (%)": weather_data["main"]["humidity"],
        "Weather": weather_data["weather"][0]["description"],
        "Timestamp": str(datetime.datetime.now())
    }])
    
    # Process news data
    articles = news_data.get("articles", [])
    news_df = pd.DataFrame([{
        "Title": article["title"],
        "Source": article["source"]["name"],
        "Published At": article["publishedAt"],
        "Description": article["description"]
    } for article in articles])

    # Save to Excel with different sheets
    with pd.ExcelWriter(EXCEL_FILE) as writer:
        weather_df.to_excel(writer, sheet_name='Weather', index=False)
        news_df.to_excel(writer, sheet_name='News', index=False)
    
    print(f"Data saved to {EXCEL_FILE} successfully.")
```
- **Parameters**:
  - `weather_data` (dict): Weather data in JSON format.
  - `news_data` (dict): News data in JSON format.
- **Functionality**:
  - Creates dataframes for weather and news data.
  - Saves these dataframes to an Excel file with separate sheets for each dataset.

---

### **6. Visualizing Weather Data**
```python
def visualize_weather_data(weather_data: dict):
    """
    Visualizes the temperature and humidity of the weather data using a bar chart.
    """
    data = {
        "Metric": ["Temperature (°C)", "Humidity (%)"],
        "Value": [weather_data["main"]["temp"], weather_data["main"]["humidity"]]
    }
    df = pd.DataFrame(data)
    
    sns.barplot(x="Metric", y="Value", data=df)
    plt.title(f"Weather Metrics for {weather_data.get('name')}")
    plt.xlabel("Metric")
    plt.ylabel("Value")
    plt.show()
```
- **Parameters**:
  - `weather_data` (dict): Weather data in JSON format.
- **Functionality**:
  - Creates a bar plot for temperature and humidity using Seaborn.

---

### **7. Visualizing News Data**
```python
def visualize_news_data(news_data: dict):
    """
    Visualizes the distribution of news sources.
    """
    sources = [article["source"]["name"] for article in news_data.get("articles", [])]
    source_counts = pd.Series(sources).value_counts()
    
    source_counts.plot(kind="bar", color="skyblue")
    plt.title("News Source Distribution")
    plt.xlabel("Source")
    plt.ylabel("Number of Articles")
    plt.xticks(rotation=45)
    plt.show()
```
- **Parameters**:
  - `news_data` (dict): News data in JSON format.
- **Functionality**:
  - Creates a bar chart showing the distribution of articles by news source.

---

### **8. Main Function to Fetch, Save, and Visualize Data**
```python
def fetch_and_process_data(city: str, news_query: str):
    """
    Fetches weather and news data, saves it to an Excel file, and visualizes it.
    """
    weather_data = get_weather_data(city)
    news_data = get_news_data(news_query)

    if weather_data and news_data:
        save_data_to_excel(weather_data, news_data)
        print("Visualizing weather data...")
        visualize_weather_data(weather_data)
        print("Visualizing news data...")
        visualize_news_data(news_data)
```
- **Parameters**:
  - `city` (str): City name for weather data.
  - `news_query` (str): Search keyword for news articles.
- **Functionality**:
  - Combines all the functions to fetch data, save it to Excel, and visualize it.

---

### **9. Example Usage**
```python
if __name__ == "__main__":
    city_name = 'Delhi'
    news_query = 'Crime'
    
    fetch_and_process_data(city_name, news_query)
```
- Runs the `fetch_and_process_data` function using `'Delhi'` as the city for weather data and `'Crime'` as the news query.

---

This code provides a modular way to fetch and analyze real-time data using APIs, save it to an Excel file, and visualize it in Python. Each function has a specific purpose, making it easy for beginners to understand and modify as needed.


---
# **Setting up in your device**

We’ll need `openpyxl` to work with Excel files, as it’s the library that enables Pandas to write data to Excel. Below is a guide on installing the required libraries and ensuring everything is set up for the project.

### Step 1: Setting Up a Virtual Environment (Optional but Recommended)
It's a good practice to create a virtual environment for each project to avoid dependency conflicts between projects. Here’s how you can set it up:

1. Open your terminal or command prompt.
2. Navigate to your project directory.
3. Create a virtual environment with the following command:
   ```bash
   python -m venv env
   ```
4. Activate the virtual environment:
   - **On Windows:**
     ```bash
     .\env\Scripts\activate
     ```
   - **On macOS/Linux:**
     ```bash
     source env/bin/activate
     ```

Now your virtual environment is active, and any packages you install will only apply to this project.

### Step 2: Installing Required Libraries
The project requires the following libraries:
- `requests` for handling HTTP requests to APIs.
- `pandas` for data manipulation and saving data to an Excel file.
- `matplotlib` and `seaborn` for data visualization.
- `openpyxl` for handling Excel files.

To install them, run the following command:
```bash
pip install requests pandas matplotlib seaborn openpyxl
```

### Explanation of Libraries:
- **requests**: Allows us to make API calls to fetch weather and news data.
- **pandas**: Helps in organizing data, handling dataframes, and exporting data to Excel.
- **matplotlib** and **seaborn**: Used to create visualizations for weather metrics and news sources.
- **openpyxl**: A dependency of Pandas for handling Excel files, specifically for writing data to Excel.

### Verifying the Installation
You can verify that everything is installed correctly by running:
```bash
pip list
```
This command will list the installed packages. Look for `requests`, `pandas`, `matplotlib`, `seaborn`, and `openpyxl` in the output list.

### Step 3: Running the Project
Once you have all libraries installed:
1. Save your project code in a file, for example, `weather_news_project.py`.
2. In the terminal, make sure you're in the directory where the file is saved.
3. Run the project with:
   ```bash
   python weather_news_project.py
   ```

If the code runs successfully, it will:
1. Fetch weather and news data.
2. Save the data to an Excel file.
3. Display visualizations for both weather and news data.

This setup ensures everything is ready to run the project seamlessly. Let me know if you'd like more details on any step!

---
