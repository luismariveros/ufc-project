from django import forms
from django.contrib.auth.forms import UserCreationForm
from treebeard.forms import *
from mptt.forms import *

from .models import *


#CategoriaForm = movenodeform_factory(Categoria)

class CategoriaForm(MoveNodeForm):
    class Meta:
        model = Categoria
        exclude = ('sib_order', 'parent')


#ClienteForm = movenodeform_factory(Cliente)
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
        fields = ('permiso', 'parent')

    def __init__(self, user, *args, **kwargs):
        p = Persona.objects.get(usuario__username=user)
        print p.get_descendants(include_self=True)
        super(PersonaForm, self).__init__(*args, **kwargs)
        #print Persona.objects.filter(usuario__groups__in=user.groups.object.all())
        self.fields['parent'].queryset = Persona.objects.filter(pk__in=p.get_descendants(include_self=True))


class UsuarioCrearForm(UserCreationForm):
    nombre = forms.CharField(max_length=100)
    apellido = forms.CharField(max_length=100)

    def __init__(self, *args, **kwargs):
        super(UsuarioCrearForm, self).__init__(*args, **kwargs)
        self.fields['username'].help_text = None

    class Meta:
        model = User
        fields = ("nombre", "apellido", "username", "password1", "password2")
        labels = {"username": "Email"}
        help_text = {"username": ""}

    def save(self, commit=True):
        user = super(UsuarioCrearForm, self).save(commit=False)
        user.first_name = self.cleaned_data["nombre"]
        user.last_name = self.cleaned_data["apellido"]
        if commit:
            user.save()
        return user
