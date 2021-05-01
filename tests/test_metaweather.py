from unittest import TestCase

from lib.metaweather import MetaWeather
from lib.exceptions import CityNameError


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