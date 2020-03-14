from django.contrib import admin
from django.conf.urls import url, include

from . import views


admin.autodiscover()

urlpatterns = [

    url(r'^$', views.IndexView.as_view(), name='index'),

    # Admin urls
    url(r'^admin/', admin.site.urls, name='admin'),
    url(r'^admin_tools/', include('admin_tools.urls')),

    # Login redirect urls
    url(r'^login/$', views.LoginView.as_view(), name='login'),
    url(r'^logout/$', views.LogoutView.as_view(), name='logout'),

    url(r"^articles/", include("xb1.articles.urls")),

]
