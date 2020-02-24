from django.conf.urls import url

from . import views

app_name = 'testApp'
urlpatterns = [

    # Test views
    url(r'^$', views.AnimalListView.as_view(), name='animal_list'),
    url(r'^create/$', views.AnimalCreateView.as_view(), name='animal_form'),

]
