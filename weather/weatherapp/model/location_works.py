from weatherapp.type_aliaces import Lat, Lon

from weatherapp.models import Location

class LocationWorks():
    def save_location(self, location_name: str, user_id: int, latitude: Lat, longitude: Lon) -> None:
        Location.objects.create(name=location_name, user_id=user_id, latitude=latitude, longitude=longitude)
        
    def is_location_exists(self, user_id: int | None, location_name: str | None) -> bool:
        try:
            Location.objects.get(user_id=user_id, location_name=location_name)
        except :
            return False
            # raise
            
        return True
