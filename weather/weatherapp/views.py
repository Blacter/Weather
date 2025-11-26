from django.forms import ValidationError
from django.http import HttpResponse, HttpRequest, QueryDict
from django.http import HttpResponseNotFound
from django.http import Http404
from django.shortcuts import render, redirect
from jinja2 import Environment
from jinja2 import FileSystemLoader

from weather.jinja2 import environment

from weatherapp.request_handlers.login_handler import LoginHandler
from weatherapp.request_handlers.login_errors import LoginError

from .forms import LoginForm, SignUpForm

# Create your views here.


def index(request: HttpRequest) -> HttpResponse:
    return render(request, 'weatherapp/index.html')


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
        'login_form': login_form
    }

    return render(request, 'weatherapp/login.html', context=context)


def signup(request: HttpRequest) -> HttpResponse:
    print('TRACE: 0')
    if request.POST:
        print(f'{request.POST=}')
        signup_form: SignUpForm = SignUpForm(request.POST)
        if signup_form.is_valid():
            print(f'{signup_form.cleaned_data=}')
        else:
            print('Form data is not valid!')
    else:
        signup_form = SignUpForm()

    context = {
        'signup_form': signup_form
    }

    return render(request, 'weatherapp/signup.html', context=context)


def logout(request: HttpRequest) -> HttpResponse:
    return redirect('home')


def search_location(request: HttpRequest) -> HttpResponse:
    return render(request, 'weatherapp/search_location.html', )


def page_not_found(request: HttpRequest, exception) -> HttpResponseNotFound:
    return HttpResponseNotFound('<h1>page not found</h1>')
