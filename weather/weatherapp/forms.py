import re
from typing import Any

from django import forms
from django.core.validators import RegexValidator
from django.forms import ValidationError
from .settings import FORM_PRINTS

from .models import User

acceptable_characters = RegexValidator(
    r'^[a-zA-Z0-9_]*$', message=FORM_PRINTS['login_validation_error_msg'], code='login')


class LoginForm(forms.Form):
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
        cleaned_data: dict[str, Any] = super().clean()
        print(f'{cleaned_data.keys()=}')
        user_password: str | None = cleaned_data.get('user_password')
        user_password_confirm: str | None = cleaned_data.get('user_password_confirm')

        if user_password is not None and user_password_confirm is not None \
            and user_password != user_password_confirm:
            raise ValidationError(FORM_PRINTS['password_confirm_error_msg'], )
        
        # TODO: check unique login.
        # TODO: [check password reliability]

        return cleaned_data

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
