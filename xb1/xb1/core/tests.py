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

import time

class AuthenticationTests(SeleniumTestCase):

	def test_register(self):
		driver = webdriver.Remote(command_executor='http://selenium_hub:4444/wd/hub', desired_capabilities=DesiredCapabilities.CHROME)
		driver.get("http://www.seznam.cz")
		
		time.sleep(2)
		driver.quit()
		print("XXX")
