class CityNameError(Exception):

    def __init__(self, city_name):
        message = "{city_name} is invalid name, it needs to be at least 3 characters".format(city_name=city_name)
        super().__init__(message)


class UnknownCityNameError(Exception):

    def __init__(self, city_name):
        message = "{city_name} was not found!".format(city_name=city_name)
        super().__init__(message)


class MetaWeatherUnreachableError(Exception):

    def __init__(self):
        message = "The metaweather API is unreachable!"
        super().__init__(message)
