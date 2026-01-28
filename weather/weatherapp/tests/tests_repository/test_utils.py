from django.test import TestCase

from weatherapp.models import User, Location
from weatherapp.repository.utils import (get_locations_by_user_name,
    get_user_by_user_login, get_one_location_by_user_name_and_location_name, delete_location)


class TestRepositoryUtils(TestCase):
    def test_get_locations_by_user_name(self) -> None:
        user_name: str = 'Ivan'
        user: User = User.objects.create(login=user_name, password='1234')
        
        location_names_benchmark: list[str] = ['Ivanovo', 'Moscow', 'Yaroslavl', 'Novgorod', 'Perm\'', 'Solnechnogorsk', 'Tula', ]
        latitudes: list[float] = [11.0, 21.0, 31.0, 41.0, 51.0, 61.0, 71.0]
        longitudes: list[float] = [12.0, 22.0, 32.0, 42.0, 52.0, 62.0, 72.0]
        
        for location_name, latitude, longitude in zip(location_names_benchmark, latitudes, longitudes):
            Location.objects.create(name=location_name, user_id=user, latitude=latitude, longitude=longitude)
        
        locations_from_db = get_locations_by_user_name(user_name)        
        
        for location_from_db, location_name_benchmark, latitude_benchmark, longitude_benchmark in zip(locations_from_db, location_names_benchmark, latitudes, longitudes):
            self.assertEqual(location_from_db.name, location_name_benchmark)
            self.assertEqual(location_from_db.latitude, latitude_benchmark)
            self.assertEqual(location_from_db.longitude, longitude_benchmark)
            
    def test_get_user_by_user_login(self) -> None:
        user_names: list[str] = ['Ivan', 'Lisa', 'SuperBob', 'Vanna']
        user_passwords: list[str] = ['1234', 'asdf', 'qwer', '1980']
        user_list: list[User] = []
        
        for name, password in zip(user_names, user_passwords):
            user_list.append(User.objects.create(login=name, password=password))

        for name in user_names:
            res_user: User = get_user_by_user_login(name)
            self.assertEqual(res_user.login, name)

        unexisting_user_name: str = 'unexisting_user_name'
        with self.assertRaises(User.DoesNotExist):
            get_user_by_user_login(unexisting_user_name)
        
    def test_get_one_location_by_user_name_and_location_name(self):
        user_names: list[str] = ['Ivan', 'Lisa']
        user_passwords: list[str] = ['1234', 'asdf']
        location_names_list: list[str] = ['Volgograd', 'Moscow', 'Tver\'', 'Minsk', 'Paris', 'London']
        lat: float = 10.0
        lon: float = 10.0
        user_list: list[User] = []
        
        for name, password in zip(user_names, user_passwords):
            user_list.append(User.objects.create(login=name, password=password))

        user_0: User = user_list[0]
        
        for location_name in location_names_list:
            Location.objects.create(name=location_name, user_id=user_0, latitude=lat, longitude=lon)
        
        for location_name in location_names_list:    
            res_location: Location = get_one_location_by_user_name_and_location_name(
                user_login=user_0.login,
                location_name_to_delete=location_name
            )
            self.assertEqual(res_location.name, location_name)
            
        with self.assertRaises(Location.DoesNotExist):
            get_one_location_by_user_name_and_location_name(
                user_login=user_names[1],
                location_name_to_delete=location_names_list[0]
            )
            
        with self.assertRaises(Location.DoesNotExist):
            get_one_location_by_user_name_and_location_name(
                user_login=user_names[0],
                location_name_to_delete='unexsist_location'
            )
            
    def test_delete_location(self) -> None:
        user_names: list[str] = ['Ivan', 'Lisa']
        user_passwords: list[str] = ['1234', 'asdf']
        location_names_list: list[str] = ['Volgograd', 'Moscow', 'Tver\'', 'Minsk', 'Paris', 'London']
        lat: float = 10.0
        lon: float = 10.0
        user_list: list[User] = []
        
        for name, password in zip(user_names, user_passwords):
            user_list.append(User.objects.create(login=name, password=password))
        
        user_0: User = user_list[0]
        
        for location_name in location_names_list:
            Location.objects.create(name=location_name, user_id=user_0, latitude=lat, longitude=lon)
            
        delete_location(user_0.login, location_names_list[0])
        with self.assertRaises(Location.DoesNotExist):
            get_one_location_by_user_name_and_location_name(
                user_login=user_0.login,
                location_name_to_delete=location_names_list[0]
                )
            
        delete_location(user_0.login, location_names_list[1])
        with self.assertRaises(Location.DoesNotExist):
            get_one_location_by_user_name_and_location_name(
                user_login=user_0.login,
                location_name_to_delete=location_names_list[1]
                )