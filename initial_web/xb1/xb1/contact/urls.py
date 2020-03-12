from django.conf.urls import url, include

from . import views

app_name = "contact"
urlpatterns = [
    url(r"^form/", views.ContactFormView.as_view(), name="form"),
]
