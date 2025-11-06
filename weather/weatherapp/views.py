from django.http import HttpResponse, HttpRequest
from django.http import HttpResponseNotFound
from django.http import Http404
from django.shortcuts import render

# Create your views here.
def index(request: HttpRequest) -> HttpResponse:
    return HttpResponse('<h1>index</h1>')
    
def login(request: HttpRequest) -> HttpResponse:
    return HttpResponse('<h1>login</h1>')
    
def signup(request: HttpRequest) -> HttpResponse:
    return HttpResponse('<h1>signup</h1>')
    
def logout(request: HttpRequest) -> HttpResponse:
    return HttpResponse('<h1>logout</h1>')
    
def search_location(request: HttpRequest) -> HttpResponse:
    return HttpResponse('<h1>search_location</h1>')
    
def page_not_found(request, exception) -> HttpResponseNotFound:
    return HttpResponseNotFound('<h1>page not found</h1>')
