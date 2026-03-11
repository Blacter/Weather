import uuid
from django.http import HttpRequest, HttpResponse

from weatherapp.session.session import SessionService


class CustomSessionMiddleware:
    def __init__(self, get_response) -> None:
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> None:
        self.cookies: dict[str, str] = request.COOKIES
        if self.is_session_id_and_login_in_cookies_exists() \
            and self.is_session_data_in_cookies_valid():
            self.get_session_data_from_cookies()
            self.set_session_attributes(request)

        response = self.get_response(request)

        print('CustomSessionMiddleware CALL')
        if hasattr(request, 'session_service'):
            self.set_custom_session_cookies_headers(
                response, request.session_service)
        return response

    def set_custom_session_cookies_headers(self, response: HttpResponse, session_service: SessionService) -> None:
        response.set_cookie(
            key='custom_session_id',
            value=session_service.get_session_id()
        )
        response.set_cookie(
            key='login',
            value=session_service.get_user_name()
        )

    def is_session_data_in_cookies_valid(self) -> bool:
        if not self._is_session_data_in_cookies_valid():
            return False
        return True

    def set_session_attributes(self, request: HttpRequest) -> None:
        setattr(
            request,
            'session_service',
            SessionService(
                user_login=self._user_login,
                session_id=self._session_id,
            )
        )

    def get_session_data_from_cookies(self) -> None:
        self._user_login = self.cookies['login']
        self._session_id = self.cookies['custom_session_id']

    def is_session_id_and_login_in_cookies_exists(self) -> bool:
        return 'custom_session_id' in self.cookies and 'login' in self.cookies

    def _is_session_data_in_cookies_valid(self) -> bool:
        if not self.is_session_id_valid():
            return False
        if not self.is_user_login_valid():
            return False
        return True

    def is_session_id_valid(self) -> bool:
        session_id: str = self.cookies['custom_session_id'].strip()
        return (self.is_valid_uuid(uuid_to_test=session_id, version=4))

    # TODO доделать проверку на допустимые символы
    def is_user_login_valid(self) -> bool:
        user_login: str = self.cookies['login'].strip()
        return True

    @staticmethod
    def is_valid_uuid(uuid_to_test: str, version: int) -> bool:
        try:
            uuid.UUID(uuid_to_test, version=version)
        except ValueError:
            return False
        return True

    def get_data_for_session(self, cookies: dict[str, str]) -> None:
        cookies['login'].strip()
