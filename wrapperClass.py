from selenium import webdriver
from selenium.webdriver.common.by import By
import os
import time


class Wrapper:
    def __init__(self, driver):
         self.driver = driver

    def getByType(self, locatorType):
        locatorType = locatorType.lower()
        if locatorType == "id":
            return By.ID

        elif locatorType == "xpath":
            return By.XPATH
        elif locatorType == "css":
            return By.CSS_SELECTOR
        else:
            print("Locator type is not supported")
            return False

    def getElement(self, locator, locatorType="id"):
        element = None
        try:
            locatorType = locatorType.lower()
            byType = self.getByType(locatorType)
            element = self.driver.find_element(byType, locator)
            # print("element found")
        except:
            print("element not found")
            return False
        return element


    def isElementPresent(self, locator, byType):
        element = None
        try:
            element = self.driver.find_element(byType, locator)
            if element:
                print("element found")
                return True
            else:
                return False
        except:
            print("element not found")
            return False

    def elementPresentCheck(self, locator, byType):
        try:
            elementList = self.driver.find_elements(byType, locator)
            if len(elementList) > 0:
                print("element found")
                return True
            else:
                return False

        except:
            print("element not found")
            return False