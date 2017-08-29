from django import forms
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from treebeard.forms import *
from mptt.forms import *

from .models import *
from django.contrib.auth.models import Group


#CategoriaForm = movenodeform_factory(Categoria)

class CategoriaForm(MoveNodeForm):
    class Meta:
        model = Categoria
        exclude = ('sib_order', 'parent')


class ClienteForm(MoveNodeForm):

    class Meta:
        model = Cliente
        fields = ('user_id', 'permiso', '_position', '_ref_node_id')
        widgets = {
            'user_id': forms.HiddenInput()
        }


class PersonaForm(forms.ModelForm):

    class Meta:
        model = Persona
        fields = ('parent', )
        labels = {
            'parent': 'Depende de:'
        }

    def __init__(self, user, *args, **kwargs):
        try:
            persona = Persona.objects.get(usuario__username=user)
            super(PersonaForm, self).__init__(*args, **kwargs)
            if bool(user.groups.filter(name__contains='ADMIN')) or user.is_superuser:
                queryset = Persona.objects.filter(pk__in=persona.get_root().get_descendants(include_self=True))
            else:
                queryset = Persona.objects.filter(pk__in=persona.get_descendants(include_self=True))
            self.fields['parent'].queryset = queryset
        except ObjectDoesNotExist:
            super(PersonaForm, self).__init__(*args, **kwargs)


class VotanteForm(forms.ModelForm):

    class Meta:
        model = Votante
        fields = ('cedula', )


class PermisoForm(forms.Form):
    choices = (
        ('COLAB', 'Colaborador'),
    )
    permiso = forms.MultipleChoiceField(choices=choices)

    def __init__(self, user,  *args, **kwargs):
        super(PermisoForm, self).__init__(*args, **kwargs)
        if user.groups.filter(name__contains='ADMIN') or user.is_superuser:
            choices = self.fields['permiso'].choices
            choices.append(('ADMIN', 'Administrador'),)
            self.fields['permiso'].choices = choices


class GrupoForm(forms.ModelForm):
    grupo = forms.ModelMultipleChoiceField(queryset=None, required=False)

    class Meta:
        model = Group
        fields = ('grupo', )

    def __init__(self, user, *args, **kwargs):
        super(GrupoForm, self).__init__(*args, **kwargs)
        #self.fields['grupos'].queryset = Group.objects.all()
        #self.fields['grupos'].initial = (('4', 'SP-COLAB'),)
        self.fields['grupo'].queryset = Group.objects.filter(user=user, name__contains='-').order_by('name')
        #if user.groups.filter(name__contains='ADMIN') or user.is_superuser:
            #choices = self.fields['permiso'].choices
            #choices.append(('ADMIN', 'Administrador'), )

        #else:
        #    self.fields['grupos'].queryset = Group.objects.filter(user=user)


class UsuarioCrearForm(UserCreationForm):
    first_name = forms.CharField(max_length=100, label="Nombre")
    last_name = forms.CharField(max_length=100, label="Apellido")

    def __init__(self, *args, **kwargs):
        super(UsuarioCrearForm, self).__init__(*args, **kwargs)
        self.fields['username'].help_text = None

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'password1', 'password2')
        labels = {'username': "Email"}

    def save(self, commit=True):
        user = super(UsuarioCrearForm, self).save(commit=False)
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        if commit:
            user.save()
        return user


class UsuarioEditarForm(forms.ModelForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')

    def __init__(self, *args, **kwargs):
        super(UsuarioEditarForm, self).__init__(*args, **kwargs)
        self.fields['username'].help_text = None
        self.fields['username'].widget.attrs['readonly'] = True
