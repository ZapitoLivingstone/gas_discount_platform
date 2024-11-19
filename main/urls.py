from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.user_login, name='user_login'),
    path('logout/', views.user_logout, name='user_logout'),
    path('register/', views.register, name='register'),
    path('ingresar_solicitud/', views.ingresar_solicitud, name='ingresar_solicitud'),
    path('buscar_solicitud/', views.buscar_solicitud, name='buscar_solicitud'),
    path('detalle_solicitud/<str:rut>/', views.detalle_solicitud, name='detalle_solicitud'),
    path('listar_solicitudes/', views.listar_solicitudes, name='listar_solicitudes'),
    path('editar_solicitud/<int:solicitud_id>/', views.editar_solicitud, name='editar_solicitud'),
    path('eliminar_solicitud/<int:solicitud_id>/', views.eliminar_solicitud, name='eliminar_solicitud'),
    path('listar_usuarios/', views.listar_usuarios, name='listar_usuarios'),
    path('crear_usuario/', views.crear_usuario, name='crear_usuario'),
    path('perfil/', views.perfil, name='perfil'), 
    path('actualizar_perfil/', views.actualizar_perfil, name='actualizar_perfil'),
    path('eliminar_usuario/', views.eliminar_usuario, name='eliminar_usuario'),
    path('gestionar_contraseña/', views.gestionar_contraseña, name='gestionar_contraseña'),
    ]
