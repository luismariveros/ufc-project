# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models


class Nacionalidad(models.Model):
    nombre = models.CharField(max_length=200)
    codigo = models.CharField(max_length=10)


class Persona(models.Model):
    cedula = models.IntegerField(db_index=True)
    nombre = models.CharField(max_length=200, blank=True)
    apellido = models.CharField(max_length=200, blank=True)
    nacimiento_fecha = models.DateField(null=True, blank=True)
    estado_civil = models.CharField(max_length=10, blank=True)
    nacimiento_lugar = models.CharField(max_length=200, blank=True)
    nacionalidad = models.ForeignKey(Nacionalidad, null=True)
    profesion = models.CharField(max_length=200)
    domicilio = models.CharField(max_length=500, null=True)
    barrio_ciudad = models.CharField(max_length=200)
    conyuge_cedula = models.ForeignKey('self', on_delete=models.CASCADE)
    sexo = models.CharField(max_length=5)

    def __unicode__(self):
        return "%s-%s %s" % (self.cedula, self.nombre, self.apellido)
