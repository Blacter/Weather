from string import Template

from weather.settings import settings

LOGIN_MIN_LENGTH: int = 4
LOGIN_MAX_LENGTH: int = 20
PASSWORD_MIN_LENGTH: int = 4
PASSWORD_MAX_LENGTH: int = 20
LOCATION_NAME_MAX_LENGTH: int = 255
LOCATION_LAT_MAX_LENGTH: int = 15
LOCATION_LON_MAX_LENGTH: int = 15


FORM_PRINTS: dict[str, str|int] = {
    # 'login_contains_wrong_characters': 'недопустимые символы в логине.',
    'field_required_error_msg': 'поле обязательно для заполнения.',
    
    'login_min_length': LOGIN_MIN_LENGTH,
    'login_max_length': LOGIN_MAX_LENGTH,
    'login_label': 'Логин:',
    'login_validation_error_msg': 'недопустимые символы в логине.',
    'login_min_length_error_msg': f'слишком короткий логин. Должен содержать хотя бы {LOGIN_MIN_LENGTH} символов.',
    'login_max_length_error_msg': f'слишком длинный логин. Должен содержать не более {LOGIN_MAX_LENGTH} символов.',
    'login_required_error_msg': 'обязательно для заполнения.',
    'login_does_not_exist': 'пользователь с данным логином не существует',
    
    'password_min_length': PASSWORD_MIN_LENGTH,
    'password_max_length': PASSWORD_MAX_LENGTH,
    'password_label': 'Пароль:',
    'password_confirm_label': 'Введите пароль еще раз:',
    'password_min_length_error_msg': f'слишком короткий пароль. Должен содержать хотя бы {PASSWORD_MIN_LENGTH} символов.',
    'password_max_length_error_msg': f'слишком длинный пароль. Должен содержать не более {PASSWORD_MAX_LENGTH} символов.',
    'password_required_error_msg': 'обязательно для заполнения.',
    'password_wrong_password': 'неверный пароль',
    
    'password_confirm_error_msg': 'пароли не совпадают.',
    'user_already_exists_error': 'пользователь с данным логином уже существует.',
    
    'location_name_max_length': LOCATION_NAME_MAX_LENGTH,
    'location_name_label': 'Введите название города:',
    'location_name_max_length_error_msg': f'слишком длинное название города. Должно содержать не более {LOCATION_NAME_MAX_LENGTH} символов.',
    
    'location_lat_required_error_msg': 'lat field is required',
    'location_lat_max_length': LOCATION_LAT_MAX_LENGTH,
    'location_lat_max_length_error_msg': f'Недопустимое значение широты. Должно содержать не более {LOCATION_LAT_MAX_LENGTH} символов.',
    
    'location_lon_required_error_msg': 'lon field is required',
    'location_lon_max_length': LOCATION_LON_MAX_LENGTH,
    'location_lon_max_length_error_msg': f'Недопустимое значение доллготы. Должно содержать не более {LOCATION_LON_MAX_LENGTH} символов.',
    
    'search_location_location_exists_error': 'локация уже существует',
    'server_error': 'Server Error, Pleace repead later',
    
    'location_addition_error': 'Ошибка при добавлении локации.',
    'location_addition_success': 'Локация успешно добавлена',
    
    'delete_location_success': 'Локация успешно удалена',
    'delete_location_does_not_exist': 'Ошибка при удалении локации',
    # '': '',
}

# weatherapp_settings: WeatherappSettings = WeatherappSettings()
APPID: str = settings.APPID
OPEN_WEATHER_PRINTS: dict[str, str|Template] = {
    'appid': settings.APPID,
    'weather_by_lat_and_lon_url': Template(f'https://api.openweathermap.org/data/2.5/weather?lat=$lat&lon=$lon&appid={APPID}'),
    'weather_by_city_and_country': Template(f'https://api.openweathermap.org/data/2.5/weather?q=$city_name,$country_code&appid={APPID}'),
    'weather_by_city': Template(f'https://api.openweathermap.org/data/2.5/weather?q=$city_name&appid={APPID}'),
}

GEOCODING_PRINTS: dict[str, str|Template] = {
    'cities_by_name_and_country_code': Template(f'http://api.openweathermap.org/geo/1.0/direct?q=$city_name,$country_code&limit=$limit&appid=$appid'),
    'cities_by_name': Template(f'http://api.openweathermap.org/geo/1.0/direct?q=$city_name&limit=$limit&appid={APPID}'),
    'limit': 5,
}
