import datetime
import requests

from .settings import API_URL
from .settings import GET_WEATHER_STR
from .settings import SEARCH_CITY_STR

from .exceptions import CityNameError
from .exceptions import CityIdNotFound
from .exceptions import UnknownCityNameError
from .exceptions import MetaWeatherUnreachableError


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

    def get_city_weather_by_date(self, city_id: int, selected_date: str):
        """
        get the weather data for a selected date formed(yyy/mm/dd) for a city (city id from the API)

        :param city_id:
        :param selected_date:
        :return:
        """
        query_url = self.construct_url(city_id) + selected_date
        response = requests.get(query_url)
        if response.ok:
            data = response.json()
            if len(data) > 0:
                return data
            else:
                raise Exception("No data found!")
        else:
            if response.status_code == 404:
                raise CityIdNotFound(city_id)
            else:
                raise MetaWeatherUnreachableError()

    def get_city_weather_for_tomorrow(self, city_id: int):
        """
        A wrapper for get_city_weather_by_date that return the next day data

        :param city_id:
        :return:
        """
        today = datetime.date.today()
        tomorrow = today + datetime.timedelta(days=1)
        return self.get_city_weather_by_date(city_id, tomorrow.strftime("%Y/%m/%d"))

    def will_it_rain(self, data):
        """
        Check data from API to see the in the day it will rain

        Data sample:

                [
                {
                    "id": 4540974517714944,
                    "weather_state_name": "Light Rain",
                    "weather_state_abbr": "lr",
                    "wind_direction_compass": "NW",
                    "created": "2021-05-02T12:51:05.139803Z",
                    "applicable_date": "2021-05-02",
                    "min_temp": 4.390000000000001,
                    "max_temp": 13.469999999999999,
                    "the_temp": 12.02,
                    "wind_speed": 3.5150352315782496,
                    "wind_direction": 316.6650091359808,
                    "air_pressure": 1021.0,
                    "humidity": 63,
                    "visibility": 10.110952040085898,
                    "predictability": 75
                },
                {
                    "id": 5631574725885952,
                    "weather_state_name": "Light Rain",
                    "weather_state_abbr": "lr",
                    "wind_direction_compass": "NW",
                    "created": "2021-05-02T09:51:04.084851Z",
                    "applicable_date": "2021-05-02",
                    "min_temp": 4.41,
                    "max_temp": 13.620000000000001,
                    "the_temp": 12.0,
                    "wind_speed": 3.3687170982449164,
                    "wind_direction": 316.3316677603159,
                    "air_pressure": 1021.0,
                    "humidity": 62,
                    "visibility": 9.348529587210688,
                    "predictability": 75
                }
            ]

        weather_state_abbr:
            Heavy Rain 	'hr'
            Light Rain 	'lr'
            Showers 	's'
        :param data:
        :return:
        """
        for element in data:
            if element['weather_state_abbr'] in ('s', 'lr', 'hr'):
                return True
        return False

    def cli_select_city(self, tmp):
        print("The search query returned multiple cities, please type the id of the city you are looking for:")
        for tmp_id, element in tmp.items():
            print("{id}. {title}".format(id=tmp_id, title=element['title']))
        selected = int(input("Please select a city: "))
        if selected in tmp:
            return tmp[selected]['woeid']
        else:
            print("[#] There was an error in the selection, please select one from the list.")
            return self.cli_select_city(tmp)

    def cli_check_if_it_will_rain(self):
        cities = self.search_for_city()
        i = 1
        if len(cities) > 1:
            tmp = {}
            for element in cities:
                tmp[i] = element
                i += 1
            city_id = self.cli_select_city(tmp)
        else:
            city_id = cities[0]['woeid']
        data = self.get_city_weather_for_tomorrow(city_id)
        rain = self.will_it_rain(data)
        if rain:
            print("Tomorrow it will rain!")
        else:
            print("Tomorrow there will be no rain!")
