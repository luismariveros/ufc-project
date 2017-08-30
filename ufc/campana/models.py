# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from mptt.models import MPTTModel, TreeForeignKey
from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now


class Partido(models.Model):
    nombre = models.CharField(max_length=100)
    codigo = models.CharField(max_length=10)

    def __unicode__(self):
        return self.codigo


class Eleccion(models.Model):
    TIPO_ELECCION = (
        ('GRAL', 'Generales'),
        ('INT', 'Internas')
    )
    nombre = models.CharField(max_length=200)
    tipo = models.CharField(max_length=20, choices=TIPO_ELECCION)
    partido = models.ForeignKey(Partido, null=True)

    def __unicode__(self):
        return self.nombre


class Candidato(models.Model):
    usuario = models.ForeignKey(User)
    codigo = models.CharField(max_length=20)
    partido = models.ForeignKey(Partido)
    eleccion = models.ForeignKey(Eleccion)

    def __unicode__(self):
        return self.usuario.get_full_name()


class Persona(MPTTModel):
    usuario = models.ForeignKey(User)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', db_index=True)

    def __unicode__(self):
        return self.usuario.get_full_name() if self.usuario else 'Sin Usuario'

    def get_votante_count(self):
        return self.votante_set.all().count()



class Votante(models.Model):
    cedula = models.IntegerField(db_index=True)
    persona = models.ForeignKey(Persona, null=True, on_delete=models.CASCADE)
    candidato = models.ForeignKey(Candidato, null=True)
    eleccion = models.ForeignKey(Eleccion, null=True)
    fecha = models.DateField(default=now)

    def __unicode__(self):
        return "%s-%s" % (self.candidato, self.cedula)

