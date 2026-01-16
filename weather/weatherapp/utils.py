from typing import Any

from django.contrib.auth.hashers import make_password
from django.db.utils import OperationalError
from django.http import HttpRequest
from django.http import HttpResponseServerError, Http404
from django.urls import reverse

from .forms import LoginForm, SignUpForm, SearchLocationForm
from .models import User
from .open_weather_works import OpenWeatherWorks
from .repository.location_works import LocationWorks
from .repository.utils import get_user_id_by_login

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
    location_info: dict[str, str | None] | None = weather_api.location_info()
    request.session['location_info'] = location_info 


def save_in_session(request: HttpRequest, key: str, value: Any) -> None:
    request.session[key] = value


def do_add_location(request: HttpRequest) -> None:    
    location_works: LocationWorks = LocationWorks(request)
    location_works.save_location()
    