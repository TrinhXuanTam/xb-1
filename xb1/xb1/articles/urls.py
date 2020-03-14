from django.conf.urls import url

from . import views

app_name = 'articles'
urlpatterns = [

    # Test views
    url(r'^animals/$', views.AnimalListView.as_view(), name="animal_list"),
    url(r'^animals/create/$', views.AnimalCreateView.as_view(), name="animal_form"),

    # Articles
    url(r'^$', views.ArticleListView.as_view(), name="article_list"),
    url(r'^create/$', views.ArticleCreateView.as_view(), name="article_create"),
    url(r'^(?P<pk>\d+)/', views.ArticleUpdateView.as_view(), name="article_update"),

]
