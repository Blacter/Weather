from copy import deepcopy
from datetime import datetime, timezone, timedelta
import pickle
import json
from typing import Any

from django.conf import settings
from django.http import HttpRequest

from weatherapp.models import Session, User
from weatherapp.repository.utils import get_user_by_user_id

# CUSTOM_SESSION_COOKIE_AGE: float = 31809906.0


class SessionError(Exception):
    def __init__(self, description: str = ''):
        self.description: str = description

    def __str__(self):
        return self.description

class ExpireDate:
    def __init__(self) -> None:
        ...

class SessionService:
    @staticmethod
    def is_session_service_exists(request: HttpRequest) -> bool:
        return hasattr(request, 'session_service')

    def __init__(
            self,
            user_login: str,
            session_id: str | None = None
        ) -> None:

        self._session_id: str | None = session_id
        self._user: User = User.objects.get(login=user_login)

        self.init_session()

    def init_session(self) -> None:
        if self._session_id is None:
            self._create_new_session()
        elif self._session_id is not None:
            self._get_exsisting_session()

    def _create_new_session(self) -> None:
        self._expire_datetime_utc: datetime
        self._calculate_expare_at()
        self._create_session_in_db()
        self._get_session_id()

    def _get_exsisting_session(self) -> None:
        self._session = Session.objects.get(id=self._session_id)

    def _calculate_expare_at(self) -> None:
        delta_unix = settings.CUSTOM_SESSION_COOKIE_AGE  # 1 year 0 month 3 days 4 hours 5min 6sec
        current_time_unix = datetime.now().timestamp()
        expire_datetime_unix = current_time_unix + delta_unix
        self._expire_datetime_utc = datetime.fromtimestamp(
            expire_datetime_unix, timezone(timedelta(hours=3)))

    def _create_session_in_db(self) -> None:
        self._session = Session.objects.create(
            expire_at=self._expire_datetime_utc,
            user_id=self._user,
        )

    def _get_session_id(self) -> None:
        self._session_id = self._session.id

    def set_session_user_data(self, session_user_data: dict[str, Any]) -> None:
        self._session_user_data_to_save = deepcopy(session_user_data)
        self._serialize_data()
        self._update_session_in_db()

    def _serialize_data(self) -> None:
        self._serialized_data: str = json.dumps(self._session_user_data_to_save)

    def _update_session_in_db(self) -> None:
        Session.objects.filter(id=self._session_id).update(
            session_data=self._serialized_data,
        )

    def get_expire_date(self) -> str:
        return self._session.expire_at

    def get_session_user_data(self) -> dict[str, Any]:
        self._deserialize_data()
        return deepcopy(self._deserialized_data)

    def _deserialize_data(self) -> None:
        data_to_deserialize: str = self._session.session_data
        self._deserialized_data: dict = json.loads(data_to_deserialize) or {} # Make Unit Test !

    def delete_session(self) -> None:
        Session.objects.filter(id=self._session.id).delete()

    def get_session_id(self) -> str:
        return self._session.id

    def get_user_name(self) -> str:
        return User.objects.get(id=self._session.user_id.id).login


# if __name__ == 'weatherapp.session.session':
#     # Create new session:
#     print('begin create new session')
#     session_service: SessionService = SessionService(user_login='Lisa')
#     session_id: str = session_service.get_session_id()
#     print(f'{session_id=}')
#     print('end create new session')

    # print('session login run')

    # session_service: SessionService = SessionService(session_id='8e14b4d3-d60f-4a1c-a3af-a008af7a0278')
    # session_service.get_session()
    # session_data = session_service.get_session_data()

    # print(f'{session_service.session_id=}')
    # print(f'{session_data=}') 

    # # add data in session.
    # session_data['new_key'] = 'updated_value'
    # session_data['key'] = 'this is old session'
    # if 'color_theme' in session_data:
    #     del session_data['color_theme']
    # session_service.update_session_data(session_data)

    # session_service.create_session(2, {'key': 'new session'})
