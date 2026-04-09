from typing import Any

from collections import namedtuple
from typing import TypeAlias

Lat: TypeAlias = str
Lon: TypeAlias = str

WeatherInfo = namedtuple('WeatherInfo', ['location_name', 'temperature', 'country_code'])
type WeatherInfoList = list[WeatherInfo]
type StatusCode = int | None
type LocationsInfoNotNull = list[dict[str, Any]]
type LocationsInfo = list[dict[str, Any]] | None
