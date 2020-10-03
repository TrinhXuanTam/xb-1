from django.test import TestCase
from django.test import LiveServerTestCase
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.urls import reverse

from selenium.common.exceptions import NoSuchElementException

from unittest import skip

from ..tests import SeleniumAuthenticatedTestCase
from ..settings import BASE_DIR
from .models import User
from .models import Profile
from .tokens import account_activation_token

from selenium import webdriver  
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from ..driver import getDriver

import time

class AuthenticationTests(SeleniumAuthenticatedTestCase):

	def test_register(self):
		pass
	
	def test_login(self):
		super().login('admin', 'admin')
