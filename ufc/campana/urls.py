from django.conf.urls import url
from . import views

app_name = 'campana'
urlpatterns = [
    url(r'^genres/$', views.show_genres, name='show'),
    url(r'^categoria/add/$', views.categoria_add, name='add'),
    url(r'^usuario/validar/$', views.ws_usuario_validar, name='usuario_validar'),
    url(r'^usuario/add/$', views.ws_usuario_add, name='usuario_add'),
    url(r'^cliente/add/$', views.cliente_add, name='cliente_add'),
    url(r'^persona/add/$', views.persona_add, name='persona_add'),
]
