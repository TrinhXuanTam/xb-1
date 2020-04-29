from django.conf.urls import url

from . import views

app_name = 'articles'
urlpatterns = [

    # Articles
    url(r'^$', views.ArticleListView.as_view(), name="article_list"),
    url(r'^create/$', views.ArticleCreateView.as_view(), name="article_create"),
    url(r'^(?P<pk>\d+)/', views.ArticleUpdateView.as_view(), name="article_update"),
    url(r'^(?P<slug>[\w-]+)/$', views.ArticleDetailView.as_view(), name="detail"),
    
]
