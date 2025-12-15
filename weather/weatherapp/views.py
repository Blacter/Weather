from typing import Any

from django.contrib.auth.hashers import make_password
from django.forms import ValidationError
from django.http import HttpResponse, HttpRequest, QueryDict
from django.http import HttpResponseNotFound
from django.http import Http404
from django.shortcuts import render, redirect
from django.urls import reverse
from jinja2 import Environment
from jinja2 import FileSystemLoader

from weather.jinja2 import environment

from .forms import LoginForm, SignUpForm, SearchLocationForm
from .model.location_works import LocationWorks
from .models import User
from .open_weather_works import OpenWeatherWorks
from .settings import FORM_PRINTS
from .type_aliaces import Lat, Lon

# Create your views here.


def index(request: HttpRequest) -> HttpResponse:
    main_page_context = {
        'user_login': request.session.get('user_login'),
    }
    return render(request, 'weatherapp/index.html', context=main_page_context)


def login(request: HttpRequest) -> HttpResponse:
    if is_loged_in(request):
        home_redirect = get_home_url()
        return redirect(home_redirect)
    
    if request.POST:
        login_form: LoginForm = LoginForm(request.POST)
        if login_form.is_valid():
            request.session['user_login'] = login_form.cleaned_data['user_login']
            home_redirect = reverse('home')
            return redirect(home_redirect)
    else:
        login_form = LoginForm()

    context: dict[str, Any] = {
        'login_form': login_form,        
    }

    return render(request, 'weatherapp/login.html', context=context)


def is_loged_in(request: HttpRequest) -> bool:
    return bool(request.session.get('user_login'))


def get_home_url() -> str:
    return reverse('home')


def signup(request: HttpRequest) -> HttpResponse:
    if request.session.get('user_login'):
        home_redirect = reverse('home')            
        return redirect(home_redirect)
        
    if request.POST:
        signup_form: SignUpForm = SignUpForm(request.POST)
        if signup_form.is_valid():
            print(f'{signup_form.cleaned_data=}')
            # TODO: add user in db
            add_user_in_db(signup_form.cleaned_data)
            # Session.
            request.session['user_login'] = signup_form.cleaned_data['user_login']            
            home_redirect = reverse('home')
            return redirect(home_redirect)
    else:
        signup_form = SignUpForm()

    context = {'signup_form': signup_form}

    return render(request, 'weatherapp/signup.html', context=context)


def add_user_in_db(cleaned_data: dict[str, Any]) -> None:
    try:
        user_password: str = cleaned_data['user_password']
        print(f'{user_password=}')
        hash_password: str = make_password(user_password)
        User.objects.create(login=cleaned_data['user_login'], password=hash_password)
    except: 
        raise
    

def logout(request: HttpRequest) -> HttpResponse:
    if is_loged_in(request):
        request.session.flush()
    return redirect('home')


def search_location(request: HttpRequest) -> HttpResponse:
    if not is_loged_in(request):
        login_redirect = reverse('login')
        return redirect(login_redirect)
    
    if request.GET:
        # user_id: str = request.session['user_id']
        user_id: str = '-1' # temporary. Then implement location in db exists when user add location in db.
        search_location_form: SearchLocationForm = SearchLocationForm(request.GET, user_id)
        if search_location_form.is_valid():
            save_user_input_location_name(request, search_location_form.cleaned_data['location_name'])
            save_location_info(request, search_location_form)
            search_location_result: str = reverse('search_location_result') # reverse('search_location_result')
            print(f'{request.session['location_info']=}')
            return redirect(search_location_result)
    else: 
        search_location_form: SearchLocationForm = SearchLocationForm()
        
    context: dict[str, Any] = {
        'search_location_form': search_location_form,
        'user_login': request.session.get('user_login'),
    }
    
    return render(request, 'weatherapp/search_location.html', context=context)


def save_user_input_location_name(request: HttpRequest, location_name: str | None) -> None:
    request.session['user_input_location_name'] = location_name
    


def save_location_info(request: HttpRequest, search_location_form: SearchLocationForm) -> None:
    location_name: str = search_location_form.cleaned_data['location_name']
    weather_api: OpenWeatherWorks = OpenWeatherWorks()
    weather_api.get_lat_and_lot_by_city(city_name=location_name)
    location_info: dict[str, str | None] | None = weather_api.location_info()
    request.session['location_info'] = location_info
    

def search_location_result(request: HttpRequest) -> HttpResponse:
    if not is_loged_in(request):
        login_redirect = reverse('login')
        return redirect(login_redirect)
    
    print(f'{request.session.get('location_info')['api_response_code']=}')
    
    context: dict[str, Any] = {
        'user_login': request.session.get('user_login'),
        'location_info': request.session.get('location_info'),
        'user_input_location_name': request.session.get('user_input_location_name'),
    }
    
    return render(request, 'weatherapp/search_location_result.html', context=context)


def page_not_found(request: HttpRequest, exception) -> HttpResponseNotFound:
    return HttpResponseNotFound('<h1>page not found</h1>')
