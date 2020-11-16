from django.conf.urls import url

from . import views

app_name = 'shop'
urlpatterns = [
    url(r'^$', views.ShopIndex.as_view(), name='shopView'),
    url(r'^cart/add/(?P<pk>[0-9]+)$', views.CartAddItemView.as_view(), name="cartadd"),
    url(r'^cart/remove/(?P<pk>[0-9]+)$', views.CartRemoveItemView.as_view(), name="cartremove"),
    url(r'^cart/discard/(?P<pk>[0-9]+)$', views.CartDiscardItemView.as_view(), name="cartdiscard"),
    url(r'^cart/discard/', views.CartDiscardItemView.as_view(), name="cartdiscardall")
]
