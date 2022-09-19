from uuid import UUID, uuid4
from bson.binary import Binary
from app.owner_finder import OwnerFinder


class Station:
    def __init__(self, data):
        self.__geo_is_valid = False
        if not data:
            raise ValueError('data is empty')

        if 'owner_uuid' not in data:
            raise ValueError('owner_id is missing')

        if type(data['owner_uuid']) is not str:
            raise ValueError('owner_id is not a string')

        try:
            self.__owner = OwnerFinder.find(UUID(data['owner_uuid']))
        except ValueError:
            raise ValueError('owner_id is not a valid UUID')

        if 'latitude' in data and 'longitude' in data:
            if isinstance(data['latitude'], int) and isinstance(data['longitude'], int):
                data['latitude'] = float(data['latitude'])
                data['longitude'] = float(data['longitude'])

            if not isinstance(data['latitude'], float) or not isinstance(data['longitude'], float):
                raise ValueError('latitude and longitude must be float')

            if data['latitude'] < -90 or data['latitude'] > 90:
                raise ValueError('latitude must be between -90 and 90')

            if data['longitude'] < -180 or data['longitude'] > 180:
                raise ValueError('longitude must be between -180 and 180')

            self.__geo_is_valid = True
            self.__latitude = data['latitude']
            self.__longitude = data['longitude']
        else:
            raise ValueError('latitude and longitude are missing')

        self.id = uuid4()

    def to_dict(self):
        data = {
            'uuid': Binary.from_uuid(self.id),
            'owner': self.__owner.__to_json_for_object__(),
            'last_temperature': 0.0,
            'last_wind': 0.0,
            'last_rain': 0.0,
            'last_sun': 0.0,
            'last_battery_state': 0.0,
            'hives': []
        }

        if self.__geo_is_valid:
            data['latitude'] = self.__latitude
            data['longitude'] = self.__longitude

        return data
