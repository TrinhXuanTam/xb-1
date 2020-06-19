from django.test import TestCase
from django.test import LiveServerTestCase
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.urls import reverse
from unittest import skip

from ..tests import SeleniumTestCase
from .models import User
from .tokens import account_activation_token

import time

class AuthenticationTests(SeleniumTestCase):

	def test_register(self):
		self.wb.get('%s%s' % (self.live_server_url, ''))
		time.sleep(2)

		loginPopup = self.wb.find_element_by_xpath('/html/body/div[3]/ul[1]/li[1]/a')
		loginPopup.click()

		time.sleep(1)

		registerButtonRedirect = self.wb.find_element_by_xpath('//*[@id="sign_up"]')
		registerButtonRedirect.click()

		time.sleep(2)

		nameField = self.wb.find_element_by_xpath('/html/body/div[4]/div/div[2]/div/form/p[1]/input')
		nameField.send_keys('test')

		emailField = self.wb.find_element_by_xpath('/html/body/div[4]/div/div[2]/div/form/p[2]/input')
		emailField.send_keys('test@localhost.yyy')

		passwordField = self.wb.find_element_by_xpath('/html/body/div[4]/div/div[2]/div/form/p[3]/input')
		passwordField.send_keys('XQhdTsbfg5')

		repasswordField = self.wb.find_element_by_xpath('/html/body/div[4]/div/div[2]/div/form/p[4]/input')
		repasswordField.send_keys('XQhdTsbfg5')

		confirmButton = self.wb.find_element_by_xpath('/html/body/div[4]/div/div[2]/div/form/div/button')
		confirmButton.click()

		time.sleep(1)

		user = User.objects.filter(email='test@localhost.yyy').first()
		self.assertNotEqual(user, None)

		self.wb.get('%s%s' % (self.live_server_url, reverse('activate_registration', kwargs={'uidb64': urlsafe_base64_encode(force_bytes(user.pk)), 'token': account_activation_token.make_token(user)})))
		logoutButton = self.wb.find_element_by_xpath('/html/body/div[3]/ul[2]/li/a')
		self.assertNotEqual(logoutButton, None)

	def test_login(self):
		User.objects.create_user(username='admin', email='admin@admin.com', password='admin')

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

		time.sleep(5)

		logoutButton = self.wb.find_element_by_xpath('/html/body/div[3]/ul[2]/li/a')
		self.assertNotEqual(logoutButton, None)
