from django.conf.urls import url
from . import views

app_name = 'padron'
urlpatterns = [
    #url(r'^$', views.IndividuoLista.as_view(), name='persona'),
    url(r'^(?P<cedula>[0-9]+)/$', views.IndividuoDetalle.as_view(), name='cedula'),
    url(r'^departamento/$', views.DepartamentoLista.as_view(), name='departamento'),
    url(r'^departamento/(?P<codigo>[0-9]+)/$', views.PadronDepartamento.as_view(), name='padrondepto'),
    #url(r'^visita/agregar/$', login_required(views.VisitaAgregar.as_view()), name='agregar'),
]
