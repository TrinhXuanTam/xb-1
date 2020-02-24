from django.contrib import admin
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^admin/', admin.site.urls, name='admin'),

    url(r'^$', views.IndexView.as_view(), name='index'),
]
