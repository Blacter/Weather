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

from weatherapp.request_handlers.login_handler import LoginHandler
from weatherapp.request_handlers.login_errors import LoginError

from .forms import LoginForm, SignUpForm
from .models import User
from .settings import FORM_PRINTS

# Create your views here.


def index(request: HttpRequest) -> HttpResponse:
    main_page_context = {
        'user_login': request.session.get('user_login'),
    }
    return render(request, 'weatherapp/index.html', context=main_page_context)


def login(request: HttpRequest) -> HttpResponse:
    if request.POST:
        print(f'{request.POST=}')
        login_form: LoginForm = LoginForm(request.POST)
        if login_form.is_valid():
            print(f'{login_form.cleaned_data=}')
        else:
            print('Form data is not valid!')
    else:
        login_form = LoginForm()

    context = {
        'login_form': login_form,        
    }

    return render(request, 'weatherapp/login.html', context=context)


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
    return redirect('home')


def search_location(request: HttpRequest) -> HttpResponse:
    return render(request, 'weatherapp/search_location.html', )


def page_not_found(request: HttpRequest, exception) -> HttpResponseNotFound:
    return HttpResponseNotFound('<h1>page not found</h1>')
