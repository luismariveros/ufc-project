from django import forms
from .models import *


class VisitaAgregarForm(forms.ModelForm):

    class Meta:
        model = Visita
        fields = ('cedula', 'celular', 'partido', 'actividad')