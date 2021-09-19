# Flask Imports
import os

# Web Sraper Imports
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import time


class QuestionScraper:

    CLASS_NAME = "Z0LcW XcVN5d"

    def __init__(self, chromeDriverPath="/Users/mark/Documents/Rice/Junior - Fall/HackRice 11/StudyFlow/chromedriver-macOS", maximized=True, headless=False):
        chromeOptions = Options()
        if maximized:
            chromeOptions.add_argument("--kiosk")
        if headless:
            chromeOptions.add_argument("--headless")
        self.driver = webdriver.Chrome(chromeDriverPath, options=chromeOptions)
        self.driver.implicitly_wait(0.5)

    def search(self, question, sleepTime=0.5):

        print("Making search")
        self.driver.get("https://www.google.com/search?q=" + question)
        time.sleep(2)
        otherElem = self.driver.find_element_by_xpath("/html/body/div[7]/div/div[8]/div[1]/div/div[2]/div[2]/div/div/div[1]/div/div[1]/div[1]/div[1]/div/div[2]/div/div/div/div[1]")
        foundElem = self.driver.find_element_by_class_name("Z0LcW XcVN5d")
        print(foundElem)
        return "Example string"


if __name__ == '__main__':
    q = QuestionScraper()
    print(q.search("how tall is mount everest"))
