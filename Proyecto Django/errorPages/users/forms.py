from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from django.contrib.auth.forms import AuthenticationForm
import re
from django.core.exceptions import ValidationError

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['email', 'name', 'surname', 'control_number', 'age', 'tel',
                  'password1', 'password2']
        widgets = {
            'email': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Correo electrónico UTEZ',
                    'required': True,
                    'minlength': 17,
                    'maxlength': 30,
                    'pattern': "^[a-zA-Z0-9]+@utez\.edu\.mx$",
                    'title': "Ingresa un formato @utez.edu.mx",
                }
            ),
            'name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Nombre',
                    'required': True,
                    'minlength': 4,
                    'maxlength': 12,
                }
            ),
            'surname': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Apellido',
                    'required': True,
                    'minlength': 4,
                    'maxlength': 15,
                }
            ),
            'control_number': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Número de control UTEZ',
                    'required': True,
                    'minlength': 10,
                    'maxlength': 10,
                    'pattern': "^\d{5}[a-zA-Z]{2}\d{3}$",
                    'title': "Ingresa un formato de la UTEZ"
                }
            ),
            'age': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Edad',
                    'required': True,
                    'minlength': 1,
                    'maxlength': 2,
                    'title': "Edad no válida"
                }
            ),
            'tel': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Teléfono',
                    'required': True,
                    'minlength': 10,
                    'maxlength': 10,
                    'pattern': "^\d{10}$",
                    'title': "Ingresa un teléfono de 10 dígitos"
                }
            ),
            'password1': forms.PasswordInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Contraseña',
                    'id': 'id_password1',
                    'required': True,
                    'minlength': 8,
                    'title': "Debe tener al menos 8 caracteres, una mayúscula, un número y un carácter especial."
                }
            ),
            'password2': forms.PasswordInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Confirma tu contraseña',
                    'id': 'id_password2',
                    'required': True,
                    'minlength': 8,
                    'title': "Debe coincidir con la contraseña ingresada arriba."
                }
            ),
        }

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if not re.match(r"^[a-zA-Z0-9._%+-]+@utez\.edu\.mx$", email):
            raise ValidationError("El correo electrónico debe ser del dominio @utez.edu.mx.")
        return email

    def clean_name(self):
        name = self.cleaned_data.get("name")
        if len(name) < 2:
            raise ValidationError("El nombre debe tener al menos 2 caracteres.")
        if len(name) > 50:
            raise ValidationError("El nombre no puede tener más de 50 caracteres.")
        
        return name
    
    def clean_control_number(self):
        control_number = self.cleaned_data.get("control_number")
        if len(control_number) != 10:
            raise ValidationError("La matrícula debe tener exactamente 10 caracteres.")
        if not re.match(r"^\d{5}[a-z]{2}\d{3}$", control_number):
            raise ValidationError("El número de control debe tener el formato correcto: 5 números, 2 letras minúsculas y 3 números (ejemplo: 20223tn134).")
        return control_number
        
    def clean_tel(self):
        tel = self.cleaned_data.get("tel")
        if len(tel) != 10 or not re.match(r'^\d{10}$', tel):
            raise ValidationError("El teléfono debe tener exactamente 10 dígitos.")
        return tel

    def clean_password1(self):
        password = self.cleaned_data.get("password1")
        if not re.match(r"^(?=.*[0-9])(?=.*[A-Z])(?=.*[!#$%^&*]).{8,}$", password):
            raise ValidationError("La contraseña debe tener al menos 8 caracteres, contener un número, una letra mayúscula y un símbolo especial (!, #, $, %, ^, &, *).")
        return password

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise ValidationError("Las contraseñas no coinciden.")
        
        return cleaned_data
        
class CustomUserLoginForm(AuthenticationForm):
    class Meta:
        model = CustomUser
        fields = ['email', 'password']
        widgets = {
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Correo electrónico',
                'required': True,
                'pattern': '^[a-zA-Z0-9]+@utez\.edu\.mx$',
                'title': 'El correo debe tener el dominio @utez.edu.mx'
            }),
            'password': forms.PasswordInput(attrs={
                'class': 'form-control',
                'placeholder': 'Contraseña',
                'required': True,
                'minlength': 8,
                'pattern': '^(?=.*[A-Z])(?=.*[0-9])(?=.*[!@#$%^&*])[a-zA-Z0-9!@#$%^&*]{8,}$',
                'title': 'La contraseña debe tener al menos 8 caracteres, incluir 1 número, 1 letra mayúscula y 1 carácter especial'
            }),
        }
