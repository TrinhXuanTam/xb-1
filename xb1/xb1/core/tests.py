from django.test import TestCase
from django.test import LiveServerTestCase

from django.urls import reverse
from unittest import skip

from ..tests import SeleniumTestCase
from .models import User

import time

class AuthenticationTests(SeleniumTestCase):
	
	@skip
	def test_register(self):
		self.wb.get('%s%s' % (self.live_server_url, reverse('eshop:shopIndex')))
		print(User.objects.count())
		time.sleep(2)

	def test_login(self):
		User.objects.create_user(username='admin', email='admin@admin.com', password='admin')
			
		print(User.objects.count())
		
		self.wb.get('%s%s' % (self.live_server_url, ''))
		time.sleep(2)
		
		loginPopup = self.wb.find_element_by_xpath('/html/body/div[3]/ul[1]/li[1]/a')
		loginPopup.click()
		
		time.sleep(1)
		
		nameField = self.wb.find_element_by_xpath('//*[@id="id_username"]')
		nameField.send_keys('admin')
		
		passwordField = self.wb.find_element_by_xpath('//*[@id="id_password"]')
		passwordField.send_keys('admin')
		
		loginButton = self.wb.find_element_by_xpath('//*[@id="login_form"]/button')
		loginButton.click()
		
		time.sleep(2)
		
		logoutButton = self.wb.find_element_by_xpath('/html/body/div[3]/ul[2]/li/a')
		self.assertNotEqual(logoutButton, None)