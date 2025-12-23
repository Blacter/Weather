from django.urls import path
from django.urls import URLPattern

from weatherapp import views

urlpatterns: list[URLPattern] = [
    path('', views.index, name='home'),
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.logout, name='logout'),
    path('search_location/', views.search_location, name='search_location'),
    path('search_location_result/', views.search_location_result, name='search_location_result'),    
]