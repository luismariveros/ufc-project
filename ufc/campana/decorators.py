from django.core.exceptions import PermissionDenied
from .models import Persona


def user_is_descendants(function):
    def wrap(request, *args, **kwargs):
        descendientes = Persona.objects.get(usuario=request.user).get_descendants(include_self=True)
        if descendientes.filter(usuario_id=kwargs['user_id']).exists():
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap
