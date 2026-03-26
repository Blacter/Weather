import re
from typing import Any

from django import forms
from django.contrib.auth.hashers import check_password
from django.core.validators import RegexValidator
from django.db.utils import OperationalError
from django.forms import ValidationError
from django.http import QueryDict
from django.http import HttpRequest

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
        user_login: str | None = self.cleaned_data.get('user_login')
        if user_login is None:
            return
        try:
            self.user: User = User.objects.get(login=user_login)
        except User.DoesNotExist:
            raise ValidationError(FORM_PRINTS['login_does_not_exist'])
        except OperationalError:
            raise

    def check_password(self) -> None:
        user_login: str | None = self.cleaned_data.get('user_login')
        user_password: str | None = self.cleaned_data.get('user_password')
        if user_login is None or user_password is None:
            return
        user_password_hash: str = self.user.password
        if not check_password(user_password, user_password_hash):
            raise ValidationError(FORM_PRINTS['password_wrong_password'])

    user_login = forms.CharField(
        min_length=FORM_PRINTS['login_min_length'],
        max_length=FORM_PRINTS['login_max_length'],
        label=FORM_PRINTS['login_label'],
        widget=forms.TextInput(attrs={'class': 'form-control'}),
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
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        error_messages={
            'min_length': FORM_PRINTS['password_min_length_error_msg'],
            'max_length': FORM_PRINTS['password_max_length_error_msg'],
            'required': FORM_PRINTS['password_required_error_msg'],
        })


class SignUpForm(forms.Form):
    def clean(self) -> dict[str, Any]:
        super().clean()  # self.cleaned_data: dict[str, Any] =

        self.check_password_confirmed()
        self.check_user_not_exists()
        # TODO: [check password reliability]

        return self.cleaned_data  # ??? Needs to be returned ?

    def check_password_confirmed(self) -> None:
        user_password: str | None = self.cleaned_data.get('user_password')
        user_password_confirm: str | None = self.cleaned_data.get(
            'user_password_confirm')

        if user_password is not None and user_password_confirm is not None \
                and user_password != user_password_confirm:
            raise ValidationError(FORM_PRINTS['password_confirm_error_msg'], )

    def check_user_not_exists(self) -> None:
        user_login: str | None = self.cleaned_data.get('user_login')
        if user_login is not None and self.is_user_exists():
            raise ValidationError(FORM_PRINTS['user_already_exists_error'])

    def is_user_exists(self) -> bool:
        try:
            users_with_the_login_count = len(
                User.objects.filter(login=self.cleaned_data['user_login']))
        except OperationalError:
            raise

        if users_with_the_login_count >= 1:
            return True
        return False

    user_login = forms.CharField(
        min_length=FORM_PRINTS['login_min_length'],
        max_length=FORM_PRINTS['login_max_length'],
        label=FORM_PRINTS['login_label'],
        widget=forms.TextInput(attrs={'class': 'form-control'}),
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
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        error_messages={
            'min_length': FORM_PRINTS['password_min_length_error_msg'],
            'max_length': FORM_PRINTS['password_max_length_error_msg'],
            'required': FORM_PRINTS['password_required_error_msg'],
        })

    user_password_confirm = forms.CharField(
        min_length=FORM_PRINTS['password_min_length'],
        max_length=FORM_PRINTS['password_max_length'],
        label=FORM_PRINTS['password_confirm_label'],
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        error_messages={
            'min_length': FORM_PRINTS['password_min_length_error_msg'],
            'max_length': FORM_PRINTS['password_max_length_error_msg'],
            'required': FORM_PRINTS['password_required_error_msg'],
        })


class SearchLocationForm(forms.Form):
    def clean(self) -> dict[str, Any]:  # FIXME: seems this funtion is useless.
        self.cleaned_data: dict[str, Any] = super().clean()
        return self.cleaned_data

    location_name = forms.CharField(
        max_length=FORM_PRINTS['location_name_max_length'],
        label=FORM_PRINTS['location_name_label'],
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        error_messages={
            'max_length': FORM_PRINTS['location_name_max_length_error_msg'],
            'required': FORM_PRINTS['field_required_error_msg'],
        }
    )


class AddLocationForm(forms.Form):
    def __init__(self, *args, request: HttpRequest | None = None, **kwargs):
        self.request: HttpRequest = request
        super(AddLocationForm, self).__init__(*args, **kwargs)

    def clean(self) -> dict[str, Any]:
        # FIXME: self.my_clean_data vs self.clean_data
        self.my_cleaned_data: dict[str, Any] = super().clean()
        self.set_location_name_from_session(self.request.session_service)
        self.check_location_name()
        return self.my_cleaned_data

    def set_location_name_from_session(self, session) -> None:
        self.location_name_in_session: str = ''
        location_info: dict[str, Any] | None = session.get('location_info')
        if location_info is None:
            raise ValidationError(
                FORM_PRINTS['location_addition_error'] + '_1')
        self.location_name_in_session: str = location_info.get('location_name')
        if self.location_name_in_session is None:
            raise ValidationError(
                FORM_PRINTS['location_addition_error'] + '_2')

    def check_location_name(self):
        if 'location_name' not in self.my_cleaned_data:
            raise ValidationError(FORM_PRINTS['location_addition_error'])

        if self.my_cleaned_data['location_name'] != self.location_name_in_session:
            raise ValidationError(FORM_PRINTS['location_addition_error'])

    location_name = forms.CharField(
        widget=forms.HiddenInput(),
        max_length=FORM_PRINTS['location_name_max_length'],
        error_messages={
            'max_length': FORM_PRINTS['location_name_max_length_error_msg'],
            'required': FORM_PRINTS['field_required_error_msg'],
        },
    )


class DeleteLocationForm(forms.Form):
    location_name = forms.CharField(
        widget=forms.HiddenInput(),
        max_length=FORM_PRINTS['location_name_max_length'],
        error_messages={
            'max_length': FORM_PRINTS['location_name_max_length_error_msg'],
            'required': FORM_PRINTS['field_required_error_msg'],
        },
    )
