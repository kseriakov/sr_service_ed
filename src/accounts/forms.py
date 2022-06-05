from django import forms
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.hashers import check_password
from django.core.exceptions import ValidationError

from scraping.models import City, Language

user_model = get_user_model()


class UserLoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def clean(self, *args, **kwargs):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        print(password)

        if email and password:
            user_list = user_model.objects.filter(email=email)
            if not user_list.exists():
                raise ValidationError('Введен неверный email')
            if not check_password(password=password, encoded=user_list.first().password):
                raise ValidationError('Введен неверный пароль')

            user = authenticate(email=email, password=password)
            if not user.is_active:
                raise ValidationError('Аккаунт данного пользователя отключен')

        return super().clean()


class UserRegisterForm(forms.ModelForm):
    password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = user_model
        fields = ('email', 'password')

        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'})
        }

    def clean_password2(self):
        data = self.cleaned_data
        psw = data.get('password')
        psw2 = data.get('password2')
        if psw != psw2:
            raise ValidationError('Пароли не совпадают')
        return psw2


class UserUpdateSettings(forms.ModelForm):
    class Meta:
        model = user_model
        fields = ('city', 'language', 'send_mail')
        widgets = {
            'city': forms.Select(attrs={'class': 'form-control'}),
            'language': forms.Select(attrs={'class': 'form-control'}),
        }

