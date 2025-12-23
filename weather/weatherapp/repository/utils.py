from weatherapp.models import User

def get_user_id_by_login(user_login: str) -> int:
    try:
        user_data: User = User.objects.get(login = user_login)
    except: # TODO: отлавливать исключение БД.
        raise
    return user_data.id