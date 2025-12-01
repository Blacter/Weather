import re
from typing import Any

from django import forms
from django.contrib.auth.hashers import check_password
from django.core.validators import RegexValidator
from django.forms import ValidationError

from .settings import FORM_PRINTS
from .models import User

acceptable_characters = RegexValidator(
    r'^[a-zA-Z0-9_]*$', message=FORM_PRINTS['login_validation_error_msg'], code='login')


class LoginForm(forms.Form):
    def clean(self) -> dict[str, Any]:
        self.cleaned_data = super().clean()
        self.get_user_with_login()
        self.check_password()
        return self.cleaned_data

    def get_user_with_login(self) -> None:
        try:            
            self.user: User  = User.objects.get(login = self.cleaned_data.get('user_login'))
        except User.DoesNotExist:
            raise ValidationError('The user with login does not exist.')

    def check_password(self) -> None:
        user_password: str | None = self.cleaned_data.get('user_password')
        if user_password is None:
            return
        user_password_hash: str = self.user.password
        if not check_password(user_password, user_password_hash):            
            raise ValidationError('Wrong password.')

    user_login = forms.CharField(
        min_length=FORM_PRINTS['login_min_length'],
        max_length=FORM_PRINTS['login_max_length'],
        label=FORM_PRINTS['login_label'],
        validators=[
            acceptable_characters,
        ],
        error_messages={
            'min_length': FORM_PRINTS['login_min_length_error_msg'],
            'max_length': FORM_PRINTS['login_max_length_error_msg'],
            'required': FORM_PRINTS['login_required_error_msg'],
        })
    user_password = forms.CharField(
        min_length=FORM_PRINTS['password_min_length'],
        max_length=FORM_PRINTS['password_max_length'], 
        label=FORM_PRINTS['password_label'],
        widget=forms.PasswordInput(),
        error_messages={
            'min_length': FORM_PRINTS['password_min_length_error_msg'],
            'max_length': FORM_PRINTS['password_max_length_error_msg'],
            'required': FORM_PRINTS['password_required_error_msg'],
        })


class SignUpForm(forms.Form):
    def clean(self) -> dict[str, Any]:
        self.cleaned_data: dict[str, Any] = super().clean()
               
        self.check_password_confirmed()
        self.check_user_not_exists()
        
        # TODO: check unique login.
        # TODO: [check password reliability]

        return self.cleaned_data
    
    def check_password_confirmed(self) -> None:
        user_password: str | None = self.cleaned_data.get('user_password')
        user_password_confirm: str | None = self.cleaned_data.get('user_password_confirm')

        if user_password is not None and user_password_confirm is not None \
            and user_password != user_password_confirm:
            raise ValidationError(FORM_PRINTS['password_confirm_error_msg'], )
        
    def check_user_not_exists(self) -> None:
        if self.is_user_exists():
            raise ValidationError(FORM_PRINTS['user_already_exists_error'])
        
    def is_user_exists(self) -> bool:
        try:
            users_with_the_login_count = len(User.objects.filter(login = self.cleaned_data['user_login']))
            print(f'{users_with_the_login_count=}')
        except:
            raise
        
        if users_with_the_login_count >= 1:
            return True
        return False

    user_login = forms.CharField(
        min_length = FORM_PRINTS['login_min_length'],
        max_length = FORM_PRINTS['login_max_length'],
        label = FORM_PRINTS['login_label'],
        validators=[
            acceptable_characters
        ],
        error_messages={
            'min_length': FORM_PRINTS['login_min_length_error_msg'],
            'max_length': FORM_PRINTS['login_max_length_error_msg'],
            'required': FORM_PRINTS['login_required_error_msg'],
        })
    
    user_password = forms.CharField(
        min_length=FORM_PRINTS['password_min_length'],
        max_length=FORM_PRINTS['password_max_length'],
        label=FORM_PRINTS['password_label'],
        widget=forms.PasswordInput(),
        error_messages={
            'min_length': FORM_PRINTS['password_min_length_error_msg'],
            'max_length': FORM_PRINTS['password_max_length_error_msg'],
            'required': FORM_PRINTS['password_required_error_msg'],
        })
    
    user_password_confirm = forms.CharField(
        min_length=FORM_PRINTS['password_min_length'],
        max_length=FORM_PRINTS['password_max_length'],
        label=FORM_PRINTS['password_label'],
        widget=forms.PasswordInput(),
        error_messages={
            'min_length': FORM_PRINTS['password_min_length_error_msg'],
            'max_length': FORM_PRINTS['password_max_length_error_msg'],
            'required': FORM_PRINTS['password_required_error_msg'],
        })
