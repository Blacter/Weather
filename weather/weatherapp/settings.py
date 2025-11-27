from string import Template

LOGIN_MIN_LENGTH: int = 4
LOGIN_MAX_LENGTH: int = 20
PASSWORD_MIN_LENGTH: int = 4
PASSWORD_MAX_LENGTH: int = 20

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
    'password_max_length_error_msg': f'слишком длинный пароль. Должен содержать не более {PASSWORD_MAX_LENGTH} символа.',
    'password_required_error_msg': 'обязательно для заполнения.',
    
    'password_confirm_error_msg': 'пароли не совпадают.',
    'user_already_exists_error': 'пользователь с данным логином уже существует.',
    # '': '',
}

