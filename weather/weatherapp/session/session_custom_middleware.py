from django.http import HttpRequest, HttpResponse

from weatherapp.session.session_custom import SessionService

class SessionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        setattr(request, 'session_service', SessionService())

        if 'session_id_custom' in request.COOKIES and 'login' in request.COOKIES:
            request.session_service.set_session_id_and_login(
                session_id=request.COOKIES['session_id_custom'],
                login=request.COOKIES['login'],
            )
            request.session_service.get_existing_session_if_valid()

        response = self.get_response(request)

        if request.session_service.is_session_valid:
            request.session_service.save_data_in_db()
        session_id, login = request.session_service.get_session_id_and_login()

        if session_id is not None and login is not None:
            response.set_cookie(
                key='session_id_custom',
                value=session_id,
                httponly=True,
            )
            response.set_cookie(
                key='login',
                value=login,
                httponly=True,
            )
        else:
            response.delete_cookie('session_id_custom')
            response.delete_cookie('login')

        return response
