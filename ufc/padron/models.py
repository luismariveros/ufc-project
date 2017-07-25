# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class Departamento(models.Model):
    nombre = models.CharField(max_length=100)
    codigo = models.IntegerField()

    def __unicode__(self):
        return self.nombre

    class Meta:
        ordering = ['codigo']


class Districto(models.Model):
    nombre = models.CharField(max_length=100)
    codigo = models.IntegerField()

    def __unicode__(self):
        return self.nombre


class Seccional(models.Model):
    nombre = models.CharField(max_length=100)
    codigo = models.IntegerField()

    def __unicode__(self):
        return "%s-%s" % (self.numero, self.nombre)


class Individuo(models.Model):
    cedula = models.IntegerField(db_index=True)
    nombre = models.CharField(max_length=200)
    #apellido = models.CharField(max_length=200, blank=True)
    #fecha_nacimiento = models.DateField()
    #sexo = models.CharField(max_length=5, blank=True)
    departamento = models.ForeignKey(Departamento)

    def __unicode__(self):
        return self.nombre
