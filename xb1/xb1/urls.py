from django.contrib import admin
from django.conf.urls import url, include
from django.urls import path

from . import views
from .views import activate

admin.autodiscover()

urlpatterns = [
    # Index
    url(r'^$', views.IndexView.as_view(), name='index'),

    # Admin urls
    url(r'^admin/', admin.site.urls, name='admin'),
    url(r'^admin_tools/', include('admin_tools.urls')),

    # Login redirect urls
    url(r'^login/$', views.LoginView.as_view(), name='login'),
    url(r'^logout/$', views.LogoutView.as_view(), name='logout'),

    # Profile view
    url(r'^profile/$', views.ProfileView.as_view(), name='profile'),

    # Register
    url(r'^register/', views.Register.as_view(), name='register'),

    # Apps.
    url(r"^articles/", include("xb1.articles.urls")),
    url(r"^core/", include("xb1.core.urls")),
    url(r"^contact/", include("xb1.contact.urls")),
    url(r"^eshop/", include("xb1.eshop.urls")),

    url(r"^sent/", views.ActivationSentView.as_view(), name="activation_sent"),
    path('activate/<slug:uidb64>/<slug:token>/', activate, name='activate'),

]
