from django.contrib import admin
from .models import Cliente, Empleado, Servicio, EstadoCita, Cita


admin.site.register(Cliente)
admin.site.register(Empleado)
admin.site.register(Servicio)
admin.site.register(EstadoCita)
admin.site.register(Cita)