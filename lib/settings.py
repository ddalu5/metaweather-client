import os

API_URL = os.environ.get("API_URL", "https://www.metaweather.com/api/")
SEARCH_CITY_STR = os.environ.get("SEARCH_CITY_STR", "location/search/?query={city}")
GET_WEATHER_STR = os.environ.get("GET_WEATHER_STR", "location/{woeid}/")
