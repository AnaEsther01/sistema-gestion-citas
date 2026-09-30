# Sistema de gestión de citas

Proyecto académico desarrollado con Python y Django. Base de datos configurada: MySQL/MariaDB.

## Funciones implementadas
- Registro, inicio y cierre de sesión.
- Consulta, creación, edición y eliminación de clientes con acceso autenticado.
- Validación de campos obligatorios y correo electrónico.
- Administración de clientes, empleados, servicios, estados y citas desde `/admin/`.
- Pruebas automatizadas de autenticación, CRUD y validaciones.

## Arquitectura MVT
- Modelos: `citas/models.py` define las entidades y sus relaciones.
- Vistas: `citas/views.py` procesa las solicitudes y los formularios.
- Plantillas: `citas/templates/citas/` contiene la interfaz.
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
2. Iniciar sesión y abrir Clientes.
3. Crear un cliente de prueba, consultarlo y editarlo.
4. Mostrar el rechazo de un correo inválido o un nombre vacío.
5. Eliminar el cliente de prueba y cerrar sesión.
6. Explicar los modelos relacionados y mostrar su administración, si se solicita.

## Entrega
Repositorio: https://github.com/AnaEsther01/sistema-gestion-citas

La copia para el repositorio excluye entornos virtuales, bases locales y archivos temporales. Las credenciales se configuran en el equipo, no en GitHub.
