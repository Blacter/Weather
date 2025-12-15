from contextlib import nullcontext

import pytest
from django.test import TestCase

from .type_aliaces import Lat, Lon
from .open_weather_works import OpenWeatherWorks

# Create your tests here.
class TestOpenWeatherWorks:
    @pytest.mark.parametrize(
        'city, res_lat, res_lon',
        [
            ('London', 51.5085, -0.1257),
            ('Moscow', 55.7522, 37.6156),
            ('Paris', 48.8534, 2.3488),
            ('Warsaw', 52.2298, 21.0118),
            ('Praga', 50.088, 14.4208), # ['Praga'-50.088-14.4208]
        ]
    )
    def test_get_lat_and_lot_by_city(self, city: str, res_lat: Lat, res_lon: Lon) -> None:
        assert OpenWeatherWorks().get_lat_and_lot_by_city(city) == (res_lat, res_lon)
    
    @pytest.mark.parametrize(
        'city, res_type',
        [
            ('London', int),
            ('Moscow', int),
            ('Paris', int),
            ('Warsaw', int),
            ('Praga', int),
        ]
    )
    def test_temperature_by_city(self, city: str, res_type) -> None:
        lat, lon = OpenWeatherWorks().get_lat_and_lot_by_city(city)
        temperature = OpenWeatherWorks().get_temperature_in_celcius_by_lat_and_lon(lat, lon)
        with nullcontext():
            assert int(temperature)