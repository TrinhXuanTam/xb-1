from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from . import views

app_name = 'forum'
urlpatterns = [

    # Forum
    url(r'^$', views.ForumIndexView.as_view(), name="index"),
    url(r'^category/(?P<pk>\d+)/$', views.ForumListView.as_view(), name="forum_list"),
    url(r'^category/$', views.ForumListView.as_view(), name="forum_list"),
    url(r'^forum-category-create/$', views.ForumCategoryCreateView.as_view(), name="create_forum_category"),
    url(r'^forum-category-update/(?P<pk>\d+)/$', views.ForumCategoryUpdateView.as_view(), name="update_forum_category"),
    url(r'^forum-category-delete/(?P<pk>\d+)/$', views.ForumCategoryDeleteView.as_view(), name="delete_forum_category"),
    url(r'^forum-detail/(?P<pk>\d+)/$', views.ForumDetailView.as_view(), name="forum_detail"),
    url(r'^forum-category/(?P<pk>\d+)/create-forum/$', views.ForumCreateView.as_view(), name="create_forum"),
    url(r'^forum-delete/(?P<pk>\d+)/$', views.ForumDeleteView.as_view(), name="delete_forum"),

    url(r'^post-comment', login_required(views.PostCommentView.as_view()), name="post_comment"),
]
