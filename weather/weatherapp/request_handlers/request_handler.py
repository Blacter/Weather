from abc import ABC, abstractmethod

from django.http import HttpRequest, HttpResponse

from weatherapp.request_handlers.request_errors import KeyError
from weatherapp.request_handlers.request_keys import GetKeys, PostKeys


class RequestHandler(ABC):
    def __init__(self, request: HttpRequest, get_keys: GetKeys, post_keys: PostKeys) -> None:
        self.request: HttpRequest = request
        self.get_keys: GetKeys = get_keys
        self.post_keys: PostKeys = post_keys

    def check_request_data(self) -> None:
        self.check_get_request_data()
        self.check_post_request_data()

    def check_get_request_data(self) -> None:
        self.check_get_keys_exist()
        self.check_get_values_exist()
        self.check_get_values_valid()

    @abstractmethod
    def check_get_keys_exist(self) -> None:
        if self.get_keys is not None:
            for key in self.get_keys:
                if key not in self.request.GET:
                    raise KeyError(key_with_error=key, request_method='GET')

    def check_get_values_exist(self) -> None:
        if self.get_keys is not None:
            for key in self.get_keys:
                pass

    @abstractmethod
    def check_get_values_valid(self) -> None:
        pass

    def check_post_request_data(self) -> None:
        self.check_post_keys_exist()
        self.check_post_values_exist()
        self.check_post_values_valid()

    @abstractmethod
    def check_post_keys_exist(self) -> None:
        if self.post_keys is not None:
            for key in self.post_keys:
                if key not in self.request.POST:
                    raise KeyError(key_with_error=key, request_method='POST')

    @abstractmethod
    def check_post_values_exist(self) -> None:
        pass

    @abstractmethod
    def check_post_values_valid(self) -> None:
        pass
