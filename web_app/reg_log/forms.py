from .models import Users
from django.forms import ModelForm, TextInput, EmailInput, PasswordInput, FileInput


class UserRegForm(ModelForm):
    class Meta:
        model = Users
        fields = ['Name', 'Surname', 'Email', 'Age', 'Pass1', 'Pass2', 'Face']

        widgets = {
            "Name": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Имя'
            }),
            "Surname": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Фамилия'
            }),
            "Email": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Почта'
            }),
            "Age": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Возраст'
            }),
            "Pass1": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Пароль',
                'type': 'password'
            }),
            "Pass2": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Повторите пароль',
                'type': 'password'
            }),
            "Face": FileInput(attrs={
                'class': 'form-control',
                'type': 'file',
            })
        }


class UserLogForm(ModelForm):
    class Meta:
        model = Users
        fields = ['Email', 'Pass1']

        widgets = {
            "Email": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Почта'
            }),
            "Pass1": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Пароль',
                'type': 'password'
            })
        }
