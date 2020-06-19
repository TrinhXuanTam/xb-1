from django.test import TestCase
from django.test import LiveServerTestCase
from django.urls import reverse

from selenium import webdriver

from ..settings import WEB_DRIVER_LOCATION

#class Test(SeleniumTestCase):
#
#	def test_X(self):
#		print(self.live_server_url)
#		WEB_DRIVER = webdriver.Chrome(WEB_DRIVER_LOCATION)
#		WEB_DRIVER.get('http://www.seznam.cz')
	