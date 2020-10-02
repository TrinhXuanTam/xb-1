from django.test import TestCase
from django.test import LiveServerTestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

from .settings import WEB_DRIVER_LOCATION

import time

class SeleniumTestCase(StaticLiveServerTestCase):

	def setUp(self):
		super(StaticLiveServerTestCase, self).setUp()

	def tearDown(self):
		super(StaticLiveServerTestCase, self).tearDown()

	def login(self):
		print("XXX")
		return 0