from django.conf.urls import url
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required


from . import views

app_name = 'campana'
urlpatterns = [
    url(r'^$', login_required(TemplateView.as_view(template_name="campana/index.html")), name='index'),
    url(r'^usuario/validar/$', views.ws_usuario_validar, name='usuario_validate'),
    url(r'^usuario/add/$', views.ws_usuario_add, name='usuario_add'),
    url(r'^persona/$', views.persona_list, name='persona_list'),
    url(r'^persona/(?P<user_id>[0-9]+)/$', views.persona_edit, name='persona_edit'),
    url(r'^persona/(?P<user_id>[0-9]+)/delete/$', views.PersonaDelete.as_view(), name='persona_delete'),
    url(r'^persona/add/$', views.persona_add, name='persona_add'),
    url(r'^votante/$', views.votante_list, name='votante_list'),
    url(r'^votante/add/$', views.votante_add, name='votante_add'),
]
