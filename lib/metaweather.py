import requests

from .exceptions import CityNameError
from .exceptions import UnknownCityNameError
from .exceptions import MetaWeatherUnreachableError

from .settings import API_URL
from .settings import GET_WEATHER_STR
from .settings import SEARCH_CITY_STR


class MetaWeather:

    def __init__(self, city_name: str):
        self.__city_name = self.validate_city_name(city_name)

    def validate_city_name(self, city_name: str):
        """
        Validate the city name
        :param city_name:
        :return:
        """
        tmp = city_name.strip().lower()
        if len(tmp) >= 3:
            return tmp
        else:
            raise CityNameError(city_name)

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

    def search_for_city(self):
        """
        Search for the city by it's name

        :return:
        """
        query_url = self.construct_url(self.__city_name)
        response = requests.get(query_url)
        if response.ok:
            cities = response.json()
            if len(cities) > 0:
                return cities
            else:
                raise UnknownCityNameError(self.__city_name)
        else:
            raise MetaWeatherUnreachableError()
