from string import Template

LOGIN_MIN_LENGTH: int = 4
LOGIN_MAX_LENGTH: int = 20
PASSWORD_MIN_LENGTH: int = 4
PASSWORD_MAX_LENGTH: int = 20
LOCATION_NAME_MAX_LENGTH: int = 255

FORM_PRINTS: dict[str, str|int] = {
    'login_contains_wrong_characters': 'недопустимые символы в логине.',
    'login_min_length': LOGIN_MIN_LENGTH,
    'login_max_length': LOGIN_MAX_LENGTH,
    'login_label': 'Логин:',
    'login_validation_error_msg': 'недопустимые символы в логине.',
    'login_min_length_error_msg': f'слишком короткий логин. Должен содержать хотя бы {LOGIN_MIN_LENGTH} символов.',
    'login_max_length_error_msg': f'слишком длинный логин. Должен содержать не более {LOGIN_MAX_LENGTH} символа.',
    'login_required_error_msg': 'обязательно для заполнения.',
    
    'password_min_length': PASSWORD_MIN_LENGTH,
    'password_max_length': PASSWORD_MAX_LENGTH,
    'password_label': 'Пароль:',
    'password_min_length_error_msg': f'слишком короткий пароль. Должен содержать хотя бы {PASSWORD_MIN_LENGTH} символов.',
    'password_max_length_error_msg': f'слишком длинный пароль. Должен содержать не более {PASSWORD_MAX_LENGTH} символов.',
    'password_required_error_msg': 'обязательно для заполнения.',
    
    'password_confirm_error_msg': 'пароли не совпадают.',
    'user_already_exists_error': 'пользователь с данным логином уже существует.',
    
    'location_name_max_length': LOCATION_NAME_MAX_LENGTH,
    'location_name_label': 'Введите название города:',
    'location_name_max_length_error_msg': f'слишком длинное название города. Должно содержать не более {LOCATION_NAME_MAX_LENGTH} символов.',
    'search_location_location_exists_error': 'Локация уже существует',
    '': '',
    # '': '',
}
APPID: str = ''
OPEN_WEATHER_PRINTS: dict[str, str|Template] = {
    'appid': APPID,
    'weather_by_lat_and_lon_url': Template(f'https://api.openweathermap.org/data/2.5/weather?lat=$lat&lon=$lon&appid={APPID}'),
    'weather_by_city_and_country': Template(f'https://api.openweathermap.org/data/2.5/weather?q=$city_name,$country_code&appid={APPID}'),
    'weather_by_city': Template(f'https://api.openweathermap.org/data/2.5/weather?q=$city_name&appid={APPID}'),
}

