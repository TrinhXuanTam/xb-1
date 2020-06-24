from django.test import TestCase
from django.test import LiveServerTestCase
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.urls import reverse

from selenium.common.exceptions import NoSuchElementException

from unittest import skip

from ..tests import SeleniumTestCase
from ..settings import BASE_DIR
from .models import User
from .models import Profile
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
		
		try:
			self.wb.find_element_by_xpath('/html/body/div[3]/ul[2]/li/a')
		except NoSuchElementException:
			self.fail("Login failed")
	
	def test_login(self):
		User.objects.create_user(username='admin', email='admin@admin.com', password='admin')
		result = super().login('admin', 'admin')
		self.assertEqual(result, 0)

	def test_change_profile(self):
		user = User.objects.create_user(username='admin', email='admin@admin.com', password='admin')
		Profile.objects.create(user=user)
		
		result = super().login('admin', 'admin')
		self.assertEqual(result, 0)
		
		profileLink = self.wb.find_element_by_xpath('/html/body/div[3]/ul[1]/li[1]/a')
		profileLink.click()
		
		time.sleep(2)
		
		nickname = 'XXX'
		firstname = 'YYY'
		lastname = 'ZZZ'
		city = 'AAA'
		postNumber = '15500'
		address = '5525'
		phoneNumber = '777000777'
		imageLocation = '/resource/test/profileImage.png'
		
		nicknameField = self.wb.find_element_by_xpath('/html/body/div[4]/div/div[2]/form/div/input[4]')
		nicknameField.send_keys(nickname)
		
		firstnameField = self.wb.find_element_by_xpath('/html/body/div[4]/div/div[2]/form/div/input[5]')
		firstnameField.send_keys(firstname)
		
		lastnameField = self.wb.find_element_by_xpath('/html/body/div[4]/div/div[2]/form/div/input[6]')
		lastnameField.send_keys(lastname)
		
		cityField = self.wb.find_element_by_xpath('/html/body/div[4]/div/div[2]/form/div/input[7]')
		cityField.send_keys(city)
		
		postNumberField = self.wb.find_element_by_xpath('/html/body/div[4]/div/div[2]/form/div/input[8]')
		postNumberField.send_keys(postNumber)
		
		addressField = self.wb.find_element_by_xpath('/html/body/div[4]/div/div[2]/form/div/input[9]')
		addressField.send_keys(address)
		
		phoneNumberField = self.wb.find_element_by_xpath('/html/body/div[4]/div/div[2]/form/div/input[10]')
		phoneNumberField.send_keys(phoneNumber)
		
		imageField = self.wb.find_element_by_xpath('/html/body/div[4]/div/div[2]/form/div/div/input')
		imageField.send_keys(BASE_DIR + imageLocation)

		confirmButton = self.wb.find_element_by_xpath('/html/body/div[4]/div/div[2]/form/div/button')
		confirmButton.click()
		
		time.sleep(2)
		
		nicknameField = self.wb.find_element_by_xpath('/html/body/div[5]/div/div[2]/form/div/input[4]')
		self.assertEqual(nicknameField.get_attribute('value'), nickname)
		
		firstnameField = self.wb.find_element_by_xpath('/html/body/div[5]/div/div[2]/form/div/input[5]')
		self.assertEqual(firstnameField.get_attribute('value'), firstname)
		
		lastnameField = self.wb.find_element_by_xpath('/html/body/div[5]/div/div[2]/form/div/input[6]')
		self.assertEqual(lastnameField.get_attribute('value'), lastname)
		
		cityField = self.wb.find_element_by_xpath('/html/body/div[5]/div/div[2]/form/div/input[7]')
		self.assertEqual(cityField.get_attribute('value'), city)
		
		postNumberField = self.wb.find_element_by_xpath('/html/body/div[5]/div/div[2]/form/div/input[8]')
		self.assertEqual(postNumberField.get_attribute('value'), postNumber)
		
		addressField = self.wb.find_element_by_xpath('/html/body/div[5]/div/div[2]/form/div/input[9]')
		self.assertEqual(addressField.get_attribute('value'), address)
		
		phoneNumberField = self.wb.find_element_by_xpath('/html/body/div[5]/div/div[2]/form/div/input[10]')
		self.assertEqual(phoneNumberField.get_attribute('value'), phoneNumber)