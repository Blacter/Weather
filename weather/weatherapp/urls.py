from django.urls import path

from weatherapp import views

urlpatterns: list = [
    path('', views.index, name='home'),
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.logout, name='logout'),
    path('search_location/', views.search_location, name='search_location'),
]
