from unittest import TestCase

from lib.metaweather import MetaWeather


class TestMetaWeather(TestCase):

    def setUp(self):
        self.meta_weather_paris = MetaWeather("Paris")

    def test_construct_url(self):
        search_query = self.meta_weather_paris.construct_url("PARIS")
        self.assertEqual(search_query, "https://www.metaweather.com/api/location/search/?query=PARIS")
        weather_query = self.meta_weather_paris.construct_url(615702)
        self.assertEqual(weather_query, "https://www.metaweather.com/api/location/615702/")
