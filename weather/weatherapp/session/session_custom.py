from copy import deepcopy
from datetime import datetime, timezone, timedelta
from typing import Any
import json

from django.conf import settings
from weatherapp.models import User, Session
from weatherapp.session.expire_datetime_service import ExpireDatetimeService


class SessionNotValid(Exception):
    ...


class SessionDataService:
    def __init__(self) -> None:
        self._session_data: dict | None = None

    def _set_session_data(self, session_data: dict | None = None) -> None:
        if session_data is None:
            self._session_data = {}
        else:
            self._session_data = deepcopy(session_data)

    def keys(self):
        return self._session_data.keys()

    def __getitem__(self, item) -> Any:
        return self._session_data[item]

    def __setitem__(self, key, value) -> None:
        self._session_data[key] = value

    def __delitem__(self, key) -> None:
        del self._session_data[key]


class SessionService(SessionDataService):
    def __init__(self):
        super().__init__()
        self._is_session_exists: bool | None = None
        self._is_session_valid: bool | None = None
        self._session_id: str | None = None
        self._login: str | None = None
        self._deserialized_data: dict | None = None
        self._expire_datetime_service: ExpireDatetimeService = ExpireDatetimeService()

    def set_session_id_and_login(self, session_id: str, login: str):
        self._session_id = session_id
        self._login = login

    def get_session_id_and_login(self) -> tuple:
        return (self._session_id, self._login)

    def delete_session_id_and_login_values(self) -> None:
        self._delete_session_id_value()
        self._delete_login_value()

    def _delete_session_id_value(self) -> None:
        self._session_id = None

    def _delete_login_value(self) -> None:
        self._login = None

    def get_existing_session_if_valid(self):
        try:
            self._get_session()
            self._is_session_exists = True
            self._check_if_session_valid()
        except Session.DoesNotExist:
            self._is_session_exists = False
        except SessionNotValid:
            self._delete_session()
        else:
            self._deserialize_session_data()

    def _get_session(self) -> None:
        self._session_model = Session.objects.get(
            id=self._session_id,
            user_id=User.objects.get(login=self._login)
        )

    def _check_if_session_valid(self) -> None:
        self._validate_session()
        if not self._is_session_valid:
            # self._is_session_valid = False
            raise SessionNotValid()

    def delete_session(self) -> None:
        self._delete_session()

    def _deserialize_session_data(self) -> None:
        data_to_deserialize: str = self._session_model.session_data
        deserialized_data: dict | None = json.loads(data_to_deserialize)
        self._set_session_data(deserialized_data)

    def _validate_session(self):
        self._validate_session_expire_date()

    @property
    def is_session_valid(self) -> bool:
        # if self._is_session_valid is None:
        return self._is_session_exists and self._is_session_valid

    def _validate_session_expire_date(self) -> None:
        self._is_session_valid = self._expire_datetime_service.is_expare_at_valid(
            self._session_model.expire_at
        )

    def _delete_session(self):
        self._delete_session_from_db()
        self.delete_session_id_and_login_values()

    def _delete_session_from_db(self):
        try:
            self._session_model.delete()
            self._session_model = None
        except Session.DoesNotExist:
            pass

    def create_new_session(self, login: str) -> None:
        expire_date = self._expire_datetime_service.get_new_expire_at()
        self._session_model = Session(
            expire_at=expire_date,
            user_id=User.objects.get(login=login)
        )
        self._session_model.save()
        self._session_id = self._session_model.id
        self._login = self._session_model.user_id.login
        self._set_session_data()

        self._is_session_exists = True
        self._is_session_valid = True

    def save_data_in_db(self) -> None:
        serialized_data: str = json.dumps(self._session_data)
        self._session_model.session_data = serialized_data
        self._session_model.save()
