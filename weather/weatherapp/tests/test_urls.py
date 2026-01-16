from django.test import SimpleTestCase
from django.urls import reverse, resolve
from weatherapp import views

class TestUrls(SimpleTestCase):
    def test_login_url_is_resolve(self):
        url = reverse('login')
        self.assertEqual(resolve(url).func, views.login)
        
    def test_signup_url_is_resolve(self):
        url = reverse('signup')
        self.assertEqual(resolve(url).func, views.signup)
        
    def test_logout_url_is_resolve(self):
        url = reverse('logout')
        self.assertEqual(resolve(url).func, views.logout)
        
    def test_search_location_is_resolve(self):
        url = reverse('search_location')
        self.assertEqual(resolve(url).func, views.search_location)
        
    def test_search_location_result_is_resolve(self):
        url = reverse('search_location_result')
        self.assertEqual(resolve(url).func, views.search_location_result)
        
    def test_add_location_url_is_resolve(self):
        url = reverse('add_location')
        self.assertEqual(resolve(url).func, views.add_location)


