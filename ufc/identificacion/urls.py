from django.conf.urls import url
from . import views

app_name = 'identificacion'
urlpatterns = [
    url(r'^persona/$', views.PersonaLista.as_view(), name='persona'),
    url(r'^persona/(?P<cedula>[0-9]+)/$', views.PersonaDetalle.as_view(), name='cedula'),
    #url(r'^visita/agregar/$', login_required(views.VisitaAgregar.as_view()), name='agregar'),
]
