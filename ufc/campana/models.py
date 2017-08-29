# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from mptt.models import MPTTModel, TreeForeignKey
from treebeard.mp_tree import MP_Node
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
    usuario = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', db_index=True)

    def __unicode__(self):
        return self.usuario.get_full_name() if self.usuario else 'Sin Usuario'


class Votante(models.Model):
    cedula = models.IntegerField(db_index=True)
    persona = models.ForeignKey(Persona, null=True, on_delete=models.CASCADE)
    candidato = models.ForeignKey(Candidato, null=True)
    eleccion = models.ForeignKey(Eleccion, null=True)
    fecha = models.DateField(default=now)

    def __unicode__(self):
        return "%s-%s" % (self.candidato, self.cedula)


class Categoria(MP_Node):
    nombre = models.CharField(max_length=50)

    node_order_by = ['nombre']

    def __unicode__(self):
        return 'Categoria: %s' % self.nombre


class Cliente(MP_Node):
    user_id = models.BigIntegerField(db_index=True)
    permiso = models.BooleanField(default=False, help_text="El Usuario podra revisar toda la estructura?")

    node_order_by = ['user_id']

    def __unicode__(self):
        return User.objects.get(id=self.user_id).get_full_name() if self.user_id else 'Sin Usuario'

