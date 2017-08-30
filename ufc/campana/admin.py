# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin
from .models import *


admin.site.register(Candidato)
admin.site.register(Votante)
admin.site.register(Eleccion)
admin.site.register(Partido)
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