from contextlib import nullcontext as does_not_raise
from pprint import pprint
from typing import Any
from unittest.mock import patch

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.db.utils import OperationalError
from django.http import HttpResponse, HttpRequest
from django.templatetags.static import static
from django.test import override_settings
from django.test import TestCase, SimpleTestCase, Client
from django.urls import reverse
from jinja2 import Environment, FileSystemLoader, Template

from weatherapp.settings import FORM_PRINTS
from weatherapp.forms import LoginForm
from weatherapp import views
from weatherapp.models import User, Session
from weatherapp.type_aliaces import WeatherInfo
from weatherapp.type_aliaces import WeatherInfoList


class TestIndexView(SimpleTestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.index_url = reverse('home')

    def test_without_login(self) -> None:
        response = self.client.get(self.index_url)
        self.assertEqual(response.status_code, 200)


class TestLoginView(TestCase):
    def setUp(self) -> None:
        self.correct_login_data = {
            'user_login': 'Anna',
            'user_password': '1234'
        }
        User.objects.create(
            login=self.correct_login_data['user_login'],
            password=make_password(self.correct_login_data['user_password']),
        )

        self.incorrect_login_data = {
            'user_login': 'Ivan',
            'user_password': 'qwer'
        }

        self.client = Client()
        self.login_url = reverse('login')

    def test_get_request_to_login_view(self) -> None:
        response = self.client.get(self.login_url)

        self.assertEqual(200, response.status_code)
        self.assertEqual(0, Session.objects.count())

    @override_settings(DEBUG=True, FORCED_LOGIN=True)
    def test_get_login_by_logged_in_user(self) -> None:
        response = self.client.get(self.login_url)
        self.assertEqual(302, response.status_code)
        self.assertEqual(reverse('home'), response.headers['Location'])

    def test_success_login(self) -> None:
        response = self.client.post(
            self.login_url,
            data=self.correct_login_data,
            follow=False,
        )

        self.assertEqual(302, response.status_code)
        self.assertEqual(reverse('home'), response.headers['Location'])

        self.assertIn('login', response.cookies)
        self.assertIn('session_id_custom', response.cookies)

        self.assertEqual(1,  Session.objects.count())
        self.assertEqual(
            self.correct_login_data['user_login'], Session.objects.first().user_id.login)

    def test_login_in_unexisting_profile(self) -> None:
        response = self.client.post(
            self.login_url,
            data=self.incorrect_login_data,
        )
        sessions = Session.objects.all()

        self.assertContains(response,
                            FORM_PRINTS['login_does_not_exist'],
                            status_code=400)
        self.assertEqual(0, len(sessions))

    def test_login_with_wrong_password(self) -> None:
        response = self.client.post(
            self.login_url,
            data={
                'user_login': self.correct_login_data['user_login'],
                'user_password': self.incorrect_login_data['user_password']
            },
        )

        self.assertContains(response,
                            FORM_PRINTS['password_wrong_password'],
                            status_code=400)

        self.assertEqual(0, Session.objects.count())

    def test_login_with_empty_post(self) -> None:
        response = self.client.post(
            self.login_url,
            data={}
        )

        self.assertContains(response,
                            FORM_PRINTS['login_required_error_msg'],
                            status_code=400)

    @patch('weatherapp.views.do_login')
    def test_login_with_operational_error(self, mock_login) -> None:
        mock_login.side_effect = OperationalError()
        response = self.client.post(
            self.login_url,
            data=self.correct_login_data,
        )

        self.assertContains(response,
                            FORM_PRINTS['server_error'],
                            status_code=500)
        self.assertEqual(0, Session.objects.count())
        mock_login.assert_called()

