from typing import Any


from django.conf import settings
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.db.utils import OperationalError
from django.forms import ValidationError
from django.http import HttpRequest
from django.http import HttpResponseServerError, Http404
from django.db.models import QuerySet
from django.urls import reverse

from .forms import LoginForm, SignUpForm, SearchLocationForm, DeleteLocationForm, AddLocationByLatAndLonForm
from .models import User, Location
from .open_weather_works import OpenWeatherWorks
from .geocoding_api import SCHEME, GeocodingAPI
from .repository.location_works import LocationWorks
from .repository.utils import get_user_id_by_login, get_locations_by_user_name, delete_location, get_user_by_user_login
from .settings import FORM_PRINTS
from .type_aliaces import WeatherInfo, WeatherInfoList, StatusCode, LocationsInfo, LocationsInfoNotNull


def do_login(request: HttpRequest, login_form: LoginForm) -> None:
    create_custom_session(request, login_form.cleaned_data['user_login'])


def do_signup(request: HttpRequest, signup_form: SignUpForm) -> None:
    add_user_in_db(signup_form.cleaned_data)
    create_custom_session(request, signup_form.cleaned_data['user_login'])


def create_custom_session(request: HttpRequest, user_login: str) -> None:
    request.session_service.create_new_session(user_login)


# def save_user_data_in_session(request: HttpRequest, user_login: str) -> None:
#     save_in_session(request, key='user_login', value=user_login)
#     user_id: int = get_user_id_by_login(user_login=user_login)
#     save_in_session(request, key='user_id', value=user_id)


def add_user_in_db(cleaned_data: dict[str, Any]) -> None:
    user_password: str = cleaned_data['user_password']
    hash_password: str = make_password(user_password)
    try:
        User.objects.create(
            login=cleaned_data['user_login'], password=hash_password)
    except OperationalError:  # TODO добавить конкретное исключение.
        raise


def is_loged_in(request: HttpRequest) -> bool:
    if settings.DEBUG and settings.FORCED_LOGIN:
        return True
    return request.session_service.is_session_valid


def get_home_url() -> str:
    return reverse('home')


def do_search_location(request: HttpRequest, search_location_form: SearchLocationForm) -> tuple[StatusCode, LocationsInfo]:
    location_name: str = search_location_form.cleaned_data['location_name']
    save_user_input_location_name(request, location_name)
    return get_locations_info(location_name)


def save_user_input_location_name(request: HttpRequest, location_name: str | None) -> None:
    request.session_service['user_input_location_name'] = location_name


def get_locations_info(location_name: str | None) -> tuple[StatusCode, LocationsInfo]:
    geocoding_api: GeocodingAPI = GeocodingAPI(settings.APPID)
    locations_info: dict | None = geocoding_api.get_cities_by_name(
        location_name)
    return (geocoding_api.response_status_code, locations_info)
    # request.session_service['geocoding_api_response_status_code'] = geocoding_api.response_status_code
    # request.session_service['locations_info'] = locations_info


def save_in_session(request: HttpRequest, key: str, value: Any) -> None:
    request.session_service[key] = value


def do_add_location(request: HttpRequest, cleaned_data: dict) -> None:
    weather_api: OpenWeatherWorks = OpenWeatherWorks()
    lat = cleaned_data['lat']
    lon = cleaned_data['lon']
    location_info = weather_api.get_location_by_lat_and_lon(lat, lon)
    try:
        Location.objects.create(
            name=location_info['location_name'],
            user_id_id=get_user_id_by_login(request.session_service.login),
            latitude=lat,
            longitude=lon
        )
    except OperationalError:
        raise


def get_weather_info_list(user_login: str, weather_info_page: int) -> WeatherInfoList:
    locations: QuerySet[Location] = get_locations_by_user_name(user_login)
    weather_api: OpenWeatherWorks = OpenWeatherWorks()
    weather_info_list: WeatherInfoList = []

    for location in locations:
        weather_api.get_weather_by_city_name(location.name)
        weather_info: dict[str, str |
                           None] | None = weather_api.location_info()
        weather_info_list.append(WeatherInfo(
            location_name=weather_info['location_name'],
            temperature=weather_info['location_temperature'],
            country_code=weather_info['country_code'],
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


def get_forms_to_add_locations(locations_info: LocationsInfoNotNull) -> list[AddLocationByLatAndLonForm]:
    res_list: list[AddLocationByLatAndLonForm] = []
    for location_info in locations_info:
        res_list.append(AddLocationByLatAndLonForm({
            'lat': location_info['location_lat'],
            'lon': location_info['location_lon'],
        })
        )
    return res_list
