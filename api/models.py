from django.db import models
from django.contrib.auth.models import User

class Status(models.Model):
    idStatus = models.AutoField(primary_key=True,db_column='idStatus')
    Status = models.CharField(max_length=15,default='Status',db_column='Status')
    class Meta:
        db_table='Status'

class Prioridad(models.Model):
    idPrioridad = models.AutoField(primary_key=True,db_column='idPrioridad')
    Prioridad = models.CharField(max_length=25,default='Prioridad',db_column='Prioridad')
    class Meta:
        db_table='Prioridad'

class Tareas(models.Model):
    idTarea = models.AutoField(primary_key=True,db_column='idTarea')
    Titulo = models.CharField(max_length=50,default='Titulo',db_column='Titulo')
    Descripcion = models.CharField(max_length=200,default='Descripcion',db_column='Descripcion')
    Fecha_inicio = models.DateTimeField(default='2000-01-01 12:00',db_column='Fecha_creacion')
    Fecha_termino = models.DateTimeField(default='2000-01-01 12:00',db_column='Fecha_vencimiento')
    fk_Status = models.ForeignKey(Status,on_delete=models.CASCADE,db_column='fk_Status')
    fk_Prioridad = models.ForeignKey(Prioridad,on_delete=models.CASCADE,db_column='fk_Prioridad')
    fk_Usuario = models.ForeignKey(User,on_delete=models.CASCADE,db_column='fk_Usuario')
    class Meta:
        db_table='Tareas'

class Lista_tareas(models.Model):
    idLista = models.AutoField(primary_key=True,db_column='idLista')
    Nombre = models.CharField(max_length=45,default='Nombre',db_column='Nombre')
    Descripcion = models.CharField(max_length=200,default='Descripcion',db_column='Descripcion')
    fk_Usuario = models.ForeignKey(User,on_delete=models.CASCADE,db_column='fk_Usuario')
    class Meta:
        db_table='Lista_tareas'

class Listas_has_tareas(models.Model):
    idListas_has_tareas = models.AutoField(primary_key=True,default=1,db_column='idListas_has_tareas')
    fk_Lista = models.ForeignKey(Lista_tareas,on_delete=models.CASCADE,db_column='fk_Lista')
    fk_Tarea = models.ForeignKey(Tareas,on_delete=models.CASCADE,db_column='fk_Tarea')
    class Meta:
        db_table='Listas_has_tareas'

class Etiquetas(models.Model):
    idEtiqueta = models.AutoField(primary_key=True,db_column='idEtiqueta')
    Nombre = models.CharField(max_length=20,default='Nombre',db_column='Nombre')
    Descripcion = models.CharField(max_length=100,default='Descripcion',db_column='Descripcion')
    class Meta:
        db_table='Etiquetas'

class Tareas_has_etiquetas(models.Model):
    idTareas_has_etiquetas = models.AutoField(primary_key=True,default=1,db_column='idTareas_has_etiquetas')
    fk_Tarea = models.ForeignKey(Tareas,on_delete=models.CASCADE,db_column='fk_Tarea')
    fk_Etiqueta = models.ForeignKey(Etiquetas,on_delete=models.CASCADE,db_column='fk_Etiqueta')
    class Meta:
        db_table='Tareas_has_etiquetas'
        
class Encuesta_calidad(models.Model):
    Marca_temporal = models.TextField(max_length=200, default='Marca temporal', db_column='Marca temporal')
    Pregunta1 = models.TextField(max_length=200, default='pregunta1', db_column='Satisfaccion de usabilidad')
    Pregunta2 = models.TextField(max_length=200, default='pregunta2', db_column='Frecuencia de uso')
    Pregunta3 = models.TextField(max_length=200, default='pregunta3', db_column='Caracteristica mas util')
    Pregunta4 = models.TextField(max_length=200, default='pregunta4', db_column='Caracteristica a mejorar')
    Pregunta5 = models.TextField(max_length=200, default='pregunta5', db_column='La recomendarias')
    Pregunta6 = models.TextField(max_length=200, default='pregunta6', db_column='Velocidad y rendimiento')
    Pregunta7 = models.TextField(max_length=200, default='pregunta7', db_column='Servicio de FAQ')
    class Meta:
        db_table='Encuesta_calidad'
