from selenium import webdriver
from wrapperClass import Wrapper
import os
import time

class setup:

    def login(self):
        baseUrl = "https://crmee.smsdrift.ee/crm"
        driverLocation = "/usr/local/bin/chromedriver"
        os.environ["webdriver.chrome.driver"] = driverLocation
        # Instantiate FF Browser Command
        driver = webdriver.Chrome(driverLocation)
        w = Wrapper(driver)
        driver.get(baseUrl)

        driver.maximize_window()
        # driver.save_screenshot('D:\\selenium_tutorial\\test_screenshot.png')
        # we need to maximise windows otherwise nasty popup blocks teh view.

        driver.implicitly_wait(4)  # waits for page to load.
        userName = w.getElement("[name='userName']", "css")
        userName.send_keys("vesmase")
        password = w.getElement("[name='userPassword']", "css")
        password.send_keys("vesmase123")
        loginBtn = w.getElement("[value='Login']", "css")
        loginBtn.click()
        driver.implicitly_wait(6)
        subnumTxt = w.getElement("//input[contains(@id,'SubNum')]", "xpath")
        if subnumTxt:
            print("Login successful")
        else:
            print("login failed")
        time.sleep(7)


ch = setup()
ch.login()
