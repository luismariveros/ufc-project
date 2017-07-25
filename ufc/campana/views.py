# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.core import serializers
from django.http import JsonResponse
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import UserCreationForm
import json

from .models import *
from .forms import *

from mptt.exceptions import InvalidMove
from mptt.forms import MoveNodeForm


def show_genres(request):
    ctx = {'nodes': Persona.objects.all()}
    return render(request, 'campana/genres.html', ctx)


@login_required()
def persona_add(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        form = PersonaForm(request.user, request.POST)
        if form.is_valid():
            persona = form.save(commit=False)
            persona.usuario = User.objects.get(username=username)
            persona.save()
            return HttpResponseRedirect(reverse('campana:show'))
    else:
        form = PersonaForm(request.user)
        form_user = UsuarioCrearForm()

        #print request.user.groups.all()
        print Persona.objects.filter(usuario__groups__in=request.user.groups.all())
    ctx = {'form': form, 'form_user': form_user}
    return render(request, 'campana/cliente_add.html', ctx)


def categoria_add(request):
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('campana:show'))
        else:
            form = CategoriaForm(request.POST)
            ctx = {'form': form}
            return render(request, 'campana/categoria_add.html', ctx)
    else:
        form = CategoriaForm
    ctx = {'form': form}
    return render(request, 'campana/categoria_add.html', ctx)


def ws_usuario_validar(request):
    username = request.GET.get('username', None)
    data = {
        'is_taken': User.objects.filter(username__iexact=username).exists()
    }
    if data['is_taken']:
        data['error_message'] = 'Ya existe un usuario registrado con ese email.'

    print data
    return JsonResponse(data)


def ws_usuario_add(request):
    if request.method == 'POST' and request.is_ajax():
        form = UsuarioCrearForm(request.POST)
        if form.is_valid():
            grupo = request.user.groups.all()[0]  # Obtener el grupo  del usuario autenticado
            usuario = form.save()
            usuario.groups.add(grupo)
            usuario.save()

            d = serializers.serialize('json', User.objects.filter(username=usuario.username), fields=('pk', 'username'))

            print  d
            #return JsonResponse({'user_id': usuario.id}, safe=False)
            return JsonResponse(d, safe=False)


def cliente_add(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('campana:show'))
    else:
        a = Cliente.objects.get(user_id=User.objects.get(username='diego@gmail.com').id)
        #a = Cliente.objects.get(user_id=User.objects.get(username='test').id)

        form = ClienteForm(instance=a)
        form_user = UsuarioCrearForm()

        #print form.__dict__
    ctx = {'form': form, 'form_user': form_user}
    return render(request, 'campana/cliente_add.html', ctx)

