import requests
from requests.exceptions import RequestException
from string import Template
from typing import Any

from weatherapp.settings import OPEN_WEATHER_PRINTS
from weatherapp.type_aliaces import Lat, Lon
# from settings import OPEN_WEATHER_PRINTS
# from type_aliaces import Lat, Lon


class OpenWeatherWorks:
    def __init__(self) -> None:
        self.api_response_code: int | None = None
        self.appid: str = OPEN_WEATHER_PRINTS['appid']
        self.weather_by_lat_and_lon_url_template: Template = OPEN_WEATHER_PRINTS['weather_by_lat_and_lon_url']
        self.weather_by_city_and_country_template: Template = OPEN_WEATHER_PRINTS['weather_by_city_and_country']
        self.weather_by_city_template: Template = OPEN_WEATHER_PRINTS['weather_by_city']

    def get_temperature_in_celcius_by_lat_and_lon(self, lat: Lat, lon: Lon) -> str:
        self.lat: Lat = lat
        self.lon: Lon = lon
        self.get_weather_by_lat_and_lon()
        return self.location_temperature
        
    def get_weather_by_lat_and_lon(self) -> None:
        self.set_url_with_lat_and_lon()
        self.get_weather_response_by_lat_and_lon()
        self.parse_weather()
        
    def set_url_with_lat_and_lon(self) -> None:
        self.url_with_lat_and_lon: str = self.weather_by_lat_and_lon_url_template.substitute(lat=self.lat, lon=self.lon)
        
    def get_weather_response_by_lat_and_lon(self) -> None:
        self.weather_response: requests.Response | None
        try: 
            self.weather_response = requests.get(self.url_with_lat_and_lon)
        except RequestException:
            self.weather_response = None
        
    def get_lat_and_lot_by_city_and_country(self, city_name: str, country_code: str) -> tuple[Lat, Lon]:
        self.city_name: str = city_name
        self.country_code: str = country_code
        self.get_weather_by_city_and_country()
        return (self.location_lat, self.location_lon)
        
    def get_weather_by_city_and_country(self) -> None:
        self.set_url_with_city_and_country()
        self.get_weather_response_by_city_and_country()
        self.parse_weather()
        
    def set_url_with_city_and_country(self) -> None:
        self.url_with_city_and_country: str = self.weather_by_city_and_country_template.substitute(city_name=self.city_name, country_code=self.country_code)
    
    def get_weather_response_by_city_and_country(self) -> None:
        self.weather_response: requests.Response | None
        try:
            self.weather_response = requests.get(self.url_with_city_and_country)
        except RequestException:
            self.weather_response = None
        
    def get_lat_and_lot_by_city(self, city_name: str) -> tuple[Lat, Lon]:
        self.city_name: str = city_name
        self.get_weather_by_city()
        return (self.location_lat, self.location_lon)
       
    def get_weather_by_city(self) -> None:        
        self.set_url_with_city()
        self.get_weather_response_by_city()
        self.parse_weather()
        
    def set_url_with_city(self) -> None:
        self.url_with_city: str = self.weather_by_city_template.substitute(city_name=self.city_name)
        
    def get_weather_response_by_city(self) -> None:
        self.weather_response: requests.Response | None
        try:
            self.weather_response = requests.get(self.url_with_city)
        except RequestException: # 
            self.weather_response = None

    def parse_weather(self) -> None:        
        self.api_response_code: str | None = None
        self._location_name: str | None = None
        self._country_code: str | None = None
        self._location_temperature: str | None = None
        self._location_lat: Lat | None = None
        self._location_lon: Lon | None = None
                
        if self.weather_response is None:
            self.api_response_code = None
            return
        self.weather: Any = self.weather_response.json()
        
        self.api_response_code = str(self.weather.get('cod'))
        if self.is_result_to_parse():
            self._location_name = self.weather.get('name')        
            self._country_code = self.weather.get('sys', {}).get('country')
            self._location_temperature: str | None = self.handle_temperature()
            self._location_lat = self.weather.get('coord', {}).get('lat')
            self._location_lon = self.weather.get('coord', {}).get('lon')

    def is_result_to_parse(self) -> bool:
        if self.api_response_code is None or self.api_response_code == '404':
            return False
        return True

    def handle_temperature(self) -> str | None:
        location_temperature: str | None = self.weather.get('main', {}).get('temp')
        if location_temperature is None:
            return None

        location_temperature = str(round(float(location_temperature) - 273.15))
        return location_temperature

    def location_info(self) -> dict[str, str | None] | None:
        info: dict[str, str | None] = {
            'api_response_code': self.api_response_code,
            'location_name': self._location_name,
            'country_code': self._country_code,
            'location_temperature': self._location_temperature,
            'location_lat': self._location_lat,
            'location_lon': self._location_lon,
        } 
        return info

    @property
    def location_name(self) -> str|None:
        return self._location_name

    @property
    def location_temperature(self) -> str|None:        
        return self._location_temperature

    @property
    def location_lat(self) -> Lat|None:
        return self._location_lat
    
    @property
    def location_lon(self) -> Lon|None:
        return self._location_lon

    
if __name__ == '__main__':
    open_weather_works: OpenWeatherWorks = OpenWeatherWorks()
    print(f'{open_weather_works.get_temperature_in_celcius_by_lat_and_lon('55.75', '37.62')=}')
    print(f'{open_weather_works.location_name = }')
    print(f'{open_weather_works.location_temperature = }', end='\n\n')

    print(f'{open_weather_works.get_lat_and_lot_by_city_and_country('London', 'UK')=}')
    print(f'{open_weather_works.location_name = }')
    print(f'{open_weather_works.location_temperature = }', end='\n\n')

    print(f'{open_weather_works.get_lat_and_lot_by_city('Moscow')=}')
    print(f'{open_weather_works.location_name = }')
    print(f'{open_weather_works.location_temperature = }', end='\n\n')

    # open_weather_works.get_weather_by_city_and_country('London', 'UK')
    # open_weather_works.get_weather_by_city('Moscow')
