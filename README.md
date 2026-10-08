# Sistema de gestión de citas

Proyecto académico desarrollado con Python y Django. Base de datos configurada: MySQL/MariaDB.

## Funciones implementadas
- Registro, inicio y cierre de sesión.
- Panel de inicio autenticado con cifras reales de clientes, citas del día y servicios, además de últimos clientes y próximas citas.
- Consulta, creación, edición y eliminación de clientes con acceso autenticado.
- Búsqueda de clientes por nombre, apellido, correo o teléfono.
- Interfaz adaptable a distintas pantallas, con CSS local y una paleta de azules (#748cab, #3e5c76 y #1d2d44).
- Validación de campos obligatorios y correo electrónico.
- Administración de clientes, empleados, servicios, estados y citas desde `/admin/`.
- 10 pruebas automatizadas de autenticación, CRUD, validaciones, privacidad del panel y búsqueda.

Las citas, empleados, servicios y estados se gestionan desde el administrador de Django. La agenda pública y la prevención de cruces de horario son mejoras futuras.

## Arquitectura MVT
- Modelos: `citas/models.py` define las entidades y sus relaciones.
- Vistas: `citas/views.py` procesa las solicitudes y los formularios.
- Plantillas: `citas/templates/citas/` contiene la interfaz.
- Estilos locales: `citas/static/citas/css/app.css` define el diseño visual.
- Rutas: `citas/urls.py` y `proyecto/urls.py` conectan las páginas.
- Formularios: `citas/forms.py` valida la entrada de clientes.
- Migraciones: `citas/migrations/` permite crear las tablas.

## Instalación en Windows (PowerShell)
Entorno del proyecto original: Python 3.14. Las versiones de `requirements.txt` corresponden a sus paquetes instalados.

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Iniciar MySQL/MariaDB y crear una base de datos vacía desde su consola:

```sql
CREATE DATABASE sistema_gestion_citas CHARACTER SET utf8mb4;
```

Configurar las credenciales en la misma ventana de PowerShell. Sustituir los valores por los del equipo:

```powershell
$env:DB_NAME = 'sistema_gestion_citas'
$env:DB_USER = 'root'
$env:DB_PASSWORD = 'tu_contrasena_local'
$env:DJANGO_SECRET_KEY = 'tu_clave_local_larga_y_aleatoria'
.\.venv\Scripts\python.exe manage.py migrate
.\.venv\Scripts\python.exe manage.py createsuperuser
.\.venv\Scripts\python.exe manage.py runserver
```

Abrir http://127.0.0.1:8000/ y registrar un usuario. Para el administrador, abrir http://127.0.0.1:8000/admin/ con el superusuario creado.

Si la cuenta local de MySQL no tiene contraseña, establecer `DB_PASSWORD` en una cadena vacía. `DB_HOST` y `DB_PORT` son opcionales y predeterminan `localhost` y `3306`. Las variables deben establecerse de nuevo al abrir otra terminal. No se carga automáticamente un archivo `.env`.

Estos pasos de migración son para una base de datos nueva; no deben aplicarse a ciegas sobre tablas preexistentes. La configuración incluida es para demostración local, con `DEBUG=True`. No es una configuración de producción. Si se omite `DJANGO_SECRET_KEY`, se genera una clave temporal: las sesiones se invalidan al reiniciar.

## Verificación
```powershell
.\.venv\Scripts\python.exe manage.py check
.\.venv\Scripts\python.exe manage.py test citas
```
Las pruebas necesitan permisos para crear y eliminar la base temporal `test_sistema_gestion_citas`. No usan los registros de la base habitual.

## Demostración en el aula
1. Iniciar el servidor de base de datos y el servidor Django.
2. Iniciar sesión y explicar los datos del panel de inicio.
3. Abrir Clientes y mostrar la búsqueda.
4. Crear un cliente de prueba, consultarlo y editarlo.
5. Mostrar el rechazo de un correo inválido o un nombre vacío.
6. Eliminar el cliente de prueba y cerrar sesión.
7. Explicar los modelos relacionados y mostrar la administración de citas, si se solicita.

## Entrega
Repositorio: https://github.com/AnaEsther01/sistema-gestion-citas

La copia para el repositorio excluye entornos virtuales, bases locales y archivos temporales. Las credenciales se configuran en el equipo, no en GitHub.
