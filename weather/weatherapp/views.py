from typing import Any

from django.contrib import messages
from django.db.utils import OperationalError
from django.http import HttpResponse, HttpRequest
from django.http import HttpResponseNotFound
from django.shortcuts import render, redirect
from django.urls import reverse

# from weather.jinja2 import environment

from .forms import LoginForm, SignUpForm, SearchLocationForm
from .settings import FORM_PRINTS
from .utils import (do_login, do_signup, do_search_location, is_loged_in, get_home_url)

def index(request: HttpRequest) -> HttpResponse:
    main_page_context: dict[str, Any] = {
        'user_login': request.session.get('user_login'),
        'search_location_form': SearchLocationForm(),
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
        'login_form': login_form,
        'messages': messages.get_messages(request),
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
        'signup_form': signup_form,
        'messages': messages.get_messages(request),
    }

    return render(request, 'weatherapp/signup.html', context=context, status=status)
    

def logout(request: HttpRequest) -> HttpResponse:
    if is_loged_in(request):
        request.session.flush()
    return redirect('home')


def search_location(request: HttpRequest) -> HttpResponse:
    if not is_loged_in(request):
        login_redirect = reverse('login')
        return redirect(login_redirect)
    
    if request.GET:
        search_location_form: SearchLocationForm = SearchLocationForm(request.GET)
        if search_location_form.is_valid():
            do_search_location(request, search_location_form)
            search_location_result_url: str = reverse('search_location_result')
            return redirect(search_location_result_url)
    else: 
        search_location_form: SearchLocationForm = SearchLocationForm()
        
    context: dict[str, Any] = {
        'search_location_form': search_location_form,
        'user_login': request.session.get('user_login'),
    }
    
    return render(request, 'weatherapp/search_location.html', context=context)



def search_location_result(request: HttpRequest) -> HttpResponse:
    if not is_loged_in(request):
        login_redirect = reverse('login')
        return redirect(login_redirect)
    
    context: dict[str, Any] = {
        'user_login': request.session.get('user_login'),
        'location_info': request.session.get('location_info'),
        'user_input_location_name': request.session.get('user_input_location_name'),
        'search_location_form': SearchLocationForm(),
    }
    
    return render(request, 'weatherapp/search_location_result.html', context=context)


def page_not_found(request: HttpRequest, exception: Exception) -> HttpResponseNotFound:
    return HttpResponseNotFound('<h1>page not found</h1>')

def server_error(request: HttpRequest) -> HttpResponseNotFound:
    return HttpResponseNotFound('<h1>server error, please, try again later</h1>')