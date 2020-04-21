from django.conf.urls import url

from . import views

app_name = 'eshop'
urlpatterns = [
	url(r'^$', views.ShopIndex.as_view(), name='shopIndex'),
	
	url(r'^order/$', views.OrderCreateView.as_view(), name = "orderCreate"),
	
	url(r'^add/$', views.OrderItemAddView.as_view(), name="orderItemAdd"),
	url(r'^remove/$', views.OrderItemRemoveView.as_view(), name="orderItemRemove"),
	url(r'^removeall/$', views.OrderItemRemoveAllView.as_view(), name="orderItemRemoveAll"),
	
	url(r'^manage/add/$', views.ShopItemCreateView.as_view(), name="shopItemCreate")
]
