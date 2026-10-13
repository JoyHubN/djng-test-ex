import re
from django import forms
from django.contrib.auth.forms import UserCreationForm
from users.models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    name = forms.CharField(max_length=150, label="Имя", widget=forms.TextInput(attrs={'placeholder': 'Кириллица, пробел, тире'}))
    surname = forms.CharField(max_length=150, label="Фамилия", widget=forms.TextInput(attrs={'placeholder': 'Кириллица, пробел, тире'}))
    patronymic = forms.CharField(max_length=150, required=False, label="Отчество", widget=forms.TextInput(attrs={'placeholder': 'Необязательно'}))
    email = forms.EmailField(label="Email")
    password1_reg = forms.CharField(label="Пароль", widget=forms.PasswordInput)
    password_repeat = forms.CharField(label="Повтор пароля", widget=forms.PasswordInput)
    rules = forms.BooleanField(label="Согласие с правилами регистрации", required=True)

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'name', 'surname', 'patronymic')

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if not re.match(r'^[А-Яа-яЁё\s\-]+$', name):
            raise forms.ValidationError("Разрешены только кириллица, пробел и тире.")
        return name

    def clean_surname(self):
        surname = self.cleaned_data.get('surname')
        if not re.match(r'^[А-Яа-яЁё\s\-]+$', surname):
            raise forms.ValidationError("Разрешены только кириллица, пробел и тире.")
        return surname

    def clean_patronymic(self):
        patronymic = self.cleaned_data.get('patronymic')
        if patronymic and not re.match(r'^[А-Яа-яЁё\s\-]+$', patronymic):
            raise forms.ValidationError("Разрешены только кириллица, пробел и тире.")
        return patronymic

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not re.match(r'^[A-Za-z0-9\-]+$', username):
            raise forms.ValidationError("Логин может содержать только латиницу, цифры и тире.")
        return username

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password1_reg') or cleaned_data.get('password1')
        password_repeat = cleaned_data.get('password_repeat')

        if password and len(password) < 6:
            self.add_error('password1_reg', "Пароль должен быть не менее 6 символов.")

        if password and password_repeat and password != password_repeat:
            self.add_error('password_repeat', "Пароли должны совпадать.")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data.get('name')
        user.last_name = self.cleaned_data.get('surname')
        user.patronymic = self.cleaned_data.get('patronymic')
        user.email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password1_reg')
        if password:
            user.set_password(password)
        if commit:
            user.save()
        return user
