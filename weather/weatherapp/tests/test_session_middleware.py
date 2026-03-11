import json
from random import randint
from unittest.mock import Mock

from django.http import HttpResponse
from django.test import TestCase
from mock import Mock

from weatherapp.models import User  # , Session
from weatherapp.session.session import SessionService
from weatherapp.session.middleware import CustomSessionMiddleware


class TestSessionMiddlewareGetExistsSession(TestCase):  # Set Session

    def setUp(self):
        self.USER_NAME: str = 'Lisa'

        User.objects.create(
            login='Lisa',
            password='1234'
        )
        session_service: SessionService = SessionService(
            user_login=self.USER_NAME
        )
        self.random_number: int = randint(1, 100)
        session_service.set_session_user_data({'key1': self.random_number})

        self.request = Mock()

        self.request.COOKIES = {
            'login': self.USER_NAME,
            'custom_session_id': str(session_service.get_session_id())
        }

    def test_get_existing_session_with_data(self) -> None:

        self.session_middleware: CustomSessionMiddleware = CustomSessionMiddleware(
            lambda x: HttpResponse())

        self.session_middleware(self.request)

        self.assertIn('session_service', self.request.__dict__)
        self.assertEqual(
            self.request.session_service.get_session_user_data(),
            {'key1': self.random_number}
        )
