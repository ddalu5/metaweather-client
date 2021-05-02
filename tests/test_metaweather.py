from datetime import date
from unittest import TestCase

from lib.metaweather import MetaWeather

from lib.exceptions import CityNameError
from lib.exceptions import CityIdNotFound


class TestMetaWeather(TestCase):

    def setUp(self):
        self.meta_weather_paris = MetaWeather("Paris")

    def test_validate_city_name(self):
        with self.assertRaises(CityNameError):
            self.meta_weather_paris.validate_city_name("x")
        self.assertEqual("paris", self.meta_weather_paris.validate_city_name("  PaRiS "))

    def test_construct_url(self):
        search_query = self.meta_weather_paris.construct_url("PARIS")
        self.assertEqual(search_query, "https://www.metaweather.com/api/location/search/?query=PARIS")
        weather_query = self.meta_weather_paris.construct_url(615702)
        self.assertEqual(weather_query, "https://www.metaweather.com/api/location/615702/")

    def test_search_city(self):
        results = self.meta_weather_paris.search_for_city()
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['woeid'], 615702)
        tmp_obj = MetaWeather("san")
        self.assertGreater(len(tmp_obj.search_for_city()), 1)

    def test_get_city_weather_by_date(self):
        results = self.meta_weather_paris.get_city_weather_by_date(615702, date.today().strftime("%Y/%m/%d"))
        self.assertGreater(len(results), 0)
        with self.assertRaises(CityIdNotFound):
            self.meta_weather_paris.get_city_weather_by_date(0, date.today().strftime("%Y/%m/%d"))
