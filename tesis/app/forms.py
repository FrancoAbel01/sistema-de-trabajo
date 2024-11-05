from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'execution_date', 'start_time', 'end_time']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el título de la Actividad',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese la descripción de la Actividad',
                'rows': 5,
            }),
            'execution_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),
            'start_time': forms.TimeInput(attrs={
                'type': 'time',
                'class': 'form-control'
            }),
            'end_time': forms.TimeInput(attrs={
                'type': 'time',
                'class': 'form-control'
            }),
        }

class RegistroForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Correo electrónico'
        })
    )
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nombre de usuario'
        })
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Contraseña'
        })
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirmar contraseña'
        })
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


# class CustomAuthenticationForm(AuthenticationForm):
#     username = forms.CharField(
#         widget=forms.TextInput(attrs={
#             'class': 'form-control',
#             'placeholder': 'Nombre de usuario'
#         })
#     )
#     password = forms.CharField(
#         widget=forms.PasswordInput(attrs={
#             'class': 'form-control',
#             'placeholder': 'Contraseña'
#         })
#     )
#     class Meta:
#         model = User
#         fields = ['username','password']


from django import forms
from .models import PersonalTask

class PersonalTaskForm(forms.ModelForm):
    class Meta:
        model = PersonalTask
        fields = ['title', 'description', 'execution_date', 'start_time', 'end_time']
        widgets = {
            'execution_date': forms.DateInput(attrs={'type': 'date'}),
            'start_time': forms.TimeInput(attrs={'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'type': 'time'}),
        }
