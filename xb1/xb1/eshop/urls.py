from django.conf.urls import url

from . import views

app_name = 'eshop'
urlpatterns = [

	url(r'^$', views.ShopIndex.as_view(), name='shopIndex'),
	

	url(r'^manage/cart/add/(?P<pk>[0-9]+)$', views.CartItemAddView.as_view(), name="cartItemAdd"),
	url(r'^manage/cart/remove/(?P<pk>[0-9]+)$', views.CartItemRemoveView.as_view(), name="cartItemRemove"),
	url(r'^manage/cart/discard/$', views.CartItemDiscardView.as_view(), name="cartItemsDiscard"),
	url(r'^manage/cart/discard/(?P<pk>[0-9]+)$', views.CartItemDiscardView.as_view(), name="cartItemDiscard"),
	
	url(r'^manage/shop/list/$', views.ShopItemListView.as_view(), name="manageShopList"),
	url(r'^manage/shop/add/$', views.ShopItemCreateView.as_view(), name="manageShopCreate"),
	url(r'^manage/shop/update/(?P<pk>[0-9]+)$', views.ShopItemUpdateView.as_view(), name = "manageShopUpdate"),
	
	url(r'^manage/order/create/$', views.OrderCreateView.as_view(), name = "manageOrderCreate"),
	url(r'^manage/order/list/$', views.OrderListView.as_view(), name="manageOrderList"),
	url(r'^manage/order/remove/(?P<pk>[0-9]+)$', views.OrderRemoveView.as_view(), name="manageOrderRemove"),
	url(r'^manage/order/pay/(?P<pk>[0-9]+)$', views.OrderPayView.as_view(), name="manageOrderPay"),
	
]