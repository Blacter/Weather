from pprint import pprint
from string import Template
from typing import Any

import requests
from requests.exceptions import RequestException

from weatherapp.settings import OPEN_WEATHER_PRINTS, GEOCODING_PRINTS

# APPID: str = "036c7b1114a05396ffe3dedefcffa484"

# GEOCODING_PRINTS: dict[str, str | Template] = {
#     'cities_by_name_and_country_code': Template(f'http://api.openweathermap.org/geo/1.0/direct?q=$city_name,$country_code&limit=$limit&appid={{APPID}}'),
#     'cities_by_name': Template(f'http://api.openweathermap.org/geo/1.0/direct?q=$city_name&limit=$limit&appid={APPID}'),
#     'limit': 5,
# }

SCHEME = {
    'location_name': 'name',
    'country_code': 'country',
    'location_lat': 'lat',
    'location_lon': 'lon',
}


class GeocodingAPI:
    def __init__(self, app_id: str):
        self._app_id: str = app_id
        self._cities_by_name_url: Template = GEOCODING_PRINTS['cities_by_name']
        self._cities_info: list[dict] | None = None
        self._error_msg: str | None = None
        self._response_status_code: int | None = None

    @property
    def error_msg(self) -> str:
        return self._error_msg

    @property
    def response_status_code(self) -> int | None:
        return self._response_status_code

    def get_cities_by_name(self, name) -> list[dict] | None:
        self._city_to_get: str = name
        try:
            self._get_cities_by_name()
        except RequestException:
            self._cities_info = None
        return self._cities_info

    def _get_cities_by_name(self) -> None:
        self._geocoding_response: requests.Response | None = None

        try:
            self._geocoding_response = requests.get(
                self._cities_by_name_url.substitute(
                    city_name=self._city_to_get,
                    limit=GEOCODING_PRINTS['limit'],
                )
            )

            if self._geocoding_response is None:
                self._error_msg = 'No response'
                raise RequestException

            self._response_status_code = self._geocoding_response.status_code

            if self._response_status_code // 100 != 2:
                self._error_msg = self._geocoding_response.json().get('message')
                raise RequestException
        except RequestException:
            raise

        self._parse_cities_data()

    def _parse_cities_data(self) -> None:
        cities_in_response = self._geocoding_response.json()
        self._cities_info = []
        for self._city_in_response in cities_in_response:
            self._get_city_info_by_scheme()
            self._cities_info.append(self._city_info)

    def _get_city_info_by_scheme(self) -> dict:
        self._city_info: dict = {}
        for key_for_dict, value_of_json_key in SCHEME.items():
            self._city_info[key_for_dict] = self._city_in_response.get(
                value_of_json_key)


if __name__ == '__main__':
    appid: str = "036c7b1114a05396ffe3dedefcffa484"
    geocoding_api: GeocodingAPI = GeocodingAPI(appid)
    cities_info: list[dict] = geocoding_api.get_cities_by_name('Moscw')
    error_msg = geocoding_api.error_msg
    print(f'{error_msg=}')
    pprint(cities_info)
