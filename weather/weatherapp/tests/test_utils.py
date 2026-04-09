import json
from unittest.mock import patch
from urllib.parse import urlparse

from django.contrib.auth.hashers import make_password
from django.http import HttpRequest
from django.test import TestCase, SimpleTestCase

from weatherapp.forms import AddLocationByLatAndLonForm
from weatherapp.type_aliaces import WeatherInfo, WeatherInfoList
from weatherapp.models import Location, User
from weatherapp.utils import get_forms_to_add_locations, get_weather_info_list, do_add_location


# class TestAddLocationUtilsSuccess(TestCase):
#     def setUp(self) -> None:
#         self.user: User = User.objects.create(
#             login='Ivan',
#             password=make_password('1234'),
#         )

#     def test_location_add_success(self) -> None:
#         request: HttpRequest = HttpRequest()
#         request.session = {}
#         request.session['user_id'] = self.user.pk
#         request.session['location_info'] = {
#             'api_response_code': '200',
#             'location_name': 'Moscow',
#             'country_code': 'RU',
#             'location_temperature': '-10',
#             'location_lat': 37.6156,
#             'location_lon': 55.7522,
#         }
#         do_add_location(request)
#         try:
#             added_location: Location = Location.objects.get(
#                 user_id=self.user.pk,
#                 name=request.session['location_info']['location_name']
#             )
#         except Location.DoesNotExist:
#             self.fail('add location utils error')

#         self.assertEqual(added_location.user_id.pk, self.user.pk)
#         self.assertEqual(added_location.name,
#                          request.session['location_info']['location_name'])


class MockResponse:
    def __init__(self, json_data: dict, status_code: int) -> None:
        self.json_data = json_data
        self.status_code = status_code

    def json(self) -> dict:
        return self.json_data


def side_effect(request_url: str) -> str:
    city_name = urlparse(request_url).query.split('&')[0].split('=')[1]
    temperature_kelvin = 297.12
    country_code = 'PH'
    if city_name not in ['Volgograd', 'Moscow', 'Tver\'', 'Minsk', 'Paris', 'London']:
        return_data = {
            "cod": "404",
            "message": "city not found"
        }
    else:
        return_data = {
            "coord": {"lon": 123.6648, "lat": 12.644},
            "weather": [{
                "id": 801,
                "main": "Clouds",
                "description": "few clouds",
                "icon": "02n"
            }],
            "base": "stations",
            "main": {
                    "temp": temperature_kelvin,
                    "feels_like": 297.53,
                    "temp_min": 297.12,
                    "temp_max": 297.12,
                    "pressure": 1014,
                    "humidity": 75,
                    "sea_level": 1014,
                    "grnd_level": 1013
            },
            "visibility": 10000,
            "wind": {
                "speed": 5.4,
                "deg": 32,
                "gust": 9.53
            },
            "clouds": {"all": 17},
            "dt": 1769629152,
            "sys": {
                "country": country_code,
                "sunrise": 1769638287,
                "sunset": 1769679906
            },
            "timezone": 28800,
            "id": 1699310,
            "name": city_name,
            "cod": 200
        }
    return MockResponse(return_data, 404)


class TestGetWeatherInfoList(TestCase):
    @patch('weatherapp.open_weather_works.requests.get')
    def test_get_weather_info_list(self, mock_get) -> None:
        mock_get.side_effect = side_effect

        user_name: str = 'Ivan'
        user_password: str = '1234'
        location_names_list: list[str] = []
        lat: float = 10.0
        lon: float = 10.0
        weather_list_benchmark: WeatherInfoList = []
        temperature = '24'
        country_code = 'PH'

        user: User = User.objects.create(
            login=user_name, password=user_password)
        for location_name in location_names_list:
            Location.objects.create(
                name=location_name, user_id=user, latitude=lat, longitude=lon)
            weather_list_benchmark.append(WeatherInfo(
                location_name=location_name,
                temperature=temperature,
                country_code=country_code,
            ))

        weather_list = get_weather_info_list('Ivan', 1)
        self.assertEqual(weather_list, weather_list_benchmark)
        # mock_get.assert_called_with('https://api.openweathermap.org/data/2.5/weather')

    @patch('weatherapp.open_weather_works.requests.get')
    def test_get_weather_info_list_with_one_elements(self, mock_get) -> None:
        mock_get.side_effect = side_effect

        user_name: str = 'Ivan'
        user_password: str = '1234'
        location_names_list: list[str] = ['Volgograd']
        lat: float = 10.0
        lon: float = 10.0
        weather_list_benchmark: WeatherInfoList = []
        temperature = '24'
        country_code = 'PH'

        user: User = User.objects.create(
            login=user_name, password=user_password)
        for location_name in location_names_list:
            Location.objects.create(
                name=location_name, user_id=user, latitude=lat, longitude=lon)
            weather_list_benchmark.append(WeatherInfo(
                location_name=location_name,
                temperature=temperature,
                country_code=country_code,
            ))

        weather_list = get_weather_info_list('Ivan', 1)
        self.assertEqual(weather_list, weather_list_benchmark)
        # mock_get.assert_called_with('https://api.openweathermap.org/data/2.5/weather')

    @patch('weatherapp.open_weather_works.requests.get')
    def test_get_weather_info_list_with_two_elements(self, mock_get) -> None:
        mock_get.side_effect = side_effect

        user_name: str = 'Ivan'
        user_password: str = '1234'
        location_names_list: list[str] = ['Volgograd', 'Moscow']
        lat: float = 10.0
        lon: float = 10.0
        weather_list_benchmark: WeatherInfoList = []
        temperature = '24'
        country_code = 'PH'

        user: User = User.objects.create(
            login=user_name, password=user_password)
        for location_name in location_names_list:
            Location.objects.create(
                name=location_name, user_id=user, latitude=lat, longitude=lon)
            weather_list_benchmark.append(WeatherInfo(
                location_name=location_name,
                temperature=temperature,
                country_code=country_code,
            ))

        weather_list = get_weather_info_list('Ivan', 1)
        self.assertEqual(weather_list, weather_list_benchmark)
        # mock_get.assert_called_with('https://api.openweathermap.org/data/2.5/weather')

    @patch('weatherapp.open_weather_works.requests.get')
    def test_get_weather_info_list_with_six_elements(self, mock_get) -> None:
        mock_get.side_effect = side_effect

        user_name: str = 'Ivan'
        user_password: str = '1234'
        location_names_list: list[str] = [
            'Volgograd', 'Moscow', 'Tver\'', 'Minsk', 'Paris', 'London']
        lat: float = 10.0
        lon: float = 10.0
        weather_list_benchmark: WeatherInfoList = []
        temperature = '24'
        country_code = 'PH'

        user: User = User.objects.create(
            login=user_name, password=user_password)
        for location_name in location_names_list:
            Location.objects.create(
                name=location_name, user_id=user, latitude=lat, longitude=lon)
            weather_list_benchmark.append(WeatherInfo(
                location_name=location_name,
                temperature=temperature,
                country_code=country_code,
            ))

        weather_list = get_weather_info_list('Ivan', 1)
        self.assertEqual(weather_list, weather_list_benchmark)
        # mock_get.assert_called_with('https://api.openweathermap.org/data/2.5/weather')


class TestGetLocationsToAddForms(SimpleTestCase):
    def setUp(self) -> None:
        # set locations_info.
        self.initial_locations_info = [
            {
                'location_name': 'Liverpool',
                'country_code': 'GB',
                'location_lat': '53.4071991',
                'location_lon': '-2.99168'
            },
            {
                'location_name': 'Liverpool',
                'country_code': 'US',
                'location_lat': '29.2949612',
                'location_lon': '-95.2788231'
            },
            {
                'location_name': 'Liverpool',
                'country_code': 'US',
                'location_lat': '40.3917076',
                'location_lon': '-90.0009491'
            },
            {
                'location_name': 'Village of Liverpool',
                'country_code': 'US',
                'location_lat': '43.106456',
                'location_lon': '-76.217705'
            },
            {
                'location_name': 'Liverpool',
                'country_code': 'AU',
                'location_lat': '-33.9198252',
                'location_lon': '150.92566'
            },
        ]
        self.data_for_froms = [
            {
                'lat': '53.4071991',
                'lon': '-2.99168'
            },
            {
                'lat': '29.2949612',
                'lon': '-95.2788231'
            },
            {
                'lat': '40.3917076',
                'lon': '-90.0009491'
            },
            {
                'lat': '43.106456',
                'lon': '-76.217705'
            },
            {
                'lat': '-33.9198252',
                'lon': '150.92566'
            },
        ]
        self.benchmark_forms = [
            AddLocationByLatAndLonForm(self.data_for_froms[0]),
            AddLocationByLatAndLonForm(self.data_for_froms[1]),
            AddLocationByLatAndLonForm(self.data_for_froms[2]),
            AddLocationByLatAndLonForm(self.data_for_froms[3]),
        ]

    def test_get_empty_location_to_add_forms(self) -> None:
        result_forms = get_forms_to_add_locations(self.initial_locations_info)
        for benchmark_form, result_form in zip(self.benchmark_forms, result_forms):
            benchmark_form.is_valid()
            result_form.is_valid()

            self.assertEqual(
                benchmark_form.cleaned_data['lat'], result_form.cleaned_data['lat'])
            self.assertEqual(
                benchmark_form.cleaned_data['lon'], result_form.cleaned_data['lon'])
