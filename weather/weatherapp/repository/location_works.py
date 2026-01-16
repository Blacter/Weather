from typing import Any

from django.db.utils import OperationalError
from django.forms import ValidationError
from django.http import HttpRequest

from weatherapp.models import Location
from weatherapp.repository.utils import get_user_by_user_id
from weatherapp.settings import FORM_PRINTS
from weatherapp.type_aliaces import Lat, Lon

class LocationWorks():
    def __init__(self, request: HttpRequest) -> None:
        location_info: dict[str, Any] | None = request.session.get('location_info')
        user_id: int | None = request.session.get('user_id')
        if location_info is None or user_id is None:
            raise ValidationError(FORM_PRINTS['location_addition_error'])
        
        self.location_name: str = location_info['location_name']
        self.user_id: int = user_id
        self.latitude: Lat = location_info['location_lat']
        self.longitude: Lon = location_info['location_lon']
        
    def save_location(self) -> None:
        if not self.is_location_exists():            
            try:
                Location.objects.create(
                    name=self.location_name,
                    user_id=get_user_by_user_id(self.user_id),
                    latitude=self.latitude,
                    longitude=self.longitude
                )
            except OperationalError:
                raise

    def is_location_exists(self) -> bool:
        try:
            Location.objects.get(user_id=self.user_id, name=self.location_name)
        except Location.DoesNotExist:
            return False
        except OperationalError:
            raise            
            
        return True
