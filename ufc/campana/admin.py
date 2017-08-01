# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from treebeard.admin import TreeAdmin
from treebeard.forms import movenodeform_factory
from mptt.admin import DraggableMPTTAdmin
from .models import *


class CategoriaAdmin(TreeAdmin):
    form = movenodeform_factory(Categoria)


class ClienteAdmin(TreeAdmin):
    form = movenodeform_factory(Cliente)


admin.site.register(Categoria, CategoriaAdmin)
admin.site.register(Cliente, ClienteAdmin)
admin.site.register(Candidato)
admin.site.register(Votante)
admin.site.register(
    Persona,
    DraggableMPTTAdmin,
    list_display=(
        'tree_actions',
        'indented_title',
        # ...more fields if you feel like it...
    ),
    list_display_links=(
        'indented_title',
    ),
)