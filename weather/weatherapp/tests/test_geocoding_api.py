from django.conf import settings
from django.test import SimpleTestCase

from weatherapp.geocoding_api import GeocodingAPI

class TestGeocodingAPI(SimpleTestCase):
    def test_get_cities_by_name(self) -> None:
        geocoding_api: GeocodingAPI = GeocodingAPI(settings.APPID)
        cities = geocoding_api.get_cities_by_name('Moscow')
        


