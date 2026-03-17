from datetime import datetime
from contextlib import nullcontext as does_not_raise
from random import randint
from uuid import uuid4

from django.conf import settings
from django.db import connection, transaction
from django.test import TestCase, SimpleTestCase, TransactionTestCase

from weatherapp.models import User, Session
from weatherapp.session.session_custom import (
    ExpireDatetimeService,
    SessionService,
    SessionDataService,
)



class TestExpireDatetimeService(SimpleTestCase):
    def setUp(self):
        self.past_datetime: datetime = datetime(1990, 1, 1, tzinfo=settings.CURRENT_TIMEZONE)
        self.future_datetime: datetime = datetime(2050, 12, 30, tzinfo=settings.CURRENT_TIMEZONE)
        self.expire_datetime_service: ExpireDatetimeService = ExpireDatetimeService()

    def test_is_expare_at_valid(self) -> None:
        expire_at_datetime: datetime = datetime.now(settings.CURRENT_TIMEZONE)
        expire_datetime_service: ExpireDatetimeService = ExpireDatetimeService()

        self.assertFalse(
            self.expire_datetime_service.is_expare_at_valid(self.past_datetime))
        self.assertTrue(
            self.expire_datetime_service.is_expare_at_valid(self.future_datetime))


class TestSessionService(TestCase):
    # def _post_teardown(self) -> None:
    #     connection.set_autocommit(True)

    def setUp(self) -> None:
        self.login = 'Lisa' + str(randint(1, 100))
        self.user: User = User.objects.create(
            login=self.login,
            password='1234'
        )

    def test_create_new_session(self) -> None:
        session_service: SessionService = SessionService()
        session_service.create_new_session(login=self.login)
        with does_not_raise():
            Session.objects.get(
                id=session_service._session_id,
                user_id=User.objects.get(login=self.login)
            )
        with self.assertRaises(Session.DoesNotExist):
            Session.objects.get(
                id=session_service._session_id,
                user_id='-1'
            )
        with self.assertRaises(Session.DoesNotExist):
            Session.objects.get(
                id=uuid4(),
                user_id=User.objects.get(login=self.login)
            )

    def test_get_existing_session_if_valid(self) -> None:
        session_service: SessionService = SessionService()
        session_service.create_new_session(login=self.login)
        session_id_initial, session_login_initial = session_service.get_session_id_and_login()
        del session_service

        session_service: SessionService = SessionService()
        session_service.set_session_id_and_login(
            session_id=session_id_initial,
            login=session_login_initial
        )
        session_service.get_existing_session_if_valid()
        session_id_from_db, session_login_from_db = session_service.get_session_id_and_login()

        self.assertNotEqual(session_id_initial, uuid4())
        self.assertEqual(session_id_initial, session_id_from_db)

        self.assertNotEqual(session_login_initial, 'unexisting login')
        self.assertEqual(session_login_initial, session_login_from_db)
        self.assertIsNone(session_service._deserialized_data)

    def test_get_existing_session_if_valid_not_valid_case(self) -> None:
        past_datetime: datetime = datetime(1990, 1, 1, tzinfo=settings.CURRENT_TIMEZONE)
        expired_session: Session = Session.objects.create(
            user_id=self.user,
            expire_at=past_datetime
        )
        session_service_with_invalid_session: SessionService = SessionService()
        session_service_with_invalid_session.set_session_id_and_login(
            session_id=expired_session.id,
            login=expired_session.user_id.login
        )
        session_service_with_invalid_session.get_existing_session_if_valid()
        session_id, session_login = session_service_with_invalid_session.get_session_id_and_login()

        self.assertIsNone(session_id)
        self.assertIsNone(session_login)
        self.assertIsNone(session_service_with_invalid_session._session_model)

        with self.assertRaises(Session.DoesNotExist):
            Session.objects.get(
                id=expired_session.id,
                user_id=self.user
            )

    def test_delete_session(self) -> None:
        session_service: SessionService = SessionService()
        session_service.create_new_session(login=self.login)
        session_id_initial, session_login_initial = session_service.get_session_id_and_login()
        del session_service

        session_service: SessionService = SessionService()
        session_service.set_session_id_and_login(
            session_id=session_id_initial,
            login=session_login_initial
        )
        session_service.get_existing_session_if_valid()
        session_service.delete_session()
        del session_service

        with self.assertRaises(Session.DoesNotExist):
            Session.objects.get(
                id=session_id_initial,
                user_id=User.objects.get(login=self.login)
            )

    def test_save_and_get_session_data(self) -> None:
        key_1 = 'user_name'
        key_2 = 'top_1_location'
        val_1 = 'Lisa'
        val_2 = 'Izevsk'

        session_service: SessionService = SessionService()
        session_service.create_new_session(login=self.login)
        session_id_initial, session_login_initial = session_service.get_session_id_and_login()
        session_service[key_1] = val_1
        session_service[key_2] = val_2
        print(f'{session_service.is_session_valid=}')
        session_service.save_data_in_db()
        del session_service

        session_service: SessionService = SessionService()
        session_service.set_session_id_and_login(session_id_initial, session_login_initial)
        session_service.get_existing_session_if_valid()
        print(f'{session_service.is_session_valid=}')

        self.assertEqual(session_service[key_1], val_1)
        self.assertEqual(session_service[key_2], val_2)


class TestSessionDataService(SimpleTestCase):
    def test_set_item_in_not_empty_session_data(self) -> None:
        data = {
            'user_name': 'Lisa',
            'top_1_location': 'Izevsk',
        }
        session_data: SessionDataService = SessionDataService()
        session_data._set_session_data(data)
        key, value = 'new_item', 'some_value'
        session_data[key] = value
        self.assertEqual(session_data._session_data[key], value)

    def test_set_item_in_empty_session_data(self) -> None:
        data = None
        session_data: SessionDataService = SessionDataService()
        session_data._set_session_data(data)
        key, value = 'new_item', 'some_value'
        session_data[key] = value
        self.assertEqual(session_data._session_data[key], value)

    def test_get_item_in_not_emtpy_session_data(self) -> None:
        key_1 = 'user_name'
        key_2 = 'top_1_location'
        val_1 = 'Lisa'
        val_2 = 'Izevsk'
        data = {
            key_1: val_1,
            key_2: val_2,
        }
        session_data: SessionDataService = SessionDataService()
        session_data._set_session_data(data)

        self.assertEqual(session_data[key_1], val_1)
        self.assertEqual(session_data[key_2], val_2)

        with self.assertRaises(KeyError):
            session_data['unexisting_key']

    def test_get_item_in_emtpy_session_data(self) -> None:
        data = None
        session_data: SessionDataService = SessionDataService()
        session_data._set_session_data(data)

        with self.assertRaises(KeyError):
            session_data['unexisting_key']

    def test_del_item_in_not_empty_session_data(self) -> None:
        key_1 = 'user_name'
        key_2 = 'top_1_location'
        val_1 = 'Lisa'
        val_2 = 'Izevsk'
        data = {
            key_1: val_1,
            key_2: val_2,
        }
        session_data: SessionDataService = SessionDataService()
        session_data._set_session_data(data)

        del session_data[key_1]
        self.assertTrue(key_1 not in session_data.keys())
        self.assertTrue(key_2 in session_data.keys())

        del session_data[key_2]
        self.assertTrue(key_2 not in session_data.keys())

