from django.conf.urls import url

from . import views

app_name = 'eshop'
urlpatterns = [
	url(r'^$', views.ShopIndex.as_view(), name='shopIndex'),
	
	url(r'^manage/add/$', views.ShopItemCreateView.as_view(), name="shopItemCreate")
]
