# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import *


class DepartamentoAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'nombre')

# Register your models here.
admin.site.register(Individuo)
admin.site.register(Departamento, DepartamentoAdmin)