from django import forms
from .models import *


class PersonaPadronForm(forms.ModelForm):

    class Meta:
        model = Individuo
        fields = ('cedula', 'nombre')

    def __init__(self, *args, **kwargs):
        super(PersonaPadronForm, self).__init__(*args, **kwargs)
        for f in self.fields:
            self.fields[f].widget.attrs['disabled'] = 'disabled'
