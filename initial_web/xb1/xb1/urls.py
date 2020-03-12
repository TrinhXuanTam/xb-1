from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include

from . import views

urlpatterns = [
    path('admin/', admin.site.urls),

    url(r'^$', views.IndexView.as_view(), name="index"),
    url(r"^contact/", include("xb1.contact.urls")),
]
