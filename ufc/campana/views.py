# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, HttpResponseRedirect, get_list_or_404, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.core.urlresolvers import reverse
from django.core import serializers
from django.urls import reverse_lazy
from django.http import JsonResponse, Http404
from django.contrib import messages
from django.views.generic.edit import DeleteView
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Permission

from .models import *
from .forms import *
from .decorators import user_is_descendants
from padron.models import Individuo as PadronIndividuo
from padron.forms import PersonaPadronForm

from mptt.exceptions import InvalidMove
from mptt.forms import MoveNodeForm


@login_required()
def persona_list(request):
    try:
        personas = Persona.objects.get(usuario=request.user).get_descendants(include_self=True)
    except ObjectDoesNotExist:
        personas = None
    ctx = {'personas': personas}
    return render(request, 'campana/persona_list.html', ctx)


@login_required()
def votante_list(request):
    persona = get_object_or_404(Persona, usuario__username=request.user)
    votantes = Votante.objects.filter(persona=persona).values('cedula')
    individuos = PadronIndividuo.objects.filter(cedula__in=votantes)
    ctx = {'persona': persona, 'object_list': votantes}
    return render(request, 'campana/votante_list.html', ctx)


@login_required()
def votante_add(request):
    if request.method == 'POST':
        form = VotanteForm(request.POST)
        if form.is_valid():
            cedula = form.cleaned_data.get('cedula')
            persona = Persona.objects.get(usuario=request.user)
            descendientes = persona.get_root().get_descendants()  # Todos los descendientes del Candidato
            if Votante.objects.filter(persona__in=descendientes, cedula=cedula).exists():
                messages.error(request, 'Votante ya agregado por otra Persona.')
                form = VotanteForm(request.POST)
                form_user = PersonaPadronForm(auto_id="padron_%s")
                ctx = {'form': form, 'form_user': form_user}
                return render(request, 'campana/votante_add.html', ctx)
            else:
                candidato = Candidato.objects.get(usuario__persona=persona.get_root())
                votante = form.save(commit=False)
                votante.persona = persona
                votante.candidato = candidato
                votante.eleccion = candidato.eleccion
                votante.save()

                messages.success(request, 'Votante agregado correctamente.')
                if '_addanother' in request.POST:
                    return HttpResponseRedirect(reverse('campana:votante_add'))
                return HttpResponseRedirect(reverse('campana:votante_list'))
    else:
        form = VotanteForm()
        form_user = PersonaPadronForm(auto_id="padron_%s")
        ctx = {'form': form, 'form_user': form_user}
    return render(request, 'campana/votante_add.html', ctx)


@login_required()
@permission_required('campana.add_persona', raise_exception=True)
def persona_add(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        form_persona = PersonaForm(request.user, request.POST)

        if form_persona.is_valid():
            padre = form_persona.cleaned_data.get('parent')
            persona = Persona.objects.get(usuario__username=username)
            persona.parent = padre

            if 'grupo' in request.POST:
                grupos = request.POST.getlist('grupo')
                for g in grupos:
                    grupo = Group.objects.get(id=g)
                    persona.usuario.groups.add(grupo)
            persona.save()

            messages.success(request, 'Persona agregada correctamente.')
            if '_addanother' in request.POST:
                return HttpResponseRedirect(reverse('campana:persona_add'))
            return HttpResponseRedirect(reverse('campana:persona_list'))
    else:
        form_persona = PersonaForm(request.user)
        form_user = UsuarioCrearForm()
        ctx = {'form': form_persona, 'form_user': form_user}
        if bool(request.user.groups.filter(name__contains='-')) or request.user.is_superuser:
            form_grupo = GrupoForm(request.user)
            ctx.update({'form_grupo': form_grupo})
    return render(request, 'campana/persona_add.html', ctx)


@login_required()
@permission_required('campana.add_persona', raise_exception=True)
@user_is_descendants
def persona_edit(request, user_id):
    persona = get_object_or_404(Persona, usuario_id=user_id)

    if request.method == 'POST':
        form_persona = PersonaForm(request.user, request.POST)
        form_user = UsuarioEditarForm(request.POST, instance=persona.usuario)

        if form_persona.is_valid() and form_user.is_valid():
            persona.parent = form_persona.cleaned_data.get('parent')

            if 'grupo' in request.POST:
                persona.usuario.groups.clear()  # Borro los grupos del usuario
                grupo = request.user.groups.exclude(name__contains='-').first()  # Obtener el grupo basico del usuario
                persona.usuario.groups.add(grupo)
                grupos = request.POST.getlist('grupo')
                for g in grupos:
                    grupo = Group.objects.get(id=g)
                    persona.usuario.groups.add(grupo)
            else:
                grupos = persona.usuario.groups.filter(name__contains='-')
                for g in grupos:
                    persona.usuario.groups.remove(g)  # Elimino todos los grupos menos el basico (SP)
            persona.save()
            form_user.save()

            messages.success(request, 'Persona editada correctamente.')
            return HttpResponseRedirect(reverse('campana:persona_list'))
    else:
        form_persona = PersonaForm(request.user, instance=persona)
        form_user = UsuarioEditarForm(instance=persona.usuario)

    ctx = {'form': form_persona, 'form_user': form_user}
    if bool(request.user.groups.filter(name__contains='-')) or request.user.is_superuser:
        form_grupo = GrupoForm(request.user, initial={'grupo': persona.usuario.groups.all()})
        ctx.update({'form_grupo': form_grupo})
    return render(request, 'campana/persona_edit.html', ctx)


class PersonaDelete(DeleteView):
    model = Persona
    pk_url_kwarg = 'user_id'
    template_name = 'campana/persona_confirm_delete.html'
    success_url = reverse_lazy('persona_list')

    def get_object(self, queryset=None):
        usuario_id = self.kwargs['user_id']
        queryset = Persona.objects.get(usuario_id=usuario_id)

        if not queryset:
            raise Http404

        ctx = {'persona': queryset, 'descendientes': queryset.get_descendants()}
        return ctx

    def delete(self, request, *args, **kwargs):
        usuario_id = self.kwargs['user_id']
        descendientes = Persona.objects.get(usuario_id=usuario_id).get_descendants(include_self=True).values('usuario_id')
        User.objects.filter(pk__in=descendientes).delete()
        messages.success(request, 'Persona borrada correctamente.')
        return HttpResponseRedirect(reverse('campana:persona_list'))


def ws_usuario_validar(request):
    username = request.GET.get('username', None)
    data = {
        'is_taken': User.objects.filter(username__iexact=username).exists()
    }
    if data['is_taken']:
        data['error_message'] = 'Ya existe un usuario registrado con ese email.'
    return JsonResponse(data)


def ws_usuario_add(request):
    if request.method == 'POST' and request.is_ajax():
        form = UsuarioCrearForm(request.POST)
        if form.is_valid():
            grupo = request.user.groups.exclude(name__contains='-').first()  # Obtener el grupo del usuario autenticado
            usuario = form.save()
            usuario.groups.add(grupo)
            usuario.email = usuario.username
            usuario.save()

            padre = Persona.objects.get(usuario=request.user)
            persona = Persona(usuario=usuario, parent=padre)
            persona.save()

            data = serializers.serialize('json',
                                         User.objects.filter(username=usuario.username),
                                         fields=('pk', 'username')
                                         )
            return JsonResponse(data, safe=False)
        else:
            print form.errors
