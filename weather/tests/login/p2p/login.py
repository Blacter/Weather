import pytest

from tests.login.p2p.login_utils import LoginRquestResult
from tests.login.p2p.login_utils import LoginUtils

@pytest.fixture(scope='module')
def login_utils() -> LoginUtils:
    return LoginUtils()

class TestLogin:
    @pytest.mark.parametrize(
        'user_login, user_password, is_error, status_code, form_general_error, login_field_error, password_field_error',
        [
            ('user_login', 'user_passowrd', False, 200, 'form_general_error', 'login_field_error', 'password_field_error'),
            ('Ivan', '1234', False, 200, '', '', ''),      
            ('user_login_12345_user_login_12345', 'user_password', True, 200, '', 'слишком длинный логин', ''),
            ('user_login', 'user_password_12345_user_password_12345', True, 200, '', '', 'слишком длинный пароль'),
            ('user_login_12345_user_login_12345', 'user_password_12345_user_password_12345', True, 200, '', 'слишком длинный логин', 'слишком длинный пароль'),
            ('lg', 'user_password', True, 200, '', 'слишком короткий логин.', ''),
            ('user_login', 'ps', True, 200, '', '', 'слишком короткий пароль.'),
            ('lg', 'ps', True, 200, '', 'слишком короткий логин.', 'слишком короткий пароль.'),
            ('', 'user_password', True, 200, '', 'обязательно для заполнения.', ''),
            ('user_login', '', True, 200, '', '', 'обязательно для заполнения.'),
            ('', '', True, 200, '', 'обязательно для заполнения.', 'обязательно для заполнения.'),
            ('user_password', '', True, 200, '', '', 'обязательно для заполнения.'),            
            ('логин', 'user_pass', True, 200, '', 'недопустимые символы в логине.', ''),
            ('user_logi', 'user_pass', True, 200, 'Пользователь с данным логином не существует', '', ''),
            ('Ivann', '1234', True, 200, 'Пользователь с данным логином не существует', '', ''),
            ('Ivan', '12345', True, 200, 'неверный пароль', '', ''),
            ('   Ivan    ', '  1234   ', False, 200, '', '', ''),            
        ]
    )
    def test_login(self, user_login: str, user_password: str, is_error: str, status_code: int, form_general_error: str, login_field_error: str, password_field_error: str,
                   login_utils: LoginUtils):
        # login_utils: LoginUtils = LoginUtils() # В фикстуру
        login_request_result: LoginRquestResult = login_utils.do_login(user_login, user_password, )
        
        # print(f'{login_utils.user_login=}')
        # print(f'{login_utils.user_password=}')
        print(f'{form_general_error=}')
        print(f'{login_request_result.form_general_error=}')
        
        print(f'{login_field_error=}')            
        print(f'{login_request_result.login_field_error=}')
        
        print(f'{password_field_error=}')
        print(f'{login_request_result.password_field_error=}')
        if is_error:
            
            assert form_general_error in login_request_result.form_general_error
            assert login_field_error in login_request_result.login_field_error
            assert password_field_error in login_request_result.password_field_error
        else:
            assert '' == login_request_result.form_general_error
            assert '' == login_request_result.login_field_error
            assert '' == login_request_result.password_field_error

if __name__ == '__main__':
    login_utils: LoginUtils = LoginUtils() # В фикстуру
    login_request_result: LoginRquestResult = login_utils.do_login('Ivan', '12')
    
    assert 'Ошибка:' in login_request_result.form_general_error and '' in login_request_result.login_field_error and '' in login_request_result.password_field_error
