# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from django.views.generic.edit import CreateView

from .models import *
from .forms import *
from padron.forms import *


class VisitaAgregar(CreateView):
    model = Visita
    fields = ['cedula', 'celular', 'partido', 'actividad']


class VisitaLista(ListView):
    model = Visita


def visita_agregar(request):
    if request.method == 'POST':
        pass
    else:
        form = VisitaAgregarForm()
        form_padron = PersonaPadronForm(prefix='padron')
    ctx = {'form': form, 'form_padron': form_padron}
    return render(request, 'visita/visita_form.html', ctx)
