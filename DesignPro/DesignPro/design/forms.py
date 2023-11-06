import re

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from .models import CustomUser
from .models import Request


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    full_name = forms.CharField(max_length=255)
    agree_to_terms = forms.BooleanField(required=True, label='Согласен на обработку персональных данных')

    class Meta:
        model = CustomUser
        fields = ("username", "email", "full_name", "password1", "password2", "agree_to_terms")

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not re.match("^[A-Za-z0-9]+$", username):
            raise ValidationError('Имя пользователя может содержать только буквы латиницы и цифры.')
        return username

    def clean_full_name(self):
        full_name = self.cleaned_data.get('full_name')
        if not re.match("^[А-Яа-яЁё\s]+$", full_name):
            raise ValidationError('ФИО может содержать только буквы кириллицы и пробелы.')
        return full_name

    def clean_agree_to_terms(self):
        agree_to_terms = self.cleaned_data.get('agree_to_terms')
        if not agree_to_terms:
            raise ValidationError('Вы должны согласиться на обработку персональных данных.')
        return agree_to_terms

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        user.full_name = self.cleaned_data["full_name"]
        if commit:
            user.save()
        return user


class ChangeRequestStatusForm(forms.ModelForm):
    comment = forms.CharField(required=False)
    design = forms.ImageField(required=False)

    class Meta:
        model = Request
        fields = ['status', 'comment', 'design']

    def clean(self):
        cleaned_data = super().clean()
        status = cleaned_data.get('status')
        comment = cleaned_data.get('comment')
        design = cleaned_data.get('design')

        if status == Request.IN_PROGRESS and not comment:
            self.add_error('comment', 'Комментарий обязателен при смене статуса на "Принято в работу".')
        elif status == Request.COMPLETED and not design:
            self.add_error('design', 'Дизайн обязателен при смене статуса на "Выполнено".')
