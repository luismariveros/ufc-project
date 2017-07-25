from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import password_change, password_change_done
from . import views

app_name = 'visita'
urlpatterns = [
    url(r'^visita/$', login_required(views.VisitaLista.as_view()), name='lista'),
    #url(r'^visita/agregar/$', login_required(views.VisitaAgregar.as_view()), name='agregar'),
    url(r'^visita/agregar/$', login_required(views.visita_agregar), name='agregar'),
]
