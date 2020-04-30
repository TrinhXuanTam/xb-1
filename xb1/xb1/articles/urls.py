from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from . import views

app_name = 'articles'
urlpatterns = [

    # Articles
    url(r'^$', views.ArticleListView.as_view(), name="article_list"),
    url(r'^create/$', views.ArticleCreateView.as_view(), name="article_create"),
    url(r'^(?P<pk>\d+)/', views.ArticleUpdateView.as_view(), name="article_update"),
    url(r'^(?P<slug>[\w-]+)/$', views.ArticleDetailView.as_view(), name="detail"),
    url(r'^post_comment', login_required(views.PostCommentView.as_view()), name="post_comment"),
    url(r'^post_reply', login_required(views.PostCommentReplyView.as_view()), name="post_reply"),
    
]
