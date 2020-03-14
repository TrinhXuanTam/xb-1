from django.conf.urls import url

from . import views

app_name = 'articles'
urlpatterns = [

    # Test views
    url(r'^$', views.AnimalListView.as_view(), name='animal_list'),
    url(r'^create/$', views.AnimalCreateView.as_view(), name='animal_form'),

]
