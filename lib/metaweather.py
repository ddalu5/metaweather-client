from .settings import API_URL
from .settings import GET_WEATHER_STR
from .settings import SEARCH_CITY_STR


class MetaWeather:

    def __init__(self, city_name: str):
        self.city_name = city_name.lower().strip()

    def construct_url(self, obj):
        """
        Constructs an URL either to search the city or to get the weather if it's an ID
        :param obj: str for city or int for city id
        :return: API URL
        """
        if type(obj) is int:
            return API_URL + GET_WEATHER_STR.format(woeid=obj)
        else:
            return API_URL + SEARCH_CITY_STR.format(city=obj)
