from django.test import TestCase
from django.test import LiveServerTestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse

from selenium import webdriver

from .settings import WEB_DRIVER_LOCATION

class SeleniumTestCase(StaticLiveServerTestCase):

	def setUp(self):
		self.wb = webdriver.Chrome(WEB_DRIVER_LOCATION)
		super(StaticLiveServerTestCase, self).setUp()

	def tearDown(self):
		self.wb.close()
		super(StaticLiveServerTestCase, self).tearDown()
