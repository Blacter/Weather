from pprint import pprint
from typing import Any

from bs4 import BeautifulSoup
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.http import HttpResponse, HttpRequest
from django.templatetags.static import static
from django.test import TestCase, SimpleTestCase, Client
from django.urls import reverse
from jinja2 import Environment, FileSystemLoader, Template

from weatherapp import forms
from weatherapp import views
from weatherapp.models import User
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
            'user_login': None,  # None
            'search_location_form': forms.SearchLocationForm(),
            'messages': None,
            'url': reverse,
            'static': static,
            'zip': zip,
            'weather_info_list': [WeatherInfo(  # weather_info_list
                location_name='l_name',
                temperature='l_temperature',
                country_code='l_country',
            )],  # weather_info_list
        }
        content_from_index_template: str = tm.render(**main_page_context)

        index_url: str = reverse('home')
        response: HttpResponse = self.client.get(index_url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(content_from_index_template,
                         response.content.decode())

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


# class TestSearchLocationResultView(TestCase):
#     def setUp(self) -> None:
#         self.client: Client = Client()
#         file_loader = FileSystemLoader('weatherapp/jinja2')
#         self.env = Environment(loader=file_loader)

#         self.user_data = {
#             'login': 'Lisa',
#             'password': '1234',
#         }
#         User.objects.create(
#             login= self.user_data['login'],
#             password= make_password(self.user_data['password'])
#         )

#     def test_user_not_loged_in(self) -> None:
#         tm_index: Template = self.env.get_template('weatherapp/index.html')
#         tm_search_location_result: Template = self.env.get_template(
#             'weatherapp/search_location_result.html')
#         weather_info_list: WeatherInfoList | None = None

#         main_page_context: dict[str, Any] = {
#             'user_login': None,  # None
#             'search_location_form': forms.SearchLocationForm(),
#             'messages': None,
#             'url': reverse,
#             'static': static,
#             'zip': zip,
#             'weather_info_list': [WeatherInfo(  # weather_info_list
#                 location_name='l_name',
#                 temperature='l_temperature',
#                 country_code='l_country',
#             )],  # weather_info_list
#         }

#         content_from_index_template: str = tm_index.render(**main_page_context)
#         search_location_results_url: str = reverse('search_location_result')
#         response: HttpResponse = self.client.get(
#             search_location_results_url, follow=True)

#         self.assertEqual(response.status_code, 302)
#         self.assertEqual(response.headers.get(
#             'Location'), '/weatherapp/login/')

#     def test_user_regular_case(self) -> None:
#         # do login
#         login_url: str = reverse('login')
#         login_get_response: HttpResponse = self.client.get(login_url)

#         # get csrf
#         login_soup = BeautifulSoup(
#             login_get_response.content, features='html.parser')
#         csrf_input_tag = login_soup.find_all('input')[0]
#         csrf_name = csrf_input_tag['name']
#         csrf_value = csrf_input_tag['value']

#         login_input_tag = login_soup.find_all('input')[1]
#         login_name_attribute = login_input_tag['name']

#         password_input_tag = login_soup.find_all('input')[2]
#         password_name_attribute = password_input_tag['name']

#         print('Trace begin')
#         print(f'{csrf_name=}')
#         print(f'{csrf_value=}')
#         print(f'{login_name_attribute=}')
#         print(f'{password_name_attribute=}')
#         print('Trace end')
        
#         data_to_login = {
#             csrf_name: csrf_value,
#             login_name_attribute: self.user_data['login'],
#             password_name_attribute: self.user_data['password']
#         }
        
#         login_post_response: HttpResponse = self.client.post(
#             login_url,
#             follow=False,
#             data=data_to_login,
#         )
        
#         self.user_login_cookie = login_post_response.cookies['login']
#         self.user_session_id_custom_cookie = login_post_response.cookies['session_id_custom']
        
#         # print(f'{login_post_response.status_code=}')
#         # print(f'{login_post_response.headers=}')
#         # print(f'{login_post_response.cookies=}')
#         # print(f'{login_post_response.content.decode('utf-8')=}')
        
#         search_location_results_url: str = reverse('search_location_result')
#         data_to_search_location = {
            
#         }

#         search_location_response: HttpResponse = self.client.post(
#             search_location_results_url,
#             data = data_to_search_location,
#             follow=True,
#             headers=f'Cookie: login={self.user_data['login']} session_id_custom={self.user_session_id_custom_cookie}'
#             )
        
#         print(f'{search_location_response.status_code=}')
#         print(f'{search_location_response.headers=}')
#         print(f'{search_location_response.cookies=}')
        

#         tm_search_location_result: Template = self.env.get_template(
#             'weatherapp/search_location_result.html')
#         weather_info_list: WeatherInfoList | None = None
#         search_location_result_page_context: dict[str, Any] = {
#             'messages': None,
#             'user_login': None,
#             'search_location_form': forms.SearchLocationForm(),

#             'geocoding_api_response_status_code': 404,
#             'locations_info': None,
#             'add_location_by_lat_and_lon_form_list': None,
#             'user_input_location_name': 'Some Location Name',

#             'url': reverse,
#             'static': static,
#             'zip': zip,
#         }

#         content_from_search_location_result_template: str = tm_search_location_result.render(
#             **search_location_result_page_context)
        
        

#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(content_from_search_location_result_template,
#                          response.content.decode())
