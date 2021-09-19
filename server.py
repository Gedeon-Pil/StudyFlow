# Flask Imports
import requests
from flask import Flask, Response, request
import os

# Web Sraper Imports
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import time

dirname = os.path.dirname(__file__)


class GoogleScraper:

    # Constants
    FIRST_LINK_CLASS_NAME = "yuRUbf"
    MAXIMIZE_FLAG = "--kiosk"
    HEADLESS_FLAG = "--headless"
    GOOGLE_RESULT_CLASS_NAMES = ["Z0LcW XcVN5d", "FLP8od", "IZ6rdc", "zCubwf"]
    GOOGLE_SEARCH_ENDPOINT = "https://www.google.com/search?q="

    DRIVER_WAIT_TIME = 0.2
    MIN_PARAGRAPH_CHARS = 30


    def __init__(self, chromeDriverPath=os.path.join(dirname, "chromedriver-macOS"), maximized=True, headless=False):
        print("Chromedriver path is: " + chromeDriverPath)
        chromeOptions = Options()
        if maximized:
            chromeOptions.add_argument(self.MAXIMIZE_FLAG)
        if headless:
            chromeOptions.add_argument(self.HEADLESS_FLAG)
        self.driver = webdriver.Chrome(chromeDriverPath, options=chromeOptions)
        self.driver.implicitly_wait(self.DRIVER_WAIT_TIME)


    def getGoogleResult(self, query):
        print("Getting Google result for query: " + query)
        self.driver.get(self.GOOGLE_SEARCH_ENDPOINT + query)
        for className in self.GOOGLE_RESULT_CLASS_NAMES:
            foundElem = self.parseGoogleEndorsedResults(className)
            if (foundElem):
                return foundElem
        return False

    def parseGoogleEndorsedResults(self, className):
        try:
            print("Checking query against class name " + className)
            foundElem = self.driver.find_element_by_class_name(className)
            print("Found elem for class name " + className)
            allText = foundElem.text
            for elem in foundElem.find_elements_by_xpath(".//*"):
                print("Child found")
                allText += elem.text
            return " ".join(allText.split())
        except Exception as e:
            print(e)
            return False


    def getBestResult(self, query):
        print("Getting best result for query: " + query)
        self.driver.get(self.GOOGLE_SEARCH_ENDPOINT + query)
        outerElem = self.driver.find_element_by_class_name(self.FIRST_LINK_CLASS_NAME)
        link = outerElem.find_element_by_tag_name("a").get_attribute("href")
        textToSummarize = str()
        try:
            self.driver.get(link)
            print("Successfully navigated to main article")
            allParagraphs = self.driver.find_elements_by_css_selector("p")
            for par in allParagraphs:
                if (len(par.text) >= self.MIN_PARAGRAPH_CHARS):
                    textToSummarize += par.text
            print("MADE IT")
        except Exception as e:
            print(e)
        return summarizeTextHelper(" ".join(textToSummarize.split()))

    def shutDown(self):
        self.driver.quit()

    def getCorrectChromedriverPath(self):
        pass

    def cleanUpQueryResult(self, text):
        return ""


googleScraper = GoogleScraper(headless=False)
app = Flask(__name__)

@app.before_first_request
def doSomething():
    print("Handling first request")
    return

@app.route('/', methods=['GET'])
def index():
    return generateResponse("The flask server is up and running!")


@app.route('/query', methods=['POST'])
def summarize():
    requestBody = request.form.to_dict()
    print(requestBody)
    if len(requestBody) != 1:
        return Response(status=404, response="Form data should only have one key-value pair")
    return handleQueryRequest(*requestBody.popitem())


def handleQueryRequest(action, query):
    if action == "summarize":
        summarizeResults = summarizeTextHelper(query)
        return generateResponse(summarizeResults)
    elif action == "define":
        # Call Meriam-Webster API
        return generateResponse("Definition API is not yet implemented")
    elif action == "elaborate":
        elaborateResults = googleScraper.getBestResult(query)
        return generateResponse(elaborateResults)
    elif action == "custom":
        googleResults = googleScraper.getGoogleResult(query)
        if googleResults:
            return generateResponse(googleResults)
        return generateResponse(googleScraper.getBestResult(query))
    else:
        return Response(status=404, body="Did not recognize form-data key: " + key)


def summarizeTextHelper(text):
    return requests.post(
        "https://api.deepai.org/api/summarization",
        files={
            'text': text,
        },
        headers={'api-key': '62fe45ec-ddc4-4c46-b066-8601a1824018'}
    )

def generateResponse(msg):
    response = Response(msg)
    response.headers["Access-Control-Allow-Origin"] = "*"
    return response


if __name__ == '__main__':
    app.run(host='0.0.0.0')
