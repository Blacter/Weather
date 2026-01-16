from dataclasses import dataclass
from string import Template

import requests
from bs4 import BeautifulSoup


@dataclass
class LoginRquestResult:
    form_general_error: str = ''
    login_field_error: str = ''
    password_field_error: str = ''


class LoginUtils:
    def __init__(self) -> None:
        self.protocol: str = 'http'
        self.host: str = 'localhost'
        self.port: str = '8000'
        self.url_template: Template = Template('$protocol://$host:$port/weatherapp/login/')
        self._request_url: str = self.url_template.substitute(protocol=self.protocol, host=self.host, port=self.port)
        
    @property
    def request_url(self) -> str:
        return self._request_url
    
    def do_login(self, user_login: str, user_password: str) -> LoginRquestResult:
        self.user_login = user_login
        self.user_password = user_password
        self.login_request_result: LoginRquestResult = LoginRquestResult()
        self.get_csrf()        
        self.do_login_request()
        return self.login_request_result
    
    def get_csrf(self) -> None:
        response: requests.Response = requests.get(self.request_url)
        page_body: BeautifulSoup = BeautifulSoup(response.text, 'html.parser')
        self.csrf_cookies: str = response.cookies.get('csrftoken')
        self.csrf_token: str = page_body.find('input', {'name': 'csrfmiddlewaretoken'})['value']
        print(f'{self.csrf_cookies=}')
        print(f'{self.csrf_token=}')
        
    def do_login_request(self) -> None:
        cookies_for_login = {
            'csrftoken': self.csrf_cookies,
        }
        data_for_login = {
            'csrfmiddlewaretoken': self.csrf_token,
            'user_login': self.user_login,
            'user_password': self.user_password,
        }
        print(f'{data_for_login=}')
        self.login_response: requests.Response = requests.post(self.request_url, data = data_for_login, cookies=cookies_for_login)
        print(f'{self.login_response.status_code=}')
        
        self.save_response_text_in_file(file_name='temp_login_results.html')
        
        self.parse_login_results()

    def save_response_text_in_file(self, file_name: str) -> None:
        with open(file_name, 'w') as html_file:
            html_file.write(self.login_response.text)    
    
    def parse_login_results(self) -> None:
        self.form_general_error: str = ''
        self.login_field_error: str = ''
        self.password_field_error: str = ''        
        self.login_results_page: BeautifulSoup = BeautifulSoup(self.login_response.text, 'html.parser')
        self.parse_general_form_error()
        self.parse_login_field_error()
        self.parse_password_field_error()
        print(f'{self.login_request_result=}')
        
    def parse_general_form_error(self) -> None:        
        form_general_error_tag = self.login_results_page.find('div', {'class': 'form-general-error'})
        if form_general_error_tag is not None:
            self.login_request_result.form_general_error = form_general_error_tag.text
            
    def parse_login_field_error(self) -> None:
        login_field_error_tag = self.login_results_page.find('div', {'class': 'login-field-error'}) # login-field-error
        if login_field_error_tag is not None:
            self.login_request_result.login_field_error = login_field_error_tag.text
            
    def parse_password_field_error(self) -> None:
        password_field_error_tag = self.login_results_page.find('div', {'class': 'password-field-error'}) # password-field-error
        if password_field_error_tag is not None:
            self.login_request_result.password_field_error = password_field_error_tag.text
