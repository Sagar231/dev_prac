import requests
import pandas as pd
import datetime
import matplotlib.pyplot as plt
import seaborn as sns

# Replace these with your actual API keys
WEATHER_API_KEY = 'your_own_key_you_will_get_by_signing_up_on_openweathermap.org'
NEWS_API_KEY = 'your_own_key_you_will_get_by_signing_up_on_newsapi.org'

# File path
EXCEL_FILE = 'data2.xlsx'

def get_weather_data(city: str):
    """
    Fetches the current weather data for a given city using OpenWeatherMap API.
    
    Args:
        city (str): The name of the city for which to fetch weather data.
        
    Returns:
        dict: Parsed JSON response containing the weather data, or None if an error occurs.
    """
    base_url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric'
    
    try:
        response = requests.get(base_url)
        response.raise_for_status()
        weather_data = response.json()
        print(f"Weather data for {city} fetched successfully.")
        return weather_data
    except requests.exceptions.RequestException as e:
        print(f"Error fetching weather data: {e}")
        return None

def get_news_data(query: str, language: str = 'en'):
    """
    Fetches the top news articles based on a search query using News API.
    
    Args:
        query (str): The search keyword for news articles.
        language (str): Language of the news (default is 'en' for English).
        
    Returns:
        dict: Parsed JSON response containing the news data, or None if an error occurs.
    """
    base_url = f'https://newsapi.org/v2/everything?q={query}&language={language}&apiKey={NEWS_API_KEY}'
    
    try:
        response = requests.get(base_url)
        response.raise_for_status()
        news_data = response.json()
        print(f"News data for '{query}' fetched successfully.")
        return news_data
    except requests.exceptions.RequestException as e:
        print(f"Error fetching news data: {e}")
        return None

def save_data_to_excel(weather_data: dict, news_data: dict):
    """
    Saves weather and news data to an Excel file.
    
    Args:
        weather_data (dict): The weather data to be saved.
        news_data (dict): The news data to be saved.
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

def visualize_weather_data(weather_data: dict):
    """
    Visualizes the temperature and humidity of the weather data using a bar chart.
    
    Args:
        weather_data (dict): The weather data to be visualized.
    """
    # Prepare data for visualization
    data = {
        "Metric": ["Temperature (°C)", "Humidity (%)"],
        "Value": [weather_data["main"]["temp"], weather_data["main"]["humidity"]]
    }
    df = pd.DataFrame(data)
    
    # Plot
    sns.barplot(x="Metric", y="Value", data=df)
    plt.title(f"Weather Metrics for {weather_data.get('name')}")
    plt.xlabel("Metric")
    plt.ylabel("Value")
    plt.show()

def visualize_news_data(news_data: dict):
    """
    Visualizes the distribution of news sources.
    
    Args:
        news_data (dict): The news data to be visualized.
    """
    # Prepare data for visualization
    sources = [article["source"]["name"] for article in news_data.get("articles", [])]
    source_counts = pd.Series(sources).value_counts()
    
    # Plot
    source_counts.plot(kind="bar", color="skyblue")
    plt.title("News Source Distribution")
    plt.xlabel("Source")
    plt.ylabel("Number of Articles")
    plt.xticks(rotation=45)
    plt.show()

def fetch_and_process_data(city: str, news_query: str):
    """
    Fetches weather and news data, saves it to an Excel file, and visualizes it.
    
    Args:
        city (str): The name of the city for weather data.
        news_query (str): The search keyword for news articles.
    """
    # Fetch data
    weather_data = get_weather_data(city)
    news_data = get_news_data(news_query)

    if weather_data and news_data:
        # Save to Excel
        save_data_to_excel(weather_data, news_data)

        # Visualize data
        print("Visualizing weather data...")
        visualize_weather_data(weather_data)
        
        print("Visualizing news data...")
        visualize_news_data(news_data)

# Example usage
if __name__ == "__main__":
    city_name = 'Delhi'
    news_query = 'Crime'
    
    fetch_and_process_data(city_name, news_query)
