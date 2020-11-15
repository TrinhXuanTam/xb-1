from django.conf.urls import url

from . import views

app_name = 'shop'
urlpatterns = [
    url(r'^$', views.ShopIndex.as_view(), name='shopView'),
    url(r'^cart/add/(?P<pk>[0-9]+)$', views.CartAddItemView.as_view(), name="additem")
]
