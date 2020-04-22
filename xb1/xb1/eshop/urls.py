from django.conf.urls import url

from . import views

app_name = 'eshop'
urlpatterns = [
	url(r'^$', views.ShopIndex.as_view(), name='shopIndex'),
	
	url(r'^order/$', views.OrderCreateView.as_view(), name = "orderCreate"),
	
	url(r'^add/$', views.OrderItemAddView.as_view(), name="orderItemAdd"),
	url(r'^remove/$', views.OrderItemRemoveView.as_view(), name="orderItemRemove"),
	url(r'^removeall/$', views.OrderItemRemoveAllView.as_view(), name="orderItemRemoveAll"),
	
	url(r'^manage/shop/list/$', views.ShopItemListView.as_view(), name="manageShopList"),
	url(r'^manage/shop/add/$', views.ShopItemCreateView.as_view(), name="shopItemCreate"),
	url(r'^manage/shop/update/(?P<pk>[0-9]+)$', views.ShopItemUpdateView.as_view(), name = "manageShopUpdate"),
	
]
