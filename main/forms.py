from django import forms
from .models import Solicitud
from django.contrib.auth.models import User

import re

class SolicitudForm(forms.ModelForm):
    class Meta:
        model = Solicitud
        fields = ['rut', 'nombre', 'apellidos', 'direccion', 'telefono', 'comuna']

    def clean_rut(self):
        rut = self.cleaned_data.get('rut')
        if not rut:
            raise forms.ValidationError("Este campo es obligatorio.")

        # Normalizar el RUT: eliminar puntos, guiones y convertir a mayúsculas
        rut = rut.replace('.', '').replace('-', '').upper()

        # Validar el formato básico del RUT (cuerpo + dígito verificador)
        if not re.match(r'^\d{7,8}[0-9K]$', rut):
            raise forms.ValidationError(
                "El RUT ingresado no tiene un formato válido. Ejemplo: 12345678-K."
            )

        # Permitir RUTs inventados sin validar el dígito verificador
        return rut

    def clean_telefono(self):
        telefono = self.cleaned_data.get('telefono')
        if not telefono:
            raise forms.ValidationError("Este campo es obligatorio.")

        # Eliminar caracteres adicionales como espacios y guiones
        telefono = telefono.replace(' ', '').replace('-', '')

        # Validar que contenga exactamente 9 dígitos
        if not re.match(r'^\d{9}$', telefono):
            raise forms.ValidationError(
                "El número de teléfono debe contener 9 dígitos. Ejemplo: 912345678."
            )

        return telefono


class BuscarUsuarioForm(forms.Form):
    email = forms.EmailField(label="Correo Electrónico", required=True)

class PerfilForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(), required=False, label="Nueva Contraseña"
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(), required=False, label="Confirmar Nueva Contraseña"
    )

    class Meta:
        model = User
        fields = ['username', 'email']

    def clean(self):
        cleaned_data = super().clean()

        # Validación de las contraseñas nuevas
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')
        if password:
            if password != password2:
                raise forms.ValidationError("Las nuevas contraseñas no coinciden.")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)

        # Solo actualizamos la contraseña si el campo 'password' tiene valor
        if self.cleaned_data['password']:
            user.set_password(self.cleaned_data['password'])  # Establece la nueva contraseña encriptada

        if commit:
            user.save()
        return user