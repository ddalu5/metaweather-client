import sys

from lib.metaweather import MetaWeather


if __name__ == "__main__":
    args = sys.argv
    if len(args) == 1:
        print("[!] no argument was passed, please type 'python main.py city name'")
    else:
        city_name = ' '.join(args[1:])
        print("[+] Selected city name : " + city_name)
        obj = MetaWeather(city_name)
        obj.cli_check_if_it_will_rain()
