from django.shortcuts import render, redirect, get_object_or_404
from .forms import PerfilForm, SolicitudForm,BuscarUsuarioForm
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import PasswordChangeForm, UserChangeForm
from django.contrib.auth.hashers import make_password 
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse
from .models import Solicitud
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.contrib.auth.password_validation import validate_password

def is_admin(user):
    return user.groups.filter(name='Administrador').exists()
    return user.is_superuser

def is_vendedor(user):
    return user.groups.filter(name='Vendedor').exists()



@login_required
@user_passes_test(is_vendedor)
def detalle_solicitud(request, rut):
    solicitud = get_object_or_404(Solicitud, rut=str(rut))
    return render(request, 'main/detalle_solicitud.html', {'solicitud': solicitud})

from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User

def restablecer_contraseña(request, user_id):
    usuario = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        nueva_contraseña = request.POST.get('nueva_contraseña')
        confirmar_contraseña = request.POST.get('confirmar_contraseña')

        if nueva_contraseña != confirmar_contraseña:
            messages.error(request, "Las contraseñas no coinciden.")
            return redirect('restablecer_contraseña', user_id=user_id)

        usuario.set_password(nueva_contraseña)
        usuario.save()
        messages.success(request, "Contraseña cambiada exitosamente.")
        return redirect('listar_usuarios')

    return render(request, 'main/restablecer_contraseña.html', {'usuario': usuario})

def gestionar_contraseña(request):
    usuario = None 
    if request.method == 'POST':
        if 'buscar_usuario' in request.POST:
            email = request.POST.get('email')
            if not email:  # Validar si el campo de email está vacío
                messages.error(request, "Por favor, ingresa un correo electrónico.")
            else:
                try:
                    usuario = User.objects.get(email=email)
                except User.DoesNotExist:
                    messages.error(request, "No se encontró un usuario con ese correo.")
        
        elif 'cambiar_contraseña' in request.POST:
            user_id = request.POST.get('user_id')
            nueva_contraseña = request.POST.get('nueva_contraseña')
            confirmar_contraseña = request.POST.get('confirmar_contraseña')

            if not nueva_contraseña:
                messages.error(request, "Por favor, ingresa una nueva contraseña.")
            elif not confirmar_contraseña:
                messages.error(request, "Por favor, confirma la nueva contraseña.")
            elif nueva_contraseña != confirmar_contraseña:
                messages.error(request, "Las contraseñas no coinciden.")
            elif len(nueva_contraseña) < 8:  # Ejemplo de validación de longitud
                messages.error(request, "La contraseña debe tener al menos 8 caracteres.")
            else:
                usuario = get_object_or_404(User, id=user_id)
                usuario.password = make_password(nueva_contraseña)
                usuario.save()
                messages.success(request, "Contraseña cambiada exitosamente.")
                return redirect('listar_usuarios')

    return render(request, 'main/gestionar_contraseña.html', {'usuario': usuario})
@login_required
def perfil(request):
    form_errors = {}
    if request.method == 'POST':
        form = UserChangeForm(request.POST, instance=request.user)
        
        if not form.is_valid():
            nombre = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            confirm_password = form.cleaned_data.get('password2')

            if not nombre:
                form_errors['nombre'] = 'El nombre completo es obligatorio.'
            
            if not email:
                form_errors['email'] = 'El correo electrónico es obligatorio.'
            elif '@' not in email:
                form_errors['email'] = 'Ingresa un correo electrónico válido.'
            
            if password and len(password) < 6:
                form_errors['password'] = 'La contraseña debe tener al menos 6 caracteres.'
            
            if password and confirm_password and password != confirm_password:
                form_errors['confirm_password'] = 'Las contraseñas no coinciden.'
            
            if form_errors:
                return render(request, 'main/perfil.html', {'form_errors': form_errors, 'form': form, 'usuario': request.user})

        if form.is_valid():
            form.save()
            return redirect('perfil') 
    else:
        form = UserChangeForm(instance=request.user)
    
    return render(request, 'main/perfil.html', {'form': form, 'usuario': request.user})



@login_required
@user_passes_test(is_admin)
def editar_solicitud(request, solicitud_id):
    solicitud = get_object_or_404(Solicitud, id=solicitud_id)

    if request.method == 'POST':
        estado = request.POST.get('estado')
        nombre = request.POST.get('nombre')
        apellidos = request.POST.get('apellidos')
        direccion = request.POST.get('direccion')
        telefono = request.POST.get('telefono')
        comuna = request.POST.get('comuna')

        # Validar campos obligatorios
        form_errors = {}
        
        if not estado:
            form_errors['estado'] = 'El estado es obligatorio.'
        if not nombre:
            form_errors['nombre'] = 'El nombre es obligatorio.'
        if not apellidos:
            form_errors['apellidos'] = 'Los apellidos son obligatorios.'
        if not direccion:
            form_errors['direccion'] = 'La dirección es obligatoria.'
        if not telefono:
            form_errors['telefono'] = 'El teléfono es obligatorio.'
        elif not re.match(r'^\d{9}$', telefono):  # Validar que el teléfono tenga 9 dígitos
            form_errors['telefono'] = 'El número de teléfono debe tener 9 dígitos.'
        if not comuna:
            form_errors['comuna'] = 'La comuna es obligatoria.'

        if form_errors:
            # Renderizar de nuevo la lista de solicitudes con los errores
            return render(request, 'main/listar_solicitudes.html', {
                'form_errors': form_errors,
                'solicitudes': Solicitud.objects.all(),  # Asegúrate de pasar todas las solicitudes
                'solicitud': solicitud  # Para mantener el contexto del modal
            })

        # Actualizar los campos
        solicitud.estado = estado
        solicitud.nombre = nombre
        solicitud.apellidos = apellidos
        solicitud.direccion = direccion
        solicitud.telefono = telefono
        solicitud.comuna = comuna
        solicitud.save()

        messages.success(request, "Solicitud actualizada exitosamente.")
        return redirect('listar_solicitudes')

    return render(request, 'main/listar_solicitudes.html', {'solicitudes': Solicitud.objects.all()})


@login_required
@user_passes_test(is_admin)
def eliminar_solicitud(request, solicitud_id):
    try:
        solicitud = Solicitud.objects.get(id=solicitud_id)
        solicitud.delete()
        messages.success(request, "Solicitud eliminada exitosamente.")
    except Solicitud.DoesNotExist:
        messages.error(request, "Solicitud no encontrada.")

    return redirect('listar_solicitudes')



@login_required
def perfil_view(request):
    user = request.user
    if request.method == 'POST':
        form = PerfilForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('perfil')  
    else:
        form = PerfilForm(instance=user)

    return render(request, 'main/perfil.html', {'form': form})
@login_required
def actualizar_perfil(request):
    usuario = request.user
    if request.method == 'POST':
        password = request.POST.get('password')
        if password:
            usuario.set_password(password)
            usuario.save()
            update_session_auth_hash(request, usuario)  
        form = PerfilForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            return redirect('perfil')  
    return redirect('perfil')  

@login_required
def index(request):
    is_admin = request.user.groups.filter(name="Administrador").exists()
    is_vendedor = request.user.groups.filter(name="Vendedor").exists()
    context = {
        'is_admin': is_admin,
        'is_vendedor': is_vendedor,
    }
    return render(request, 'main/base.html', context)
def index(request):
    user_roles = {
        'is_admin': False,
        'is_vendedor': False,
        'is_user': False,
    }

    if request.user.is_authenticated:
        user_roles['is_admin'] = request.user.groups.filter(name='Administrador').exists()
        user_roles['is_vendedor'] = request.user.groups.filter(name='Vendedor').exists()
        user_roles['is_user'] = not (user_roles['is_admin'] or user_roles['is_vendedor'])

    return render(request, 'main/index.html', user_roles)

import re

def validar_rut(rut):
    # Elimina puntos y guiones
    rut = rut.replace('.', '').replace('-', '')
    # Verifica el formato
    if not re.match(r'^\d{7,8}[0-9kK]$', rut):
        return False
    # Aquí puedes agregar más lógica para verificar el dígito verificador si es necesario
    return True

@login_required
@user_passes_test(is_vendedor)
def buscar_solicitud(request):
    solicitudes = None
    error_message = None
    if request.method == 'POST':
        rut = request.POST.get('rut', '').strip()
        
        # Validación para campo vacío
        if not rut:
            error_message = "Por favor, ingresa un RUT."
        elif not validar_rut(rut):
            error_message = "El RUT ingresado no es válido."
        else:
            solicitudes = Solicitud.objects.filter(rut__icontains=rut)  
    return render(request, 'main/buscar_solicitud.html', {'solicitudes': solicitudes, 'error_message': error_message})

    
def restablecer_contraseña(request, user_id):
    usuario = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        nueva_contraseña = request.POST.get('nueva_contraseña')
        confirmar_contraseña = request.POST.get('confirmar_contraseña')

        if nueva_contraseña != confirmar_contraseña:
            messages.error(request, "Las contraseñas no coinciden.")
            return redirect('restablecer_contraseña', user_id=user_id)

        usuario.set_password(nueva_contraseña)
        usuario.save()

        messages.success(request, "Contraseña cambiada exitosamente.")
        return redirect('listar_usuarios')  

    return render(request, 'main/restablecer_contraseña.html', {'usuario': usuario})


def ingresar_solicitud(request):
    if request.method == 'POST':
        form = SolicitudForm(request.POST)
        if form.is_valid():
            solicitud = form.save(commit=False)
            
            if request.user.is_authenticated:
                solicitud.usuario = request.user
            else:
                solicitud.usuario = None 

            solicitud.save()  
            return redirect('index')  
    else:
        form = SolicitudForm()
    
    return render(request, 'main/ingresar_solicitud.html', {'form': form})


@login_required
@user_passes_test(is_admin)
def eliminar_usuario(request):
    if request.method == 'POST':
        usuario_id = request.POST.get('usuario_id')

        if not usuario_id:
            messages.error(request, "No se proporcionó un ID de usuario.")
            return redirect('listar_usuarios')

        try:
            usuario = User.objects.get(id=usuario_id)

            if usuario.is_superuser:
                messages.error(request, "No puedes eliminar a un superusuario.")
                return redirect('listar_usuarios')

            usuario.delete()
            messages.success(request, f"Usuario {usuario.username} eliminado exitosamente.")
            return redirect('listar_usuarios')

        except User.DoesNotExist:
            messages.error(request, "Usuario no encontrado.")
            return redirect('listar_usuarios')
        except Exception as e:
            messages.error(request, f"Error al eliminar usuario: {e}")
            return redirect('listar_usuarios')

    return redirect('listar_usuarios')

@login_required
@user_passes_test(is_admin)
def listar_solicitudes(request):
    solicitudes = Solicitud.objects.all() 
    
    for solicitud in solicitudes:
        solicitud.cambiar_estado()  

    if request.method == 'POST':
        solicitud_id = request.POST.get('solicitud_id')
        nuevo_estado = request.POST.get('estado')
        
        if solicitud_id and nuevo_estado:
            solicitud = Solicitud.objects.get(id=solicitud_id)
            solicitud.estado = nuevo_estado
            solicitud.save()

    return render(request, 'main/listar_solicitudes.html', {'solicitudes': solicitudes})

# Vista para listar usuarios (solo administradores)

@login_required
@user_passes_test(is_admin)
def listar_usuarios(request):
    usuarios = User.objects.all().prefetch_related('groups')
    return render(request, 'main/listar_usuarios.html', {'usuarios': usuarios})


@login_required
@user_passes_test(is_admin)
def crear_usuario(request):
    if request.method == 'POST':
        form_errors = {}
        nombre = request.POST.get('nombre', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '').strip()
        confirm_password = request.POST.get('confirm_password', '').strip()
        role = request.POST.get('role', '').strip()

        if not nombre:
            form_errors['nombre'] = 'El nombre completo es obligatorio.'
        if not email:
            form_errors['email'] = 'El correo electrónico es obligatorio.'
        if not password:
            form_errors['password'] = 'La contraseña es obligatoria.'
        elif len(password) < 6:
            form_errors['password'] = 'La contraseña debe tener al menos 6 caracteres.'
        if password != confirm_password:
            form_errors['confirm_password'] = 'Las contraseñas no coinciden.'

        if form_errors:
            return render(request, 'main/crear_usuario.html', {'form_errors': form_errors, 'request': request})

        nuevo_usuario = User.objects.create_user(
            username=email.split('@')[0],  # Usa parte del correo como username
            email=email,
            password=password,
            first_name=nombre.split(' ')[0],
            last_name=' '.join(nombre.split(' ')[1:])
        )

        if role:
            grupo, created = Group.objects.get_or_create(name=role)
            nuevo_usuario.groups.add(grupo)
        
        return redirect('listar_usuarios')

    return render(request, 'main/crear_usuario.html')


# Vista de inicio de sesión
def user_login(request):
    if request.user.is_authenticated:
        return redirect('index')  # Redirigir si el usuario ya está logueado
    
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '').strip()

        # Variables para los mensajes de error
        error_email = None
        error_password = None

        # Validación de campos vacíos
        if not email:
            error_email = "El correo electrónico es obligatorio."
        if not password:
            error_password = "La contraseña es obligatoria."

        # Validación del correo electrónico
        if not error_email:  # Solo si el correo no está vacío
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                error_email = "Este correo electrónico no está registrado."

        # Validación de la contraseña
        if not error_email and not error_password:  # Solo si el correo existe
            user = authenticate(request, username=user.username, password=password)
            if user is None:
                error_password = "Contraseña incorrecta."

        # Si hay errores, se vuelve a renderizar con los mensajes de error
        if error_email or error_password:
            return render(request, 'main/login.html', {
                'error_email': error_email,
                'error_password': error_password,
                'email': email  # Se pasa el correo para que el usuario no lo tenga que escribir de nuevo
            })

        # Si la autenticación es exitosa, se hace login y se redirige al inicio
        login(request, user)
        return redirect('index')

    return render(request, 'main/login.html')
    
def user_logout(request):
    logout(request)
    return redirect('user_login')




def register(request):
    if request.method == 'POST':
        errors = {}
        username = request.POST.get('nombre', '').strip()
        password = request.POST.get('password', '').strip()
        confirm_password = request.POST.get('confirm_password', '').strip()
        email = request.POST.get('email', '').strip()

        # Validación del nombre
        if not username:
            errors['nombre'] = 'El nombre completo es obligatorio.'
        elif len(username) < 3:
            errors['nombre'] = 'El nombre debe tener al menos 3 caracteres.'
        elif not username.replace(' ', '').isalpha():
            errors['nombre'] = 'El nombre solo debe contener letras.'
        elif User.objects.filter(username=username).exists():
            errors['nombre'] = 'El nombre de usuario ya existe.'

        # Validación del email
        if not email:
            errors['email'] = 'El correo electrónico es obligatorio.'
        else:
            try:
                validate_email(email)
                if User.objects.filter(email=email).exists():
                    errors['email'] = 'El correo electrónico ya está en uso.'
            except ValidationError:
                errors['email'] = 'Correo electrónico inválido.'

        # Validación de la contraseña
        if not password:
            errors['password'] = 'La contraseña es obligatoria.'
        elif len(password) < 8:
            errors['password'] = 'La contraseña debe tener al menos 8 caracteres.'
        else:
            try:
                validate_password(password)
            except ValidationError as e:
                errors['password'] = list(e.messages)[0]

        # Validación de confirmación de contraseña
        if not confirm_password:
            errors['confirm_password'] = 'Debe confirmar la contraseña.'
        elif password != confirm_password:
            errors['confirm_password'] = 'Las contraseñas no coinciden.'

        # Si hay errores, los paso a la plantilla
        if errors:
            context = {
                'errors': errors,
                'old_data': {
                    'nombre': username,
                    'email': email,
                }
            }
            return render(request, 'main/register.html', context)

        # Si no hay errores, se crea el usuario
        try:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )
            user = authenticate(request, username=username, password=password)
            login(request, user)
            return redirect('user_login')  # Redirige a la página de login o perfil después de registro
        except Exception as e:
            errors['general'] = 'Error al crear el usuario. Por favor, intente nuevamente.'
            return render(request, 'main/register.html', {'errors': errors})

    return render(request, 'main/register.html')
