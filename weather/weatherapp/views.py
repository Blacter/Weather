from collections import namedtuple
from pprint import pprint
from typing import Any

from django.contrib import messages
from django.db.utils import OperationalError
from django.forms import ValidationError
from django.http import HttpResponse, HttpRequest
from django.http import HttpResponseNotFound
from django.shortcuts import render, redirect
from django.urls import reverse

from django.template.loader import render_to_string

# from weather.jinja2 import environment

from .forms import (
    LoginForm, SignUpForm, SearchLocationForm,  DeleteLocationForm,
    AddLocationByLatAndLonForm,
)
from .type_aliaces import WeatherInfoList, StatusCode, LocationsInfo
from .settings import FORM_PRINTS
from .utils import (
    do_login, do_signup, do_search_location, do_delete_location,
    is_loged_in, get_home_url, aget_weather_info_list, get_delete_location_form_list,
    get_forms_to_add_locations, do_add_location
)


def page_not_found(request: HttpRequest, exception: Exception) -> HttpResponseNotFound:
    return HttpResponseNotFound('<h1>page not found</h1>')


def server_error(request: HttpRequest) -> HttpResponseNotFound:
    return HttpResponseNotFound('<h1>server error, please, try again later</h1>')


async def index(request: HttpRequest) -> HttpResponse:
    weather_info_list: WeatherInfoList | None = None
    delete_location_form_list: list[DeleteLocationForm] = []
    user_login: str | None = None
    if is_loged_in(request):
        user_login = request.session_service.get_session_id_and_login()[1]

        if request.POST:
            delete_location_form: DeleteLocationForm = DeleteLocationForm(
                request.POST)
            if delete_location_form.is_valid():
                location_to_delete: str = delete_location_form.cleaned_data['location_name']
                do_delete_location(
                    request,
                    user_login,
                    location_to_delete
                )
            else:
                messages.error(
                    request, delete_location_form.errors['location_name'][0])

        weather_info_page: int = 1
        # TODO: Вернуть результат из асинхронной функции.
        weather_info_list = await aget_weather_info_list(user_login, weather_info_page)
        delete_location_form_list = get_delete_location_form_list(
            weather_info_list)

    main_page_context: dict[str, Any] = {
        'messages': messages.get_messages(request),
        'user_login': user_login,
        'search_location_form': SearchLocationForm(),
        'delete_location_form_list': delete_location_form_list,
        'weather_info_list': weather_info_list,
    }

    return render(request, 'weatherapp/index.html', context=main_page_context)


def login(request: HttpRequest) -> HttpResponse:
    status_code: StatusCode = 200
    if is_loged_in(request):
        home_redirect = get_home_url()
        return redirect(home_redirect)

    if request.method == 'POST':
        login_form: LoginForm = LoginForm(request.POST)
        try:
            if login_form.is_valid():
                do_login(request, login_form)
                home_redirect = reverse('home')
                return redirect(home_redirect)
            else:
                status_code = 400
        except OperationalError:
            messages.error(request, FORM_PRINTS['server_error'])
            status_code = 500
    else:
        login_form = LoginForm()
        status_code = 200

    context: dict[str, Any] = {
        'messages': messages.get_messages(request),
        'login_form': login_form,
    }

    return render(request, 'weatherapp/login.html', context=context, status=status_code)


def signup(request: HttpRequest) -> HttpResponse:
    status: int = 200
    if is_loged_in(request):
        home_redirect = reverse('home')
        return redirect(home_redirect)

    if request.POST:
        signup_form: SignUpForm = SignUpForm(request.POST)
        if signup_form.is_valid():
            try:
                do_signup(request, signup_form)
                home_redirect = reverse('home')
                return redirect(home_redirect)
            except OperationalError:
                messages.error(request, FORM_PRINTS['server_error'])
                status = 500
    else:
        signup_form = SignUpForm()

    context: dict[str, Any] = {
        'messages': messages.get_messages(request),
        'signup_form': signup_form,
    }

    return render(request, 'weatherapp/signup.html', context=context, status=status)


def logout(request: HttpRequest) -> HttpResponse:
    if is_loged_in(request):
        request.session_service.delete_session()
    return redirect('home')


def search_location_result(request: HttpRequest) -> HttpResponse:
    if not is_loged_in(request):
        login_redirect = reverse('login')
        return redirect(login_redirect)

    geocoding_api_response_status_code: StatusCode = None
    locations_info: LocationsInfo = None

    if request.POST:
        search_location_form: SearchLocationForm = SearchLocationForm(
            request.POST)
        if search_location_form.is_valid():
            geocoding_api_response_status_code, locations_info = do_search_location(
                request, search_location_form)
    else:
        search_location_form: SearchLocationForm = SearchLocationForm()

    location_to_add_forms = None
    if locations_info is not None:
        location_to_add_forms = get_forms_to_add_locations(
            locations_info)

    context: dict[str, Any] = {
        'messages': messages.get_messages(request),
        'user_login': request.session_service.get_session_id_and_login()[1],
        'search_location_form': search_location_form,

        'geocoding_api_response_status_code': geocoding_api_response_status_code,
        'locations_info': locations_info,
        'add_location_by_lat_and_lon_form_list': location_to_add_forms,
        'user_input_location_name': request.session_service.get('user_input_location_name'),
    }

    return render(request, 'weatherapp/search_location_result.html', context=context)


def add_location(request: HttpRequest) -> HttpResponse:
    if not is_loged_in(request):
        login_redirect = reverse('login')
        return redirect(login_redirect)

    status: StatusCode = 200

    if request.POST:
        try:
            add_location_by_lat_and_lon_form: AddLocationByLatAndLonForm = AddLocationByLatAndLonForm(
                request.POST)

            if add_location_by_lat_and_lon_form.is_valid():
                do_add_location(
                    request, add_location_by_lat_and_lon_form.cleaned_data)
                home_redirect = reverse('home')
                messages.success(
                    request, message=FORM_PRINTS['location_addition_success'])
                return redirect(home_redirect)
            else:
                ValidationError(FORM_PRINTS['location_addition_error'])
                messages.error(request, FORM_PRINTS['location_addition_error'])
        except ValidationError:
            raise
        except OperationalError:
            messages.error(request, FORM_PRINTS['server_error'])
            status: StatusCode = 500

    location_info: LocationsInfo = request.session_service.get(
        'location_info')

    context: dict[str, Any] = {
        'messages': messages.get_messages(request),
        'user_login': request.session_service.login,
        'search_location_form': SearchLocationForm(),
        'location_info': location_info,
        'user_input_location_name': request.session_service.get('user_input_location_name'),
    }

    return render(request, 'weatherapp/search_location_result.html', context=context, status=status)
