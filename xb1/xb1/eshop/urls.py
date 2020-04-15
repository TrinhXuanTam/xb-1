from django.conf.urls import url

from . import views

app_name = 'eshop'
urlpatterns = [
	url(r'^$', views.ShopIndex.as_view(), name='shopIndex'),
	url(r'^add/$', views.ShopItemAddView.as_view(), name="shopItemAdd"),
	url(r'^removeall/$', views.ShopItemRemoveAllView.as_view(), name="shopItemRemoveAll"),
	url(r'^manage/add/$', views.ShopItemCreateView.as_view(), name="shopItemCreate")
]
