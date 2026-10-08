from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.db.models import Q
from django.utils import timezone
from .models import Cliente, Cita, Servicio
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
    contexto = {}
    # El panel muestra datos reales solo después de iniciar sesión.
    if request.user.is_authenticated:
        hoy = timezone.localdate()
        contexto = {
            'total_clientes': Cliente.objects.count(),
            'citas_hoy': Cita.objects.filter(fecha=hoy).count(),
            'total_servicios': Servicio.objects.count(),
            'ultimos_clientes': Cliente.objects.order_by('-pk')[:4],
            'proximas_citas': Cita.objects.filter(fecha__gte=hoy)
                .select_related('cliente', 'servicio', 'estado')
                .order_by('fecha', 'hora')[:4],
        }
    return render(request, 'citas/inicio.html', contexto)


@login_required(login_url='login')
def clientes(request):
    busqueda = request.GET.get('q', '').strip()[:150]
    lista_clientes = Cliente.objects.order_by('nombre', 'apellido', 'pk')
    if busqueda:
        lista_clientes = lista_clientes.filter(
            Q(nombre__icontains=busqueda) | Q(apellido__icontains=busqueda)
            | Q(correo__icontains=busqueda) | Q(telefono__icontains=busqueda))
    return render(request, 'citas/clientes.html', {
        'busqueda': busqueda,
        'total_clientes': Cliente.objects.count(),
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
