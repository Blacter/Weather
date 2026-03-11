from django.urls import path
from django.urls import URLPattern

from weatherapp import views

urlpatterns: list[URLPattern] = [
    path('test_session/', views.session_test, name='test_session'),

    path('', views.index, name='home'),
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.logout, name='logout'),
    path('search_location_result/', views.search_location_result, name='search_location_result'),
    path('add_location/', views.add_location, name='add_location'),
]