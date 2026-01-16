from collections import namedtuple 

import pytest
from django.conf import settings
from django.db import connection

from weather.settings import BASE_DIR
from weatherapp.models import User, Location

UserResult = namedtuple('UserResult', ['user_id', 'login', 'password'])
users = [
    UserResult(user_id=1, login='Ivan', password='1234'),
    UserResult(user_id=2, login='Olga', password='qwertyui'),
    UserResult(user_id=3, login='Inga', password='pass_1234'),
    UserResult(user_id=4, login='Rafael', password='abcdefg'),
    UserResult(user_id=5, login='Alisee_Ten', password='cat_cat'),
    UserResult(user_id=6, login='Valeria555', password='limit'),
    UserResult(user_id=7, login='Varti99', password='seven_five'),
    UserResult(user_id=8, login='Daniel_Mayer', password='zxcv'),
    UserResult(user_id=9, login='Gomer_Simpson', password='asdf'),
    UserResult(user_id=10, login='Bart_Simpson', password='qwertyui'),
    UserResult(user_id=11, login='Marg_Simpson', password='rtyu'),
    UserResult(user_id=12, login='Lisa_Simpson', password='fghj'),
    UserResult(user_id=13, login='Magy_Simpson', password='vbnm'),
    UserResult(user_id=14, login='Big_Ly', password='asdf'),
    UserResult(user_id=15, login='Mr_Smitters', password='qwertyui'),
]


@pytest.fixture(scope='function', autouse=True)
def restore_db() -> None:
    print(f'fixture restore_db start')    
    # settings.DATABASES = {
    #     'default': {
    #         'ENGINE': 'django.db.backends.sqlite3',
    #         'NAME': BASE_DIR / 'test_db.sqlite3',
    #         'TEST': {
    #             'NAME': 'test_db.sqlite3',
    #         },
    #     }
    # }
    print(f'{settings.DATABASES=}')
    print(f'{connection.settings_dict['NAME']=}')
    
    Location.objects.all().delete()
    User.objects.all().delete()
    for user in users:
        print(f'{user=}')
        User.objects.create(login=user.login, password=user.password)
    for user in User.objects.all():
        print(f'{user.login=}')