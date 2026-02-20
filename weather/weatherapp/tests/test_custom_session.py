import json
import random

from contextlib import nullcontext as does_not_raise
from django.core.exceptions import ValidationError
from django.test import TestCase, TransactionTestCase
from django.db import transaction
from django.db import connection

from weatherapp.models import Session, User

from weatherapp.session.session import SessionService


class TestSessionCreate(TestCase):
    def setUp(self) -> None:
        User.objects.create(
            login='Lisa',
            password='1234'
        )

    def test_session_create(self) -> None:
        session_service: SessionService = SessionService(user_login='Lisa')
        session_id: str = session_service.get_session_id()
        with does_not_raise():
            created_session = Session.objects.get(id=session_id)
        with self.assertRaises(ValidationError):
            Session.objects.get(id="not valid uuid")
        with self.assertRaises(Session.DoesNotExist):
            Session.objects.get(id="80a1aae6-39ce-4c9a-9b93-24cd40c34690")


class TestGetSession(TestCase):
    def setUp(self) -> None:
        User.objects.create(
            login='Lisa',
            password='1234'
        )
        session_service: SessionService = SessionService(user_login='Lisa')
        self.session_id: str = session_service.get_session_id()
        del session_service

    def test_session_get(self) -> None:
        session_service: SessionService = SessionService(
            user_login='Lisa',
            session_id=self.session_id
        )
        session_data = session_service.get_session_user_data()

        self.assertEqual(self.session_id, session_service.get_session_id())
        self.assertIsNone(session_data)


class TestSetSessionUserData(TransactionTestCase):
    # def _post_teardown(self): # Для предотвращения удаления данных в БД после прохождения тестов.
    #     connection.set_autocommit(True)

    def setUp(self) -> None:
        User.objects.create(
            login='Lisa',
            password='1234'
        )
        session_service: SessionService = SessionService(user_login='Lisa')
        self.session_id: str = session_service.get_session_id()
        del session_service

    def test_set_session_user_data(self) -> None:
        session_service: SessionService = SessionService(
            user_login='Lisa',
            session_id=self.session_id
        )
        user_data = {
            'is_logged_in': True,
            'color_theme': 'Light',
            'randint': random.randint(0, 1000),
        }
        session_service.set_session_user_data(user_data)
        session_user_data_from_db = json.loads(
            Session.objects.get(id=self.session_id).session_data
        )
        self.assertEqual(user_data, session_user_data_from_db)


class TestGetSessionUserData(TestCase):
    def setUp(self) -> None:
        User.objects.create(
            login='Lisa',
            password='1234'
        )
        session_service: SessionService = SessionService(user_login='Lisa')
        self.session_id: str = session_service.get_session_id()
        self.random_int: int = random.randint(0, 1000)
        session_service.set_session_user_data(
            session_data={
                'color_theme': 'light',
                'user_id': 2,
                'user_login': 'Lisa',
                'randint': self.random_int,
            }
        )
        del session_service

    def test_custom_session_get_session_with_data(self) -> None:
        session_service: SessionService = SessionService(
            user_login='Lisa',
            session_id=self.session_id
        )
        session_user_data = session_service.get_session_user_data()

        self.assertEqual(self.session_id, session_service.get_session_id())
        self.assertEqual(session_user_data, {
            'color_theme': 'light',
            'user_id': 2,
            'user_login': 'Lisa',
            'randint': self.random_int,
        })


class TestDeleteSession(TestCase):
    def setUp(self) -> None:
        User.objects.create(
            login='Lisa',
            password='1234'
        )

    def test_delete_new_sessison(self) -> None:
        session_service: SessionService = SessionService(
            user_login='Lisa',
            # session_id=self.session_id
        )
        session_id: str = session_service.get_session_id()
        session_service.delete_session()
        with self.assertRaises(Session.DoesNotExist):
            Session.objects.get(id=session_id)

    def test_delete_existing_session(self) -> None:
        session_service: SessionService = SessionService(
            user_login='Lisa',
        )
        session_id: str = session_service.get_session_id()
        del session_service

        session_service: SessionService = SessionService(
            user_login='Lisa',
            session_id=session_id
        )
        session_service.delete_session()
        with self.assertRaises(Session.DoesNotExist):
            Session.objects.get(id=session_id)



class TestCustomSessionExpire(TestCase):
    def setUp(self) -> None:
        User.objects.create(
            login='Lisa',
            password='1234'
        )
