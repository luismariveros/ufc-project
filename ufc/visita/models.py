# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.urls import reverse
from datetime import date


class Partido(models.Model):
    nombre = models.CharField(max_length=100)
    codigo = models.CharField(max_length=10)

    def __unicode__(self):
        return self.codigo


class ActividadProductiva(models.Model):
    descripcion = models.CharField(max_length=100)

    def __unicode__(self):
        return self.descripcion


class Visita(models.Model):
    cedula = models.CharField(max_length=15)
    celular = models.CharField(max_length=20, blank=True)
    nombre = models.CharField(max_length=200)
    votante_asociado = models.IntegerField(default=0)
    fecha_visita = models.DateField(default=date.today)
    partido = models.ManyToManyField('Partido')
    oficialista = models.BooleanField(default=False)
    actividad = models.ForeignKey('ActividadProductiva')

    def get_absolute_url(self):
        return reverse('visita:agregar')
