from django.contrib import admin
from django.conf.urls import url, include
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
from .views import activate, ckeditor_browse, ckeditor_upload, ckeditor_delete

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

    # CKEDITOR
    # url(r'^ckeditor/', include('ckeditor_uploader.urls')),
    url(r'^ckeditor/upload/', ckeditor_upload, name='ckeditor_upload'),
    url(r'^ckeditor/browse/', ckeditor_browse, name='ckeditor_browse'),
    url(r'^ckeditor/delete/', ckeditor_delete, name='ckeditor_delete')

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)