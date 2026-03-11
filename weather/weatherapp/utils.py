from typing import Any

from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.db.utils import OperationalError
from django.forms import ValidationError
from django.http import HttpRequest
from django.http import HttpResponseServerError, Http404
from django.db.models import QuerySet
from django.urls import reverse

from .forms import LoginForm, SignUpForm, SearchLocationForm, DeleteLocationForm
from .models import User, Location
from .open_weather_works import OpenWeatherWorks
from .repository.location_works import LocationWorks
from .repository.utils import get_user_id_by_login, get_locations_by_user_name, delete_location
from .settings import FORM_PRINTS
from .type_aliaces import WeatherInfo, WeatherInfoList


def do_login(request: HttpRequest, login_form: LoginForm) -> None:
    save_user_data_in_session(request, login_form.cleaned_data['user_login'])


def do_signup(request: HttpRequest, signup_form: SignUpForm) -> None:
    add_user_in_db(signup_form.cleaned_data)
    save_user_data_in_session(request, signup_form.cleaned_data['user_login'])    


def save_user_data_in_session(request: HttpRequest, user_login: str) -> None:    
    save_in_session(request, key='user_login', value=user_login)
    user_id: int = get_user_id_by_login(user_login=user_login)
    save_in_session(request, key='user_id', value=user_id)


def add_user_in_db(cleaned_data: dict[str, Any]) -> None:
    user_password: str = cleaned_data['user_password']
    hash_password: str = make_password(user_password)
    try:
        User.objects.create(login=cleaned_data['user_login'], password=hash_password)
    except OperationalError:  # TODO добавить конкретное исключение.
        raise 


def is_loged_in(request: HttpRequest) -> bool:
    return bool(request.session.get('user_login'))


def get_home_url() -> str:
    return reverse('home')


def do_search_location(request: HttpRequest, search_location_form: SearchLocationForm) -> None:
    save_user_input_location_name(request, search_location_form.cleaned_data['location_name'])
    save_location_info(request, search_location_form)


def save_user_input_location_name(request: HttpRequest, location_name: str | None) -> None:
    request.session['user_input_location_name'] = location_name


def save_location_info(request: HttpRequest, search_location_form: SearchLocationForm) -> None:
    location_name: str = search_location_form.cleaned_data['location_name']
    weather_api: OpenWeatherWorks = OpenWeatherWorks()
    weather_api.get_lat_and_lot_by_city(city_name=location_name)
    location_info: dict[str, str | None] | None = weather_api.location_info() # TODO: implement result return with dataclasses?
    request.session['location_info'] = location_info 


def save_in_session(request: HttpRequest, key: str, value: Any) -> None:
    request.session[key] = value


def do_add_location(request: HttpRequest) -> None:    
    location_works: LocationWorks = LocationWorks(request)
    location_works.save_location()


def get_weather_info_list(user_login: str, weather_info_page: int) -> WeatherInfoList:
    locations: QuerySet[Location] = get_locations_by_user_name(user_login)
    weather_api: OpenWeatherWorks = OpenWeatherWorks()    
    weather_info_list: WeatherInfoList = []

    for location in locations:
        weather_api.get_weather_by_city_name(location.name)
        weather_info: dict[str, str | None] | None = weather_api.location_info()
        weather_info_list.append(WeatherInfo(
            location_name = weather_info['location_name'],
            temperature = weather_info['location_temperature'],
            country_code = weather_info['country_code'],
        ))
    return weather_info_list


def get_delete_location_form_list(weather_info_list: WeatherInfoList) -> list[DeleteLocationForm]:
    delete_location_form_list: list[DeleteLocationForm] = []
    for weather_info in weather_info_list:
            delete_location_form_list.append(
                DeleteLocationForm({'location_name': weather_info.location_name})
            )
    return delete_location_form_list


def do_delete_location(request: HttpRequest, user_login: str, location_name_to_delete: str) -> None:
    try:
        delete_location(user_login, location_name_to_delete)
        messages.success(request, FORM_PRINTS['delete_location_success'])
    except Location.DoesNotExist:
        messages.error(request, FORM_PRINTS['delete_location_does_not_exist'])
