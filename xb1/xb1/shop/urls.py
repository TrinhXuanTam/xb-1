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
    url(r'^cart/update/(?P<pk>[0-9]+)/set/(?P<spec>[0-9]+)', views.CartSetSpecificationView.as_view(), name="cartspecificationset"),

    url(r'^admin/item/list$', views.ItemListView.as_view(), name="adminItemList"),
    url(r'^admin/item/create$', views.ItemCreateView.as_view(), name="adminItemCreate"),
    url(r'^admin/item/create/(?P<pk>[0-9]+)$', views.ItemCreateAsView.as_view(), name="adminItemCreateAs"),
    url(r'^admin/item/delete/(?P<pk>[0-9]+)$', views.ItemDeleteView.as_view(), name="adminItemDelete"),
    url(r'^admin/item/detail/(?P<pk>[0-9]+)$', views.ItemDetailView.as_view(), name="adminItemDetail"),
    url(r'^admin/item/update/(?P<pk>[0-9]+)$', views.ItemUpdateView.as_view(), name="adminItemUpdate"),
    url(r'^admin/item/deactivate/(?P<pk>[0-9]+)$', views.ItemDeactivateView.as_view(), name="adminItemDeactivate"),


    url(r'^order/create$', views.OrderCreateView.as_view(), name="orderCreate"),
    url(r'^order/tracker/(?P<slug>[\w-]+)/$', views.OrderTrackerView.as_view(), name="orderTracker"),

    url(r'^user/order/list$', views.OrderListUserView.as_view(), name="userOrderList"),

    url(r'^admin/order/list$', views.OrderListView.as_view(), name="adminOrderList"),
    url(r'^admin/order/payment/confirm/(?P<pk>[0-9]+)$', views.OrderPaymentConfirmView.as_view(), name="adminOrderPaymentConfirm"),
    url(r'^admin/order/payment/revoke/(?P<pk>[0-9]+)$', views.OrderPaymentRevokeView.as_view(), name="adminOrderPaymentRevoke"),
    url(r'^admin/order/detail/(?P<pk>[0-9]+)$', views.OrderDetailView.as_view(), name="adminOrderDetail"),
]
