from contextlib import nullcontext as does_not_raise
from decimal import Decimal

from django.db.utils import IntegrityError, DataError
from django.db import transaction
from django.test import TestCase
import pytest
from weatherapp.models import User, Location

class TestUserModels(TestCase):

    def test_user_create(self) -> None:        
        User.objects.create(login='Ivan', password='12341234')
        self.user1: User = User.objects.get(login = 'Ivan')
        self.assertEqual(self.user1.login, 'Ivan')
        self.assertEqual(self.user1.password, '12341234')

    def test_login_unique_constraint(self) -> None:
        User.objects.create(login='Ivan', password='12341234')
        with pytest.raises(IntegrityError): # FIXME: ? change to self.assertRaises(IntegrityError)
            with transaction.atomic():
                User.objects.create(login='Ivan', password='asdfasdf')
            
        with does_not_raise():
            User.objects.create(login='Inga', password='12341234')

    def test_login_max_length_constraint(self) -> None:
        with pytest.raises(DataError): 
            with transaction.atomic():
                User.objects.create(login='I'*256, password='12341234')
            self.fail('fail test_login_max_length_constraint')

        with does_not_raise(): 
            User.objects.create(login='I'*255, password='12341234')

    def test_password_max_length_constraint(self) -> None:
        with pytest.raises(DataError): # 
            with transaction.atomic():
                User.objects.create(login='Vera', password='1'*256)
            self.fail('fail test_password_max_length_constraint')

        with does_not_raise():
            User.objects.create(login='Vera', password='1'*255)


class TestLocationModels(TestCase):
    def setUp(self) -> None:
        self.user: User = User.objects.create(login='Ivan', password='1234')
        
    def test_location_create(self) -> None:
        Location.objects.create(
            name = 'Ivanovo',
            user_id = self.user,
            latitude = 56.9942,
            longitude = 40.9858,
        )
        location: Location = Location.objects.get(name='Ivanovo', user_id=self.user)
        self.assertEqual(location.name, 'Ivanovo')
        self.assertEqual(location.user_id, self.user)
        self.assertEqual(location.latitude, Decimal('56.9942'))
        self.assertEqual(location.longitude, Decimal('40.9858'))  

    def test_name_max_length_constraint(self) -> None:        
        with pytest.raises(DataError):
            with transaction.atomic():
                Location.objects.create(
                    name = 'I'*256,
                    user_id = self.user,
                    latitude = 56.9942,
                    longitude = 40.9858,
                )
        
        with does_not_raise():
            Location.objects.create(
                name = 'I'*255,
                user_id = self.user,
                latitude = 56.9942,
                longitude = 40.9858,
            )
    
    def test_location_on_delete_cascade(self) -> None:
        Location.objects.create(
            name = 'Ivanovo',
            user_id = self.user,
            latitude = 56.9942,
            longitude = 40.9858,
        )
        self.user.delete()
        with pytest.raises(Location.DoesNotExist):
            Location.objects.get(name='Ivanovo')
        
    def test_location_latitude_max_digits_constraint(self) -> None:
        with pytest.raises(DataError):
            with transaction.atomic():
                Location.objects.create(
                    name = 'Ivanovo',
                    user_id = self.user,
                    latitude = 560000.9942,
                    longitude = 40.9858,
                )
        with does_not_raise():
            Location.objects.create(
                name = 'Ivanovo',
                user_id = self.user,
                latitude = 5600.9942455,
                longitude = 40.9858,
            )

    def test_location_longitude_max_digits_constraint(self) -> None:
        with pytest.raises(DataError):
            with transaction.atomic():
                Location.objects.create(
                    name = 'Ivanovo',
                    user_id = self.user,
                    latitude = 56.9942,
                    longitude = 401234.9858,
                )
                
        with does_not_raise():
            Location.objects.create(
                        name = 'Ivanovo',
                        user_id = self.user,
                        latitude = 56.9942,
                        longitude = 4012.9858,
                    )