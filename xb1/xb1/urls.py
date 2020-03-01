from django.contrib import admin
from django.conf.urls import url, include

from . import views

urlpatterns = [

    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^admin/', admin.site.urls, name='admin'),

    url(r"^testapp/", include("xb1.testApp.urls")),

]
