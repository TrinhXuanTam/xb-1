from django.conf.urls import url

from . import views

app_name = 'shop'
urlpatterns = [
    url(r'^$', views.ShopIndex.as_view(), name='shopView'),

    # By PK of Item
    url(r'^cart/insert/(?P<pk>[0-9]+)$', views.CartInsertItemView.as_view(), name="cartinsert"),

    # By PK of CartEntry 
    url(r'^cart/update/(?P<pk>[0-9]+)/add$', views.CartAddItemView.as_view(), name="cartadd"),
    url(r'^cart/update/(?P<pk>[0-9]+)/remove$', views.CartRemoveItemView.as_view(), name="cartremove"),
    url(r'^cart/update/(?P<pk>[0-9]+)/discard$', views.CartDiscardItemView.as_view(), name="cartdiscard"),
    url(r'^cart/update/discard', views.CartDiscardItemView.as_view(), name="cartdiscardall"),

    url(r'^admin/item/list$', views.ItemListView.as_view(), name="adminItemList"),
    url(r'^admin/item/create$', views.ItemCreateView.as_view(), name="adminItemCreate"),
    url(r'^admin/item/detail/(?P<pk>[0-9]+)$', views.ItemDetailView.as_view(), name="adminItemDetail"),
]
