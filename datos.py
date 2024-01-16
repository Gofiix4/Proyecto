import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "PROYECTO.settings")
django.setup()
from api.models import *
datosStatus = [
    {'Status': 'Activo'},
    {'Status': 'Pendiente'},
    {'Status': 'Completada'},
    {'Status': 'Vencida'},
    {'Status': 'Cancelada'},
]
datosPrioridad = [
    {'Prioridad': 'Baja'},
    {'Prioridad': 'Media'},
    {'Prioridad': 'Alta'},
    {'Prioridad': 'Urgente'},
    {'Prioridad': 'Critica'},
    {'Prioridad': 'Inmediata'},
    {'Prioridad': 'Sin prioridad'},
]
for datoStatus in datosStatus:
    createStatus = Status(**datoStatus)
    createStatus.save()
print("Status insertados correctamente.")
for datoPrioridad in datosPrioridad:
    createPrioridad = Prioridad(**datoPrioridad)
    createPrioridad.save()
print("Prioridad insertados correctamente.")

