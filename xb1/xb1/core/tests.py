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

from selenium import webdriver  
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from ..driver import getDriver

import time

class AuthenticationTests(SeleniumTestCase):

	def test_register(self):
		driver = getDriver()
		driver.get("http://www.seznam.cz")
		
		time.sleep(2)
		
		element = driver.find_element_by_xpath('//*[@id="hp-app"]/div/div[1]/div[2]/div/div/div[1]/header/div/div/div[2]/div[1]/form/div/label/input')
		
		time.sleep(2)
		driver.quit()
		print("XXX")
