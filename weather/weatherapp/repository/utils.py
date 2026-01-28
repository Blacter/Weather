from django.db.models import QuerySet
from django.db.utils import OperationalError

from weatherapp.models import User, Location

def get_user_by_user_id(user_id: int) -> User:
    try:
        user: User = User.objects.get(id = user_id)
    except OperationalError:
        raise
    return user

def get_user_by_user_login(user_login: str) -> User:
    try:
        user_data: User = User.objects.get(login = user_login)
    except OperationalError:
        raise
    return user_data

def get_user_id_by_login(user_login: str) -> int:
    try:
        user_data: User = User.objects.get(login = user_login)
    except OperationalError:
        raise
    return user_data.id

def get_locations_by_user_name(user_login: str) -> QuerySet[Location]:
    user_id: int = get_user_id_by_login(user_login)
    res_locations: QuerySet[Location] = Location.objects.filter(user_id=user_id)
    # print(f'{type(locations_with_user_id)=}')
    return res_locations

def get_one_location_by_user_name_and_location_name(user_login: str, location_name_to_delete: str) -> Location:
    user: User = get_user_by_user_login(user_login)
    return Location.objects.get(name=location_name_to_delete, user_id=user)
    
def delete_location(user_login: str, location_name_to_delete: str) -> None:
    location: Location = get_one_location_by_user_name_and_location_name(user_login, location_name_to_delete)
    location.delete()
    