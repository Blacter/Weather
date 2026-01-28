from pprint import pprint
from typing import Any

from django.contrib import messages
from django.http import HttpResponse, HttpRequest
from django.test import TestCase, Client
from django.urls import reverse
from jinja2 import Environment, FileSystemLoader, Template

from weatherapp import forms
from weatherapp import views
from weatherapp.type_aliaces import WeatherInfo
from weatherapp.type_aliaces import WeatherInfoList


class TestViews(TestCase):
    def setUp(self) -> None:
        self.client: Client = Client()
        file_loader = FileSystemLoader('weatherapp/jinja2')
        self.env = Environment(loader=file_loader)
    
    def test_index_view(self) -> None:
        tm: Template = self.env.get_template('weatherapp/index.html')
        weather_info_list: WeatherInfoList | None = None
        
        main_page_context: dict[str, Any] = {
            'user_login': 'tmp', # None
            'search_location_form': forms.SearchLocationForm(),
            'messages': None,
            'url': reverse,
            'weather_info_list': [WeatherInfo( # weather_info_list
                location_name = 'l_name',
                temperature = 'l_temperature',
                country_code = 'l_country',
            )], # weather_info_list 
        }        
        content_from_index_template: str = tm.render(**main_page_context)
        print(content_from_index_template)
        
        index_url: str = reverse('home')
        response: HttpResponse = self.client.get(index_url)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(content_from_index_template, response.content.decode())
        
    # def test_login_view_user_not_logged_in(self) -> None:
    #     tm: Template = self.env.get_template('weatherapp/login.html')
    #     login_context: dict[str, Any] = {
    #         'login_form': forms.LoginForm(),
    #         'messages': None,
    #         'url': reverse,
    #     }
    #     content_from_login_template: str = tm.render(**login_context)
        
    #     login_url: str = reverse('login')        
    #     response: HttpResponse = self.client.get(login_url)
        
    #     response.cookies['session']
        
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(content_from_login_template, response.content.decode())

    # def test_login_view_user_is_logined_in(self) -> None:
    #     pass
    