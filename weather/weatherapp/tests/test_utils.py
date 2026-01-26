from django.contrib.auth.hashers import make_password
from django.http import HttpRequest
from django.test import TestCase

from weatherapp.models import Location, User
from weatherapp.utils import do_add_location

class TestAddLocationUtilsSuccess(TestCase):
    def setUp(self) -> None:
        self.user: User = User.objects.create(
            login='Ivan',
            password=make_password('1234'),
        )
        
    def test_location_add_success(self) -> None:
        request: HttpRequest = HttpRequest()
        request.session = {}
        request.session['user_id'] = self.user.pk
        request.session['location_info'] = {
            'api_response_code': '200',
            'location_name': 'Moscow',
            'country_code': 'RU',
            'location_temperature': '-10',
            'location_lat': 37.6156,
            'location_lon': 55.7522,
        }
        do_add_location(request)
        try: 
            added_location: Location = Location.objects.get(
                user_id=self.user.pk,
                name=request.session['location_info']['location_name']
            )
        except Location.DoesNotExist:
            self.fail('add location utils error')
            
        self.assertEqual(added_location.user_id.pk, self.user.pk)
        self.assertEqual(added_location.name, request.session['location_info']['location_name'])
        