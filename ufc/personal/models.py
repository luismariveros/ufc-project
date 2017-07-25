# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class Persona(models.Model):
    cedula = models.IntegerField(db_index=True)
    nombre = models.CharField(max_length=200, blank=True)
    apellido = models.CharField(max_length=200, blank=True)
    nacimiento_fecha = models.DateField(null=True, blank=True)
    estado_civil = models.CharField(max_length=10)
    #nacimiento_lugar = models.CharField(max_length=200)
    #nacionalidad = models.CharField(max_length=200)
    #profesion = models.CharField(max_length=200)
    #domicilio = models.CharField(max_length=400)
    #barrio_ciudad = models.CharField(max_length=200)
    #conyuge_cedula = models.IntegerField(db_index=True)
    #sexo = models.CharField(max_length=5)

    def __unicode__(self):
        return self.nombre
