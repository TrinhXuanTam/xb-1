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
		self.wb = webdriver.Chrome(WEB_DRIVER_LOCATION)
		super(StaticLiveServerTestCase, self).setUp()

	def tearDown(self):
		self.wb.close()
		super(StaticLiveServerTestCase, self).tearDown()

	def login(self, name, password):
		self.wb.get('%s%s' % (self.live_server_url, reverse('index')))
		time.sleep(2)
		
		isLogged = True
		try:
			self.wb.find_element_by_xpath('/html/body/div[3]/ul[2]/li/a')
		except NoSuchElementException:
			isLogged = False
			
		if isLogged is True:
			return 1
			
		loginPopup = self.wb.find_element_by_xpath('/html/body/div[3]/ul[1]/li[1]/a')
		loginPopup.click()
		time.sleep(2)

		nameField = self.wb.find_element_by_xpath('//*[@id="id_username"]')
		nameField.send_keys(name)

		passwordField = self.wb.find_element_by_xpath('//*[@id="id_password"]')
		passwordField.send_keys(password)
		
		loginButton = self.wb.find_element_by_xpath('//*[@id="login_form"]/button')
		loginButton.click()
		time.sleep(2)
		
		try:
			self.wb.find_element_by_xpath('/html/body/div[3]/ul[2]/li/a')
		except NoSuchElementException:
			return 2
			
		return 0