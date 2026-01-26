from collections import namedtuple
from typing import TypeAlias

Lat: TypeAlias = str
Lon: TypeAlias = str

WeatherInfo = namedtuple('WeatherInfo', ['location_name', 'temperature', 'country_code'])
type WeatherInfoList = list[WeatherInfo]