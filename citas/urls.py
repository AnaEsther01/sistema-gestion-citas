from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('registro/', views.registro, name='registro'),
    path('login/', views.iniciar_sesion, name='login'),
    path('logout/', views.cerrar_sesion, name='logout'),
    path('clientes/', views.clientes, name='clientes'),
    path('clientes/crear/', views.crear_cliente, name='crear_cliente'),
    path('clientes/<int:id_cliente>/actualizar/', views.actualizar_cliente, name='actualizar_cliente'),
    path('clientes/<int:id_cliente>/eliminar/', views.eliminar_cliente, name='eliminar_cliente'),
]