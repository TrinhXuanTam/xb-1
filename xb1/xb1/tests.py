import time

from .driver import getDriver

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import TestCase
from django.test import LiveServerTestCase
from django.urls import reverse

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

class SeleniumTestCase(StaticLiveServerTestCase):

	def setUp(self):
		self.wb = getDriver()
		super(StaticLiveServerTestCase, self).setUp()

	def tearDown(self):
		self.wb.quit()
		super(StaticLiveServerTestCase, self).tearDown()
		
class SeleniumAuthenticatedTestCase(SeleniumTestCase):

	def login(self, name, password):
		print('%s%s' % (self.live_server_url, reverse('index')))
		self.wb.get('%s%s' % (self.live_server_url, reverse('index')))
		time.sleep(1)
		loginPopup = self.wb.find_element_by_xpath('/html/body/div[3]/ul[1]/li[1]/a')
		loginPopup.click()
		time.sleep(1)
		nameField = self.wb.find_element_by_xpath('//*[@id="id_username"]')
		nameField.send_keys(name)
		passwordField = self.wb.find_element_by_xpath('//*[@id="id_password"]')
		passwordField.send_keys(password)
		loginButton = self.wb.find_element_by_xpath('//*[@id="login_form"]/button')