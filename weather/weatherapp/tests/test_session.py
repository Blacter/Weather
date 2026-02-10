import time

from django.http import HttpResponse
from django.test import TestCase, Client
from weatherapp.models import User

class SessionTestCase(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.user: User = User.objects.create(
            login='testuser',
            password='testpass123'
        )

    # def test_session_storage(self) -> None:
    #     # Тестируем сохранение в сессию
    #     response: HttpResponse = self.client.post('', {
    #         'user_preferences':{
    #             'theme': 'dark',
    #             'language': 'en'
    #         }
    #     })

    #     # Проверяем, что данные сохранились
    #     session = self.client.session
    #     self.assertEqual(session['user_preferences']['theme'], 'dark')
    #     self.assertEqual(session['user_preferences']['language'], 'en')

    def test_session_expiry(self) -> None:
        # Тестируем истечение сессии
        session = self.client.session
        session['test_data'] = 'value'
        session.set_expiry(1)
        session.save()
        
        time.sleep(2)

        self.assertNotIn('test_data', self.client.session)
