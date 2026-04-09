from django.contrib.auth.hashers import make_password
from django.forms import ValidationError
from django.http import HttpRequest
from django.test import SimpleTestCase, TestCase

from weatherapp.forms import (
    LoginForm, SignUpForm, SearchLocationForm, DeleteLocationForm, AddLocationByLatAndLonForm)
from weatherapp.models import User
from weatherapp.settings import LOCATION_NAME_MAX_LENGTH
from weatherapp.settings import FORM_PRINTS


class TestLoginFormUserLoginFieldValidators(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create(
            login='Ivan',
            password=make_password('1234'),
        )

    def test_user_login_required_validator(self) -> None:
        login_form: LoginForm = LoginForm({
            'user_login': 'Ivan',
            'user_password': '1234'
        })

        self.assertTrue(login_form.is_valid())

        login_form: LoginForm = LoginForm({
            'user_login': '',
            'user_password': '1234'
        })
        self.assertFalse(login_form.is_valid())
        self.assertIn('user_login', login_form.errors)
        self.assertEqual(
            login_form.errors['user_login'][0], FORM_PRINTS['login_required_error_msg'])

    def test_user_login_min_length_validator(self) -> None:
        login_form: LoginForm = LoginForm({
            'user_login': 'Ivan',
            'user_password': '1234'
        })
        self.assertTrue(login_form.is_valid())

        login_form: LoginForm = LoginForm({
            'user_login': 'Iva',
            'user_password': '1234'
        })
        self.assertFalse(login_form.is_valid())
        self.assertIn('user_login', login_form.errors)
        self.assertEqual(
            login_form.errors['user_login'][0], FORM_PRINTS['login_min_length_error_msg'])

    def test_user_login_max_length_validator(self) -> None:
        self.user.login = 'I'*20
        self.user.save()
        login_form: LoginForm = LoginForm({
            'user_login': 'I'*20,
            'user_password': '1234'
        })
        self.assertTrue(login_form.is_valid())

        login_form: LoginForm = LoginForm({
            'user_login': 'I'*21,
            'user_password': '1234'
        })
        self.assertFalse(login_form.is_valid())
        self.assertIn('user_login', login_form.errors)
        self.assertEqual(
            login_form.errors['user_login'][0], FORM_PRINTS['login_max_length_error_msg'])

    def test_user_login_acceptable_characters_validator(self) -> None:
        login_form: LoginForm = LoginForm({
            'user_login': 'Ivan',
            'user_password': '1234'
        })
        self.assertTrue(login_form.is_valid())

        login_form: LoginForm = LoginForm({
            'user_login': 'Ivan*',
            'user_password': '1234'
        })

        self.assertFalse(login_form.is_valid())
        self.assertIn('user_login', login_form.errors)
        self.assertEqual(
            login_form.errors['user_login'][0], FORM_PRINTS['login_validation_error_msg'])


class TestLoginFormUserPasswordFieldValidators(TestCase):
    def setUp(self) -> None:
        self.user: User = User.objects.create(
            login='Ivan',
            password=make_password('1234'),
        )

    def test_user_password_required_validator(self) -> None:
        login_form: LoginForm = LoginForm({
            'user_login': 'Ivan',
            'user_password': '1234'
        })
        self.assertTrue(login_form.is_valid())

        login_form: LoginForm = LoginForm({
            'user_login': 'Ivan',
            'user_password': ''
        })
        self.assertFalse(login_form.is_valid())
        self.assertIn('user_password', login_form.errors)
        self.assertEqual(
            login_form.errors['user_password'][0], FORM_PRINTS['password_required_error_msg'])

    def test_user_password_min_length_validator(self) -> None:
        login_form: LoginForm = LoginForm({
            'user_login': 'Ivan',
            'user_password': '1234'
        })
        self.assertTrue(login_form.is_valid())

        login_form: LoginForm = LoginForm({
            'user_login': 'Ivan',
            'user_password': '123'
        })
        self.assertFalse(login_form.is_valid())
        self.assertIn('user_password', login_form.errors)
        self.assertEqual(
            login_form.errors['user_password'][0], FORM_PRINTS['password_min_length_error_msg'])

    def test_user_password_max_length_validator(self) -> None:
        self.user.password = make_password('1'*20)
        self.user.save()
        login_form: LoginForm = LoginForm({
            'user_login': 'Ivan',
            'user_password': '1'*20
        })
        self.assertTrue(login_form.is_valid())

        login_form: LoginForm = LoginForm({
            'user_login': 'Ivan',
            'user_password': '1'*21
        })
        self.assertFalse(login_form.is_valid())
        self.assertIn('user_password', login_form.errors)
        self.assertEqual(
            login_form.errors['user_password'][0], FORM_PRINTS['password_max_length_error_msg'])


class TestLoginFormBeyondFieldsValidators(TestCase):
    def setUp(self) -> None:
        self.user: User = User.objects.create(
            login='Ivan',
            password=make_password('1234'),
        )

    def test_login_exists_validator(self) -> None:
        login_form: LoginForm = LoginForm({
            'user_login': 'Ivan',
            'user_password': '1234'
        })
        self.assertTrue(login_form.is_valid())

        login_form: LoginForm = LoginForm({
            'user_login': 'Ivann',
            'user_password': '1234'
        })
        self.assertFalse(login_form.is_valid())
        self.assertIn('__all__', login_form.errors)
        self.assertEqual(
            login_form.errors['__all__'][0], FORM_PRINTS['login_does_not_exist'])

    def test_password_correct_validator(self) -> None:
        login_form: LoginForm = LoginForm({
            'user_login': 'Ivan',
            'user_password': '1234'
        })
        self.assertTrue(login_form.is_valid())

        login_form: LoginForm = LoginForm({
            'user_login': 'Ivan',
            'user_password': '12345'
        })
        self.assertFalse(login_form.is_valid())
        self.assertIn('__all__', login_form.errors)
        self.assertEqual(
            login_form.errors['__all__'][0], FORM_PRINTS['password_wrong_password'])


class TestSignUpFormUserLoginValidators(TestCase):
    def test_user_login_required_validator(self) -> None:
        signup_form: SignUpForm = SignUpForm({
            'user_login': 'Ivan',
            'user_password': '1234',
            'user_password_confirm': '1234',
        })
        self.assertTrue(signup_form.is_valid())

        signup_form: SignUpForm = SignUpForm({
            'user_login': '',
            'user_password': '1234',
            'user_password_confirm': '1234',
        })
        self.assertFalse(signup_form.is_valid())
        self.assertIn('user_login', signup_form.errors)
        self.assertEqual(
            signup_form.errors['user_login'][0], FORM_PRINTS['login_required_error_msg'])

    def test_user_login_min_length_validator(self) -> None:
        signup_form: SignUpForm = SignUpForm({
            'user_login': 'Ivan',
            'user_password': '1234',
            'user_password_confirm': '1234',
        })
        self.assertTrue(signup_form.is_valid())

        signup_form: SignUpForm = SignUpForm({
            'user_login': 'Iva',
            'user_password': '1234',
            'user_password_confirm': '1234',
        })
        self.assertFalse(signup_form.is_valid())
        self.assertIn('user_login', signup_form.errors)
        self.assertEqual(
            signup_form.errors['user_login'][0], FORM_PRINTS['login_min_length_error_msg'])

    def test_user_login_max_length_validator(self) -> None:
        signup_form: SignUpForm = SignUpForm({
            'user_login': 'I'*20,
            'user_password': '1234',
            'user_password_confirm': '1234',
        })
        self.assertTrue(signup_form.is_valid())

        signup_form: SignUpForm = SignUpForm({
            'user_login': 'I'*21,
            'user_password': '1234',
            'user_password_confirm': '1234',
        })
        self.assertFalse(signup_form.is_valid())
        self.assertIn('user_login', signup_form.errors)
        self.assertEqual(
            signup_form.errors['user_login'][0], FORM_PRINTS['login_max_length_error_msg'])

    def test_user_login_acceptable_characters_validator(self) -> None:
        signup_form: SignUpForm = SignUpForm({
            'user_login': 'Ivan',
            'user_password': '1234',
            'user_password_confirm': '1234',
        })
        self.assertTrue(signup_form.is_valid())

        signup_form: SignUpForm = SignUpForm({
            'user_login': '*Ivan',
            'user_password': '1234',
            'user_password_confirm': '1234',
        })
        self.assertFalse(signup_form.is_valid())
        self.assertIn('user_login', signup_form.errors)
        self.assertEqual(
            signup_form.errors['user_login'][0], FORM_PRINTS['login_validation_error_msg'])


class TestSignUpFormUserPasswordValidators(TestCase):
    def test_user_password_required_validator(self) -> None:
        signup_form: SignUpForm = SignUpForm({
            'user_login': 'Ivan',
            'user_password': '1234',
            'user_password_confirm': '1234',
        })
        self.assertTrue(signup_form.is_valid())

        signup_form: SignUpForm = SignUpForm({
            'user_login': 'Ivan',
            'user_password': '',
            'user_password_confirm': '1234',
        })
        self.assertFalse(signup_form.is_valid())
        self.assertIn('user_password', signup_form.errors)
        self.assertEqual(
            signup_form.errors['user_password'][0], FORM_PRINTS['password_required_error_msg'])

    def test_user_password_min_length_validator(self) -> None:
        signup_form: SignUpForm = SignUpForm({
            'user_login': 'Ivan',
            'user_password': '1234',
            'user_password_confirm': '1234',
        })
        self.assertTrue(signup_form.is_valid())

        signup_form: SignUpForm = SignUpForm({
            'user_login': 'Ivan',
            'user_password': '123',
            'user_password_confirm': '1234',
        })
        self.assertFalse(signup_form.is_valid())
        self.assertIn('user_password', signup_form.errors)
        self.assertEqual(
            signup_form.errors['user_password'][0], FORM_PRINTS['password_min_length_error_msg'])

    def test_user_password_max_length_validator(self) -> None:
        signup_form: SignUpForm = SignUpForm({
            'user_login': 'Ivan',
            'user_password': 'I'*20,
            'user_password_confirm': 'I'*20,
        })
        self.assertTrue(signup_form.is_valid())

        signup_form: SignUpForm = SignUpForm({
            'user_login': 'Ivan',
            'user_password': 'I'*21,
            'user_password_confirm': '1234',
        })
        self.assertFalse(signup_form.is_valid())
        self.assertIn('user_password', signup_form.errors)
        self.assertEqual(
            signup_form.errors['user_password'][0], FORM_PRINTS['password_max_length_error_msg'])


class TestSignUpFormUserPasswordConfirValidators(TestCase):
    def test_user_password_required_validator(self) -> None:
        signup_form: SignUpForm = SignUpForm({
            'user_login': 'Ivan',
            'user_password': '1234',
            'user_password_confirm': '1234',
        })
        self.assertTrue(signup_form.is_valid())

        signup_form: SignUpForm = SignUpForm({
            'user_login': 'Ivan',
            'user_password': '1234',
            'user_password_confirm': '',
        })
        self.assertFalse(signup_form.is_valid())
        self.assertIn('user_password_confirm', signup_form.errors)
        self.assertEqual(signup_form.errors['user_password_confirm']
                         [0], FORM_PRINTS['password_required_error_msg'])

    def test_user_password_min_length_validator(self) -> None:
        signup_form: SignUpForm = SignUpForm({
            'user_login': 'Ivan',
            'user_password': '1234',
            'user_password_confirm': '1234',
        })
        self.assertTrue(signup_form.is_valid())

        signup_form: SignUpForm = SignUpForm({
            'user_login': 'Ivan',
            'user_password': '1234',
            'user_password_confirm': '123',
        })
        self.assertFalse(signup_form.is_valid())
        self.assertIn('user_password_confirm', signup_form.errors)
        self.assertEqual(signup_form.errors['user_password_confirm']
                         [0], FORM_PRINTS['password_min_length_error_msg'])

    def test_user_password_max_length_validator(self) -> None:
        signup_form: SignUpForm = SignUpForm({
            'user_login': 'Ivan',
            'user_password': 'I'*20,
            'user_password_confirm': 'I'*20,
        })
        self.assertTrue(signup_form.is_valid())

        signup_form: SignUpForm = SignUpForm({
            'user_login': 'Ivan',
            'user_password': '1234',
            'user_password_confirm': 'I'*21,
        })
        self.assertFalse(signup_form.is_valid())
        self.assertIn('user_password_confirm', signup_form.errors)
        self.assertEqual(signup_form.errors['user_password_confirm']
                         [0], FORM_PRINTS['password_max_length_error_msg'])


class TestSignUpFormBeyondFieldsValidators(TestCase):
    def test_user_password_confirm_validator(self) -> None:
        signup_form: SignUpForm = SignUpForm({
            'user_login': 'Ivan',
            'user_password': '1234',
            'user_password_confirm': '1234',
        })
        self.assertTrue(signup_form.is_valid())

        signup_form: SignUpForm = SignUpForm({
            'user_login': 'Ivan',
            'user_password': '1234',
            'user_password_confirm': '12345',
        })
        self.assertFalse(signup_form.is_valid())
        self.assertIn('__all__', signup_form.errors)
        self.assertEqual(
            signup_form.errors['__all__'][0], FORM_PRINTS['password_confirm_error_msg'])

    def test_user_not_exists_validator(self) -> None:
        User.objects.create(
            login='Ivan',
            password=make_password('1234'),
        )
        signup_form: SignUpForm = SignUpForm({
            'user_login': 'Ioan',
            'user_password': '1234',
            'user_password_confirm': '1234',
        })
        self.assertTrue(signup_form.is_valid())

        signup_form: SignUpForm = SignUpForm({
            'user_login': 'Ivan',
            'user_password': '1234',
            'user_password_confirm': '1234',
        })
        self.assertFalse(signup_form.is_valid())
        self.assertIn('__all__', signup_form.errors)
        self.assertEqual(
            signup_form.errors['__all__'][0], FORM_PRINTS['user_already_exists_error'])


class TestSearchLocationFormLocationNameFieldValidators(TestCase):
    def setUp(self) -> None:
        self.regular_name: str = 'Vladivostok'
        self.empty_name: str = ''
        self.almost_too_long_name: str = 'I'*255
        self.too_long_name: str = 'I'*256

    def test_location_name_success_validation(self) -> None:
        search_location_form = SearchLocationForm({
            'location_name': self.regular_name
        })
        self.assertTrue(search_location_form.is_valid())

    def test_location_name_required_validator(self) -> None:
        search_location_form = SearchLocationForm({})
        self.assertFalse(search_location_form.is_valid())

        search_location_form = SearchLocationForm({
            'location_name': self.empty_name
        })
        self.assertFalse(search_location_form.is_valid())
        self.assertIn('location_name', search_location_form.errors)
        self.assertEqual(
            search_location_form.errors['location_name'][0], FORM_PRINTS['field_required_error_msg'])

    def test_location_name_max_length_validator(self) -> None:
        search_location_form = SearchLocationForm({
            'location_name': self.almost_too_long_name
        })
        self.assertTrue(search_location_form.is_valid())

        search_location_form = SearchLocationForm({
            'location_name': self.too_long_name
        })
        self.assertFalse(search_location_form.is_valid())
        self.assertIn('location_name', search_location_form.errors)
        self.assertEqual(
            search_location_form.errors['location_name'][0], FORM_PRINTS['location_name_max_length_error_msg'])


class TestAddLocationByLatAndLonFormValidation(SimpleTestCase):
    def setUp(self) -> None:
        self.empty_lat = ''
        self.normal_lat = '1'*FORM_PRINTS['location_lat_max_length']
        self.too_long_lat = '1'*(FORM_PRINTS['location_lat_max_length'] + 1)

        self.empty_lon = ''
        self.normal_lon = '1'*(FORM_PRINTS['location_lon_max_length'] - 1)
        self.long_lon = '1'*FORM_PRINTS['location_lon_max_length']

    def test_lat_field_required_validation(self):
        add_location_by_lat_and_lon: AddLocationByLatAndLonForm = AddLocationByLatAndLonForm({
            'lon': self.normal_lon
        })

        self.assertFalse(add_location_by_lat_and_lon.is_valid())
        self.assertIn('lat', add_location_by_lat_and_lon.errors)
        self.assertEqual(
            add_location_by_lat_and_lon.errors['lat'][0], FORM_PRINTS['location_lat_required_error_msg'])

    def test_lat_field_max_length_validation(self):
        add_location_by_lat_and_lon: AddLocationByLatAndLonForm = AddLocationByLatAndLonForm({
            'lat': self.too_long_lat,
            'lon': self.normal_lon
        })
        self.assertFalse(add_location_by_lat_and_lon.is_valid())
        self.assertIn('lat', add_location_by_lat_and_lon.errors)
        self.assertEqual(
            add_location_by_lat_and_lon.errors['lat'][0], FORM_PRINTS['location_lat_max_length_error_msg'])

    def test_lat_field_success_validation(self):
        add_location_by_lat_and_lon: AddLocationByLatAndLonForm = AddLocationByLatAndLonForm({
            'lat': self.normal_lat,
            'lon': self.normal_lon
        })
        self.assertTrue(add_location_by_lat_and_lon.is_valid())
        self.assertNotIn('lat', add_location_by_lat_and_lon.errors)
#####
    def test_lon_field_required_validation(self):
        add_location_by_lat_and_lon: AddLocationByLatAndLonForm = AddLocationByLatAndLonForm({
            'lat': self.normal_lat
        })

        self.assertFalse(add_location_by_lat_and_lon.is_valid())
        self.assertIn('lon', add_location_by_lat_and_lon.errors)
        self.assertEqual(
            add_location_by_lat_and_lon.errors['lon'][0], FORM_PRINTS['location_lon_required_error_msg'])

    def test_lon_field_max_length_validation(self):
        add_location_by_lat_and_lon: AddLocationByLatAndLonForm = AddLocationByLatAndLonForm({
            'lat': self.normal_lon,
        })
        self.assertFalse(add_location_by_lat_and_lon.is_valid())
        self.assertIn('lon', add_location_by_lat_and_lon.errors)
        self.assertEqual(
            add_location_by_lat_and_lon.errors['lon'][0], FORM_PRINTS['location_lon_required_error_msg'])

    def test_lon_field_success_validation(self):
        add_location_by_lat_and_lon: AddLocationByLatAndLonForm = AddLocationByLatAndLonForm({
            'lat': self.normal_lon,
            'lon': self.normal_lat,
        })
        self.assertTrue(add_location_by_lat_and_lon.is_valid())
        self.assertNotIn('lon', add_location_by_lat_and_lon.errors)

# class TestAddLocationFormLocationNameValidators(TestCase):
#     def setUp(self) -> None:
#         self.user: User = User.objects.create(
#             login='Ivan',
#             password=make_password('1234'),
#         )

#     def test_location_name_required_validator(self) -> None:
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
#         add_location_form: AddLocationForm = AddLocationForm({
#             'location_name': 'Moscow'
#         },
#             request=request
#         )
#         self.assertTrue(add_location_form.is_valid())

#         add_location_form: AddLocationForm = AddLocationForm({
#             'location_name': '',
#         },
#             request=request
#         )
#         self.assertFalse(add_location_form.is_valid())
#         self.assertIn('location_name', add_location_form.errors)
#         self.assertIn('__all__', add_location_form.errors)
#         self.assertEqual(
#             add_location_form.errors['location_name'][0], FORM_PRINTS['field_required_error_msg'])
#         self.assertEqual(
#             add_location_form.errors['__all__'][0], FORM_PRINTS['location_addition_error'])

#     def test_location_name_max_length_validator(self) -> None:
#         request: HttpRequest = HttpRequest()
#         request.session = {}
#         request.session['user_id'] = self.user.pk
#         request.session['location_info'] = {
#             'api_response_code': '200',
#             'location_name': 'I'*255,
#             'country_code': 'RU',
#             'location_temperature': '-10',
#             'location_lat': 37.6156,
#             'location_lon': 55.7522,
#         }
#         add_location_form: AddLocationForm = AddLocationForm({
#             'location_name': 'I'*255
#         },
#             request=request
#         )
#         self.assertTrue(add_location_form.is_valid())

#         add_location_form: AddLocationForm = AddLocationForm({
#             'location_name': 'I'*256,
#         },
#             request=request,
#         )
#         self.assertFalse(add_location_form.is_valid())
#         self.assertIn('location_name', add_location_form.errors)
#         self.assertEqual(add_location_form.errors['location_name']
#                          [0], FORM_PRINTS['location_name_max_length_error_msg'])
#         self.assertIn('__all__', add_location_form.errors)
#         self.assertEqual(
#             add_location_form.errors['__all__'][0], FORM_PRINTS['location_addition_error'])


# class TestAddLocationFormBeyondFieldsValidators(TestCase):
#     def setUp(self) -> None:
#         self.user: User = User.objects.create(
#             login='Ivan',
#             password=make_password('1234'),
#         )

#     def test_location_location_info_exists_validator(self) -> None:
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
#         add_location_form: AddLocationForm = AddLocationForm({
#             'location_name': 'Moscow'
#         },
#             request=request
#         )
#         self.assertTrue(add_location_form.is_valid())

#         del request.session['location_info']
#         add_location_form: AddLocationForm = AddLocationForm({
#             'location_name': 'Moscow'
#         },
#             request=request
#         )
#         self.assertFalse(add_location_form.is_valid())
#         self.assertIn('__all__', add_location_form.errors)
#         self.assertEqual(
#             add_location_form.errors['__all__'][0], FORM_PRINTS['location_addition_error'])

#     def test_location_name_exists_validator(self) -> None:
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
#         add_location_form: AddLocationForm = AddLocationForm({
#             'location_name': 'Moscow'
#         },
#             request=request
#         )
#         self.assertTrue(add_location_form.is_valid())

#         del request.session['location_info']['location_name']
#         add_location_form: AddLocationForm = AddLocationForm({
#             'location_name': 'Moscow'
#         },
#             request=request
#         )
#         self.assertFalse(add_location_form.is_valid())
#         self.assertIn('__all__', add_location_form.errors)
#         self.assertEqual(
#             add_location_form.errors['__all__'][0], FORM_PRINTS['location_addition_error'])

#     def test_location_location_info_exists_validator(self) -> None:
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
#         add_location_form: AddLocationForm = AddLocationForm({
#             'location_name': 'Moscow'
#         },
#             request=request
#         )
#         self.assertTrue(add_location_form.is_valid())
#         add_location_form: AddLocationForm = AddLocationForm({
#             'location_name': 'Moscoww'
#         },
#             request=request
#         )
#         self.assertFalse(add_location_form.is_valid())
#         self.assertIn('__all__', add_location_form.errors)
#         self.assertEqual(
#             add_location_form.errors['__all__'][0], FORM_PRINTS['location_addition_error'])


class TestDeleteLocationFormLocationNameFieldValidation(SimpleTestCase):
    def test_location_name_required_validator(self) -> None:
        delete_location_form: DeleteLocationForm = DeleteLocationForm({
            'location_name': 'Moscow'
        })
        self.assertTrue(delete_location_form.is_valid())

        delete_location_form: DeleteLocationForm = DeleteLocationForm({
            'location_name': ''
        })
        self.assertFalse(delete_location_form.is_valid())
        self.assertIn('location_name', delete_location_form.errors)
        self.assertEqual(
            delete_location_form.errors['location_name'][0], FORM_PRINTS['field_required_error_msg'])

        delete_location_form: DeleteLocationForm = DeleteLocationForm({})
        self.assertFalse(delete_location_form.is_valid())
        self.assertIn('location_name', delete_location_form.errors)
        self.assertEqual(
            delete_location_form.errors['location_name'][0], FORM_PRINTS['field_required_error_msg'])

    def test_location_name_max_length_validator(self) -> None:
        delete_location_form: DeleteLocationForm = DeleteLocationForm({
            'location_name': 'M' * LOCATION_NAME_MAX_LENGTH
        })
        self.assertTrue(delete_location_form.is_valid())

        delete_location_form: DeleteLocationForm = DeleteLocationForm({
            'location_name': 'm' * (1+LOCATION_NAME_MAX_LENGTH)
        })
        self.assertFalse(delete_location_form.is_valid())
        self.assertIn('location_name', delete_location_form.errors)
        self.assertEqual(
            delete_location_form.errors['location_name'][0], FORM_PRINTS['location_name_max_length_error_msg'])
