import os
import requests
import time
from dotenv import load_dotenv
from datetime import datetime
def main():
    """Main script to fetch data from OpenMeteo API and NewsAPI, generate daily brief
       and saves in a timestamped .txt file

    Raises:
        ValueError: raise when NewsAPI key not found in .env file
        
    """
    load_dotenv() # Load .env file
    NEWS_API = os.getenv('NEWS_API_KEY') # Extract newsAPI key
    if not NEWS_API: # Check for newsAPI key
        raise ValueError("NEWS_API_KEY not found in .env file")
    news_url = 'https://newsapi.org/v2/everything' # Base URLs
    weather_url = 'https://api.open-meteo.com/v1/forecast'
    wmo_codes = { # Weather code to translate current weather
        0: "Clear sky",
        1: "Mainly clear",
        2: "Partly cloudy",
        3: "Overcast",
        45: "Fog",
        48: "Depositing rime fog",
        51: "Light drizzle",
        53: "Moderate drizzle",
        55: "Dense drizzle",
        56: "Light freezing drizzle",
        57: "Dense freezing drizzle",
        61: "Slight rain",
        63: "Moderate rain",
        65: "Heavy rain",
        66: "Light freezing rain",
        67: "Heavy freezing rain",
        71: "Slight snow fall",
        73: "Moderate snow fall",
        75: "Heavy snow fall",
        77: "Snow grains",
        80: "Slight rain showers",
        81: "Moderate rain showers",
        82: "Violent rain showers",
        85: "Slight snow showers",
        86: "Heavy snow showers",
        95: "Thunderstorm",
        96: "Thunderstorm with slight hail",
        99: "Thunderstorm with heavy hail"
    }
    category = ''
    avail_categories = ['business','entertainment','general','health','science','sports','technology']
    while category not in avail_categories: # Validate input category
        category = input('Select a category (business/entertainment/general/health/science/sports/technology): ').lower()
        if category not in avail_categories:
            print('Please enter a valid category')
    if category == 'general': # Initialize querys
        query = 'Malaysia'
    else:
        query = 'Malaysia ' + category
    news_params = {
        'q' : query,
        'searchIn' : 'title,description',
        'pageSize' : 3
    }
    news_headers = {
        'Authorization': f'Bearer {NEWS_API}'
    }
    weather_params = {
        'latitude' : 2.196,
        'longitude' : 102.2405,
        'hourly' : ['temperature_2m', 'weather_code'],
        'timezone' : 'Asia/Kuala_Lumpur',
        'forecast_days' : 1
    }
    # Extracting data from news and weather API from helper methods
    def fetch_news(url:str, headers:dict, params:dict) -> dict:
        """Fetch news data from NewsAPI with input parameters

        Args:
            url (str): base URL of NewsAPI
            headers (dict): NewsAPI key authorization
            params (dict): queries for news fetching

        Returns:
            dict: dictionary of response object
        """
        response = requests.get(url, headers = headers, params = params, timeout = 10)
        response.raise_for_status()
        return response.json()
    def fetch_weather(url:str, params:dict) -> dict:
        """Fetch weather data from OpenMeteo API with input parameters

        Args:
            url (str): base URL of OpenMeteo API
            params (dict): queries for weather fetching

        Returns:
            dict: dictionary of response object
        """
        response = requests.get(url, params = params, timeout = 10)
        response.raise_for_status()
        return response.json()
    news_data = {}
    weather_data = {}
    # Error handling for fetching news
    for attempt in range(2):       # try up to 2 times
        try:
            news_data = fetch_news(news_url,news_headers,news_params)
            break                  # Exit loop if success
        except requests.exceptions.Timeout:
            print('Request time out, server may be slow')
        except requests.exceptions.HTTPError as e:
            print(f'HTTP error: {e}')
        except requests.exceptions.ConnectionError:
            print('No Internet connection')
        except requests.exceptions.RequestException as e:
            print(f'Unexpected error {type(e).__name__}: {e}')
        if attempt == 0:
            print('Retrying in 2 seconds...')
            time.sleep(2)
    else:
        print('NewsAPI unavailable after 2 attempts')
    # Error handling for fetching weather
    for attempt in range(2):       # try up to 2 times
        try:
            weather_data = fetch_weather(weather_url,weather_params)
            break                  # Exit loop if success
        except requests.exceptions.Timeout:
            print('Request time out, server may be slow')
        except requests.exceptions.HTTPError as e:
            print(f'HTTP error: {e}')
        except requests.exceptions.ConnectionError:
            print('No Internet connection')
        except requests.exceptions.RequestException as e:
            print(f'Unexpected error {type(e).__name__}: {e}')
        if attempt == 0:
            print('Retrying in 2 seconds...')
            time.sleep(2)
    else:
        print('OpenMeteo API unavailable after 2 attempts')
    if (not news_data) and (not weather_data):
        print(f'Error: News and weather unavailble today')
    else:
        current_time = datetime.now().strftime('%Y.%m.%d_%H.%M.%S')
        hour = datetime.now().hour
        if hour < 5 or hour > 21: # Compute current time period
            period = 'night'
        elif hour < 12:
            period = 'morning'
        elif hour < 17:
            period = 'afternoon'
        else:
            period = 'evening'
        # Brief header with error messages handled
        if not weather_data:
            text = f'Good {period}. Error: Weather unavailable today\nTop news currently({current_time}):'
        else:
            text = f'Good {period}. Current temperature in Melaka: {weather_data["hourly"]["temperature_2m"][hour]}{weather_data["hourly_units"]["temperature_2m"]}. Current weather: {wmo_codes[weather_data["hourly"]["weather_code"][hour]]}\nTop news currently({current_time}):'
        if not news_data:
            text += '\nError: News unavailable today'
        else:
            articles = news_data['articles']
            if not articles:
                text += '\nNo articles found for this category.' # If no article found
            else:
                for index,article in enumerate(articles,1): # Adding articles to brief
                    text += f'\n({index}) {article["title"]}'
                    text += f'\n    Source     : {article["source"]["name"]}'
                    text += f'\n    URL        : {article["url"]}'
        print(text)
        filename = f'{period}_{category}_brief_{current_time}.txt'
        
        with open(filename,'w') as f: # Saves brief in txt file
            f.write(text)
if __name__ == '__main__':
    main()