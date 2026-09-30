from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Cliente
from .forms import ClienteForm

def registro(request):
    if request.method == 'POST':
        formulario = UserCreationForm(request.POST)

        if formulario.is_valid():
            usuario = formulario.save()
            login(request, usuario)
            return redirect('inicio')
    else:
        formulario = UserCreationForm()

    return render(request, 'citas/registro.html', {
        'formulario': formulario
    })


def iniciar_sesion(request):
    if request.method == 'POST':
        formulario = AuthenticationForm(request, data=request.POST)

        if formulario.is_valid():
            usuario = formulario.get_user()
            login(request, usuario)
            return redirect('inicio')
    else:
        formulario = AuthenticationForm()

    return render(request, 'citas/login.html', {
        'formulario': formulario
    })


@require_POST
def cerrar_sesion(request):
    logout(request)
    messages.success(request, 'Sesión cerrada correctamente.')
    return redirect('inicio')

def inicio(request):
    return render(request, 'citas/inicio.html')


@login_required(login_url='login')
def clientes(request):
    lista_clientes = Cliente.objects.all()
    return render(request, 'citas/clientes.html', {
        'clientes': lista_clientes
    })


@login_required(login_url='login')
def crear_cliente(request):
    if request.method == 'POST':
        formulario = ClienteForm(request.POST)

        if formulario.is_valid():
            formulario.save()
            messages.success(request, 'Cliente creado correctamente.')
            return redirect('clientes')
    else:
        formulario = ClienteForm()

    return render(request, 'citas/crear_cliente.html', {
        'formulario': formulario
    })

@login_required(login_url='login')
def actualizar_cliente(request, id_cliente):
    cliente = get_object_or_404(Cliente, id_cliente=id_cliente)

    if request.method == 'POST':
        formulario = ClienteForm(request.POST, instance=cliente)

        if formulario.is_valid():
            formulario.save()
            messages.success(request, 'Cliente actualizado correctamente.')
            return redirect('clientes')
    else:
        formulario = ClienteForm(instance=cliente)

    return render(request, 'citas/actualizar_cliente.html', {
        'formulario': formulario,
        'cliente': cliente
    })

@login_required(login_url='login')
def eliminar_cliente(request, id_cliente):
    cliente = get_object_or_404(Cliente, id_cliente=id_cliente)

    if request.method == 'POST':
        cliente.delete()
        messages.success(request, 'Cliente eliminado correctamente.')
        return redirect('clientes')

    return render(request, 'citas/eliminar_cliente.html', {
        'cliente': cliente
    })
