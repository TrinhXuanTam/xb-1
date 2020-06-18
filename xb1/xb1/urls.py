from django.contrib import admin
from django.conf.urls import url, include
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
from .views import activate_registration, PasswordChangeView, EmailChangeView, activate_email, ckeditor_browse, ckeditor_upload, ckeditor_delete
from django.contrib.auth import views as auth_views


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

    # Password reset urls
    url(r'^password_reset/$', views.PasswordResetView.as_view(), name='password_reset'),
    url(r'^password_reset/done/$', views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    url(r'^password_reset_complete/$', views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    # Profile view
    url(r'^profile/$', views.ProfileView.as_view(), name='profile'),

    # Register
    url(r'^register/', views.Register.as_view(), name='register'),

    # Apps.
    url(r"^articles/", include("xb1.articles.urls")),
    url(r"^core/", include("xb1.core.urls")),
    url(r"^contact/", include("xb1.contact.urls")),
    url(r"^forum/", include("xb1.forum.urls")),
    url(r"^eshop/", include("xb1.eshop.urls")),

    url(r"^sent/", views.ActivationSentView.as_view(), name="activation_sent"),
    path('activate_registration/<slug:uidb64>/<slug:token>/', activate_registration, name='activate_registration'),

    url(r'^profile/change_password/', PasswordChangeView.as_view(), name='change_password'),
    url(r'^profile/change_email/', EmailChangeView.as_view(), name='change_email'),
    path('activate_email/<slug:uidb64>/<slug:token>/', activate_email, name='activate_email'),

    # CKEDITOR
    # url(r'^ckeditor/', include('ckeditor_uploader.urls')),
    url(r'^ckeditor/upload/', ckeditor_upload, name='ckeditor_upload'),
    url(r'^ckeditor/browse/', ckeditor_browse, name='ckeditor_browse'),
    url(r'^ckeditor/delete/', ckeditor_delete, name='ckeditor_delete'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)