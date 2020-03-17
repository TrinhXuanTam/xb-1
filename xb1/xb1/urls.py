from django.contrib import admin
from django.conf.urls import url, include
from . import views

admin.autodiscover()

urlpatterns = [
    # Index
    url(r'^$', views.IndexView.as_view(), name='index'),

    # Admin urls
    url(r'^admin/', admin.site.urls, name='admin'),
    url(r'^admin_tools/', include('admin_tools.urls')),

    # Login redirect urls
    url(r'^login/$', views.LoginView.as_view(), name='login'),
    url(r'^logout/$', views.LogoutView.as_view(template_name='registration/logout.html'), name='logout'),

    # Profile view
    url(r'^profile/$', views.profile, name='profile'),

    # Register
    url(r'^register/', views.register, name='register'),

    # Apps.
    url(r"^articles/", include("xb1.articles.urls")),
    url(r"^core/", include("xb1.core.urls")),

]
