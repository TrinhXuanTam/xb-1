from django.conf.urls import url

from . import views

app_name = 'core'
urlpatterns = [
    url(r'^switch-language/$', views.SwitchLanguageRedirectView.as_view(), name='switch_language'),
]
