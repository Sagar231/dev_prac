from flask import Flask, render_template, request
#flask is a micro framework
import requests
import io
import matplotlib.pyplot as plt
import base64
import pandas as pd
import os

import matplotlib
matplotlib.use('Agg')

app = Flask(__name__)

WEATHER_API_KEY = 'bb94f838d7ed3b1f99c74735434843b5'

def get_weather_data(city):
    base_url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric'
    try:
        response = requests.get(base_url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching weather data: {e}")
        return None

def generate_weather_plot(weather_data):
    metrics = ['Temperature (°C)', 'Humidity (%)']
    values = [weather_data['main']['temp'], weather_data['main']['humidity']]
    plt.figure(figsize=(6, 4))
    plt.bar(metrics, values, color=['blue', 'green'])
    plt.title(f"Weather Metrics for {weather_data['name']}")
    plt.ylabel('Value')
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plot_data = base64.b64encode(buffer.getvalue()).decode('utf-8')
    buffer.close()
    plt.close()
    return plot_data

def save_weather_data_to_excel(weather_data, filename="weather_data.xlsx"):
    # Prepare new data to append
    new_data = {
        'City': [weather_data['name']],
        'Temperature (°C)': [weather_data['main']['temp']],
        'Humidity (%)': [weather_data['main']['humidity']],
        'Weather Description': [weather_data['weather'][0]['description']],
        'Pressure (hPa)': [weather_data['main']['pressure']],
        'Wind Speed (m/s)': [weather_data['wind']['speed']],
    }

    new_df = pd.DataFrame(new_data)
    
    # Check if the Excel file exists
    if os.path.exists(filename):
        # If file exists, append the new data without writing header
        with pd.ExcelWriter(filename, mode='a', engine='openpyxl', if_sheet_exists='overlay') as writer:
            new_df.to_excel(writer, index=False, header=False, sheet_name='WeatherData')
    else:
        # If file does not exist, create a new one with header
        new_df.to_excel(filename, index=False, engine='openpyxl', sheet_name='WeatherData')

@app.route("/", methods=["GET", "POST"])
def index():
    weather_data = None
    weather_plot = None
    error_message = None

    if request.method == "POST":
        city = request.form.get("city")
        if city:
            weather_data = get_weather_data(city)
            if weather_data and weather_data.get("cod") == 200:
                weather_plot = generate_weather_plot(weather_data)
                save_weather_data_to_excel(weather_data)  # Save the weather data to Excel
            else:
                error_message = f"City '{city}' not found. Please try again."

    return render_template(
        "index.html",
        graph_url=weather_plot,
        error_message=error_message,
        weather_data=weather_data
    )

if __name__ == "__main__":
    app.run(debug=True)
