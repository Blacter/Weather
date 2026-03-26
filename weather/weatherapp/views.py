from collections import namedtuple
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

from .forms import LoginForm, SignUpForm, SearchLocationForm, AddLocationForm,  DeleteLocationForm
from .type_aliaces import WeatherInfoList
from .settings import FORM_PRINTS
from .utils import (
    do_login, do_signup, do_search_location, do_add_location, do_delete_location,
    is_loged_in, get_home_url, get_weather_info_list, get_delete_location_form_list
)


def page_not_found(request: HttpRequest, exception: Exception) -> HttpResponseNotFound:
    return HttpResponseNotFound('<h1>page not found</h1>')


def server_error(request: HttpRequest) -> HttpResponseNotFound:
    return HttpResponseNotFound('<h1>server error, please, try again later</h1>')


def index(request: HttpRequest) -> HttpResponse:
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
        weather_info_list = get_weather_info_list(
            user_login, weather_info_page)
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
    status: int = 200
    if is_loged_in(request):
        home_redirect = get_home_url()
        return redirect(home_redirect)

    if request.POST:
        login_form: LoginForm = LoginForm(request.POST)
        try:
            if login_form and login_form.is_valid():
                do_login(request, login_form)
                home_redirect = reverse('home')
                return redirect(home_redirect)
        except OperationalError:
            messages.error(request, FORM_PRINTS['server_error'])
            status = 500
    else:
        login_form = LoginForm()

    context: dict[str, Any] = {
        'messages': messages.get_messages(request),
        'login_form': login_form,
    }

    return render(request, 'weatherapp/login.html', context=context, status=status)


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

    if request.GET:
        search_location_form: SearchLocationForm = SearchLocationForm(
            request.GET)
        if search_location_form.is_valid():
            do_search_location(request, search_location_form)
            # search_location_result_url: str = reverse('search_location_result')
    else:
        search_location_form: SearchLocationForm = SearchLocationForm()

    location_info: dict[str, Any] = request.session_service.get(
        'location_info')
    location_name: str = ''
    if location_info:
        location_name: str = location_info.get('location_name')

    context: dict[str, Any] = {
        'messages': messages.get_messages(request),
        'user_login': request.session_service.get_session_id_and_login()[1],
        'search_location_form': search_location_form,
        'add_location_form': AddLocationForm({'location_name': location_name}),
        'location_info': location_info,
        'user_input_location_name': request.session_service.get('user_input_location_name'),
    }

    return render(request, 'weatherapp/search_location_result.html', context=context)


def add_location(request: HttpRequest) -> HttpResponse:
    if not is_loged_in(request):
        login_redirect = reverse('login')
        return redirect(login_redirect)

    status: int = 200

    if request.POST:
        try:
            add_location_form: AddLocationForm = AddLocationForm(
                request.POST, request=request)
            if add_location_form.is_valid():
                do_add_location(request)
                home_redirect = reverse('home')
                messages.success(
                    request, message=FORM_PRINTS['location_addition_success'])
                return redirect(home_redirect)
            else:
                ValidationError(
                    FORM_PRINTS['location_addition_error'])  # FIXME!
                messages.error(request, FORM_PRINTS['location_addition_error'])
        except ValidationError:
            raise
        except OperationalError:
            messages.error(request, FORM_PRINTS['server_error'])
            status: int = 500

    location_info: dict[str, Any] = request.session_service.get(
        'location_info')
    location_name: str = ''
    if location_info:
        location_name: str = location_info.get('location_name')

    context: dict[str, Any] = {
        'messages': messages.get_messages(request),
        'user_login': request.session_service.get('user_login'),
        'search_location_form': SearchLocationForm(),
        'add_location_form': AddLocationForm({'location_name': location_name}),
        'location_info': location_info,
        'user_input_location_name': request.session_service.get('user_input_location_name'),
    }

    return render(request, 'weatherapp/search_location_result.html', context=context, status=status)
