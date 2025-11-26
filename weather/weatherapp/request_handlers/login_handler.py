from django.http import HttpRequest, HttpResponse

from weatherapp.request_handlers.request_handler import RequestHandler
from weatherapp.request_handlers.request_keys import login_keys


class LoginHandler(RequestHandler):
    def __init__(self, request: HttpRequest) -> None:
        super().__init__(request=request, get_keys=login_keys, post_keys=None)
        
    # def do_login(self) -> HttpResponse:
    #     try:
    #         self.check_login_data()
    #     except LoginError as e:
    #         raise
        
    #     try:
    #         self.check_login()
    
    # def check_login_data(request_post_data: QueryDict):
    #     super().check_request_data()
    #     check_user_data()
        
    