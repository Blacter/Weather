from collections import namedtuple

import pytest
from django.conf import settings

from weather.settings import BASE_DIR

from weatherapp.repository.utils import get_user_by_user_id, get_user_id_by_login
from weatherapp.models import User, Location

UserResult = namedtuple('UserResult', ['user_id', 'login', 'password'])

@pytest.mark.django_db
class TestTest:
    @pytest.mark.django_db()
    def test_test(self):
        assert 1 == 1


class TestUtils:
    @pytest.mark.django_db
    @pytest.mark.parametrize(
        'user_id, user_result',
        [
            (1, UserResult(user_id=1, login='Ivan', password='1234')),
            (2, UserResult(user_id=2, login='Olga', password='qwertyui')),
            (3, UserResult(user_id=3, login='Inga', password='pass_1234')),
            (4, UserResult(user_id=4, login='Rafael', password='abcdefg')),
            (5, UserResult(user_id=5, login='Alisee_Ten', password='cat_cat')),
            (6, UserResult(user_id=6, login='Valeria555', password='limit')),
            (7, UserResult(user_id=7, login='Varti99', password='seven_five')),
            (8, UserResult(user_id=8, login='Daniel_Mayer', password='zxcv')),
            (9, UserResult(user_id=9, login='Gomer_Simpson', password='asdf')),
            (10, UserResult(user_id=10, login='Bart_Simpson', password='qwertyui')),
            (11, UserResult(user_id=11, login='Marg_Simpson', password='rtyu')),
            (12, UserResult(user_id=12, login='Lisa_Simpson', password='fghj')),
            (13, UserResult(user_id=13, login='Magy_Simpson', password='vbnm')),
            (14, UserResult(user_id=14, login='Big_Ly', password='asdf')),
            (15, UserResult(user_id=15, login='Mr_Smitters', password='qwertyui')),
        ]
    )
    def test_get_user_by_user_id(self, user_id: int, user_result: UserResult):
        pass