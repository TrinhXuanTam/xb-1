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
    url(r'^get_articles_by_category', views.GetArticlesByCategoryView.as_view(), name="get_articles_by_category"),
    url(r'^get_all_articles', views.GetAllArticlesView.as_view(), name="get_all_articles"),
    url(r'^search_articles', views.ArticleSearchView.as_view(), name="search_articles"),
    url(r'^article_delete', views.ArticleDeleteView.as_view(), name="article_delete"),
    url(r'^hide_article', views.HideArticleView.as_view(), name="hide_article"),
    url(r'^publish_article', views.PublishArticleView.as_view(), name="publish_article"),

    # Comments
    url(r'^post_comment', login_required(views.PostCommentView.as_view()), name="post_comment"),
    url(r'^comment/(?P<pk>\d+)/ban', views.BanCommentView.as_view(), name="ban_comment"),
    url(r'^comment/(?P<pk>\d+)/unban', views.UnbanCommentView.as_view(), name="unban_comment"),

]
