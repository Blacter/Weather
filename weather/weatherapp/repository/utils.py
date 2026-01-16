from django.db.utils import OperationalError

from weatherapp.models import User

def get_user_by_user_id(user_id: int) -> User:
    try:
        user: User = User.objects.get(id = user_id)
    except OperationalError:
        raise
    return user

def get_user_id_by_login(user_login: str) -> int:
    try:
        user_data: User = User.objects.get(login = user_login)
    except OperationalError:
        raise
    return user_data.id