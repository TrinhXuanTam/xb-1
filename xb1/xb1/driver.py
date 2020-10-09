import os

from selenium import webdriver  
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

def getDriver():
	return webdriver.Remote(command_executor=os.getenv('SELENIUM_REMOTE_ADDRESS', 'localhost:4444/wd/hub'), desired_capabilities=DesiredCapabilities.CHROME)