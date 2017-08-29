from .models import Persona
from django.core.exceptions import ObjectDoesNotExist


def my_processor(request):
    if request.user.is_authenticated():
        try:
            ancentros = Persona.objects.get(usuario=request.user).get_ancestors(ascending=True)
            padre = ancentros[0]
            candidato = ancentros.last()
        except (IndexError, ObjectDoesNotExist):
            padre = candidato = None

        context = {
            'padre': padre,
            'candidato': candidato
        }
    else:
        context = {
            'padre': None,
            'candidato': None
        }
    return context

