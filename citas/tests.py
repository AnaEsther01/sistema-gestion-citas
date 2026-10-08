from django.test import TestCase
from django.contrib.auth.models import User
from .models import Cliente
from django.forms import modelform_factory
from .models import Servicio, Empleado, EstadoCita, Cita


class ValidacionFase4Tests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='qa_fase4')
        self.client.force_login(self.user)

    def test_obligatorios_no_guardan(self):
        response = self.client.post('/clientes/crear/', {})
        self.assertContains(response, 'Este campo es obligatorio.', count=2)
        self.assertEqual(Cliente.objects.count(), 0)

    def test_correo_invalido_no_guarda(self):
        response = self.client.post('/clientes/crear/', {
            'nombre': 'QA', 'apellido': 'Fase4', 'correo': 'correo-invalido'})
        self.assertContains(response, 'Introduzca una dirección de correo electrónico válida.')
        self.assertEqual(Cliente.objects.count(), 0)

    def test_actualizacion_invalida_conserva_registro(self):
        cliente = Cliente.objects.create(nombre='QA', apellido='Original', correo='qa@example.com')
        self.client.post(f'/clientes/{cliente.pk}/actualizar/', {
            'nombre': '', 'apellido': 'Alterado', 'correo': 'invalido'})
        cliente.refresh_from_db()
        self.assertEqual((cliente.nombre, cliente.apellido, cliente.correo),
                         ('QA', 'Original', 'qa@example.com'))

    def test_tipos_numericos_servicio(self):
        form_class = modelform_factory(Servicio, fields='__all__')
        form = form_class(data={'nombre': 'QA', 'precio': 'abc', 'duracion_minutos': 'xyz'})
        self.assertFalse(form.is_valid())
        self.assertIn('precio', form.errors)
        self.assertIn('duracion_minutos', form.errors)
        self.assertEqual(Servicio.objects.count(), 0)

    def test_rutas_y_404(self):
        for url in ['/', '/clientes/', '/clientes/crear/', '/login/', '/registro/']:
            self.assertEqual(self.client.get(url).status_code, 200, url)
        self.assertEqual(self.client.get('/ruta-inexistente-fase4/').status_code, 404)

    def test_borrado_relacionado_no_deja_huerfanos(self):
        cliente = Cliente.objects.create(nombre='QA', apellido='Temporal')
        empleado = Empleado.objects.create(nombre='QA', apellido='Empleado')
        servicio = Servicio.objects.create(nombre='QA', precio='50.00', duracion_minutos=30)
        estado = EstadoCita.objects.create(nombre='Prueba')
        cita = Cita.objects.create(cliente=cliente, empleado=empleado, servicio=servicio,
                                   estado=estado, fecha='2026-09-29', hora='10:00')
        self.client.post(f'/clientes/{cliente.pk}/eliminar/')
        self.assertFalse(Cita.objects.filter(pk=cita.pk).exists())
        self.assertTrue(Empleado.objects.filter(pk=empleado.pk).exists())
        self.assertTrue(Servicio.objects.filter(pk=servicio.pk).exists())


class PanelYBusquedaTests(TestCase):
    def test_panel_publico_no_expone_clientes(self):
        Cliente.objects.create(nombre='Privado', apellido='Reservado')
        respuesta = self.client.get('/')
        self.assertNotContains(respuesta, 'Privado')
        self.assertNotIn('total_clientes', respuesta.context)

    def test_panel_y_busqueda_autenticada(self):
        self.client.force_login(User.objects.create_user(username='panel'))
        Cliente.objects.create(nombre='Lucia', apellido='Prueba', correo='lucia@example.com')
        Cliente.objects.create(nombre='Mario', apellido='Otro', telefono='12345')
        respuesta = self.client.get('/')
        self.assertEqual(respuesta.context['total_clientes'], 2)
        self.assertContains(respuesta, 'Lucia Prueba')
        for consulta in ['lucia', 'Prueba', 'lucia@example.com']:
            resultado = self.client.get('/clientes/', {'q': consulta})
            self.assertContains(resultado, 'Lucia Prueba')
            self.assertNotContains(resultado, 'Mario Otro')
        self.assertContains(self.client.get('/clientes/', {'q': '12345'}), 'Mario Otro')
        self.assertContains(self.client.get('/clientes/', {'q': 'inexistente'}), 'No encontramos coincidencias')


class FlujoClientesTests(TestCase):
    def test_acceso_restringido(self):
        for url in ['/clientes/', '/clientes/crear/',
                    '/clientes/1/actualizar/', '/clientes/1/eliminar/']:
            self.assertEqual(self.client.get(url).status_code, 302)

    def test_registro_login_crud_logout(self):
        password = 'ClavePrueba!Fase3_2026'
        response = self.client.post('/registro/', {
            'username': 'prueba', 'password1': password, 'password2': password})
        self.assertRedirects(response, '/')
        self.assertTrue(User.objects.filter(username='prueba').exists())
        self.assertEqual(self.client.get('/logout/').status_code, 405)
        self.client.post('/logout/')
        self.assertNotIn('_auth_user_id', self.client.session)
        self.assertRedirects(self.client.post('/login/', {
            'username': 'prueba', 'password': password}), '/')
        self.client.post('/clientes/crear/', {'nombre': 'Cliente', 'apellido': 'Prueba'})
        cliente = Cliente.objects.get(nombre='Cliente')
        self.assertContains(self.client.get('/clientes/'), 'Cliente Prueba')
        self.client.post(f'/clientes/{cliente.pk}/actualizar/', {
            'nombre': 'Cliente', 'apellido': 'Actualizado'})
        cliente.refresh_from_db()
        self.assertEqual(cliente.apellido, 'Actualizado')
        self.assertEqual(self.client.get(f'/clientes/{cliente.pk}/eliminar/').status_code, 200)
        self.assertTrue(Cliente.objects.filter(pk=cliente.pk).exists())
        self.client.post(f'/clientes/{cliente.pk}/eliminar/')
        self.assertFalse(Cliente.objects.filter(pk=cliente.pk).exists())
        self.assertEqual(self.client.get(f'/clientes/{cliente.pk}/actualizar/').status_code, 404)
