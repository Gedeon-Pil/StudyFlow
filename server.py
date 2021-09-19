# Flask Imports
import requests
import os
import platform
from flask import Flask, Response, request
import json

# Web Sraper Imports
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import time


class GoogleScraper:

    # Constants
    FIRST_LINK_CLASS_NAME = "yuRUbf"
    MAXIMIZE_FLAG = "--kiosk"
    HEADLESS_FLAG = "--headless"
    GOOGLE_RESULT_CLASS_NAMES = ["Z0LcW XcVN5d", "FLP8od", "IZ6rdc", "zCubwf"]
    GOOGLE_SEARCH_ENDPOINT = "https://www.google.com/search?q="

    DRIVER_WAIT_TIME = 0.2
    MIN_PARAGRAPH_CHARS = 30

    DIR_NAME = os.path.dirname(__file__)
    PLATFORM_NAME = platform.system()


    def __init__(self, maximized=True, headless=True):
        chromeOptions = Options()
        if maximized:
            chromeOptions.add_argument(self.MAXIMIZE_FLAG)
        if headless:
            chromeOptions.add_argument(self.HEADLESS_FLAG)
        chromeDriverPath = self.getCorrectChromeDriverPath()
        self.driver = webdriver.Chrome(chromeDriverPath, options=chromeOptions)


    def getGoogleResult(self, query):
        print("Getting Google result for query: " + query)
        self.driver.get(self.GOOGLE_SEARCH_ENDPOINT + query)
        time.sleep(self.DRIVER_WAIT_TIME)
        for className in self.GOOGLE_RESULT_CLASS_NAMES:
            foundElem = self.parseGoogleEndorsedResults(className)
            if (foundElem):
                return foundElem
        return False

    def parseGoogleEndorsedResults(self, className):
        try:
            foundElem = self.driver.find_element_by_class_name(className)
            print("Found elem for class name " + className)
            allText = foundElem.text
            for elem in foundElem.find_elements_by_xpath(".//*"):
                allText += elem.text
            return allText
        except Exception as e:
            return False


    def getBestResult(self, query):
        print("Getting best result for query: " + query)
        self.driver.get(self.GOOGLE_SEARCH_ENDPOINT + query)
        time.sleep(self.DRIVER_WAIT_TIME)
        outerElem = self.driver.find_element_by_class_name(self.FIRST_LINK_CLASS_NAME)
        time.sleep(self.DRIVER_WAIT_TIME)
        link = outerElem.find_element_by_tag_name("a").get_attribute("href")
        textToSummarize = ""
        try:
            time.sleep(self.DRIVER_WAIT_TIME)
            self.driver.get(link)
            print("Successfully navigated to main article")
            allParagraphs = self.driver.find_elements_by_css_selector("p")
            for par in allParagraphs:
                if (len(par.text) >= self.MIN_PARAGRAPH_CHARS):
                    textToSummarize += par.text
        except Exception as e:
            print(e)
        return summarizeTextHelper(textToSummarize)


    def getCorrectChromeDriverPath(self):
        if self.PLATFORM_NAME == "Darwin":
            return os.path.join(self.DIR_NAME, "chromedriver-macOS")
        elif self.PLATFORM_NAME == "Windows":
            return os.path.join(self.DIR_NAME, "chromedriver-win64")
        raise Exception("There is only chromedriver support of Mac and Windows")


    def shutDown(self):
        self.driver.quit()


googleScraper = GoogleScraper()
app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    return generateResponse("The flask server is up and running!", 200)


@app.route('/query', methods=['POST'])
def summarize():
    requestBody = request.form.to_dict()
    if len(requestBody) != 1:
        print("Form data should have exactly one key-value pair")
        return generateResponse("Form data should only have one key-value pair", 404)
    return handleQueryRequest(*requestBody.popitem())


def handleQueryRequest(action, query):
    if action == "summarize":
        return generateResponse(summarizeTextHelper(query), 200)
    elif action == "define":
        return generateResponse(getDefinitionHelper(query), 200)
    elif action == "elaborate":
        return generateResponse(googleScraper.getBestResult(query), 200, True)
    elif action == "custom":
        googleResults = googleScraper.getGoogleResult(query)
        if googleResults:
            return generateResponse(googleResults, 200)
        return generateResponse(googleScraper.getBestResult(query), True)
    else:
        return generateResponse("Did not recognize form-data key: " + key, 404)


def summarizeTextHelper(text):
    response = requests.post(
        "https://api.deepai.org/api/summarization",
        files={
            'text': text,
        },
        headers={'api-key': '62fe45ec-ddc4-4c46-b066-8601a1824018'}
    )
    jsonResponse = json.loads(response.text)
    if "output" in jsonResponse and jsonResponse["output"] != "":
        return jsonResponse["output"]
    return "Not enough text to summarize."


def getDefinitionHelper(word):
    response = requests.get("https://api.dictionaryapi.dev/api/v2/entries/en/" + word)
    allMeanings = json.loads(response.text)[0]["meanings"]
    topDefinitions = []
    for index in range(len(allMeanings)):
        meaning = allMeanings[index]
        partOfSpeech = meaning["partOfSpeech"]
        definition = meaning["definitions"][0]["definition"]
        topDefinitions.append(setFirstUppercase(partOfSpeech) + ": " + setFirstUppercase(definition))
    return "\n".join(topDefinitions)


def generateResponse(text, statusCode, cleanUp=False):
    if cleanUp:
        text = cleanUpResponse(text)
    response = Response(status=statusCode, response=text)
    response.headers["Access-Control-Allow-Origin"] = "*"
    print("Responding with status code: " + str(statusCode) + " and message " + str(text))
    return response


def cleanUpResponse(text, maxSentences=5, minSentenceLength=30):
    punctuationMarks = {".", "?", "!"}
    newText = ""
    for char in text:
        newText += char
        if char in punctuationMarks:
            newText += " "
    text = " ".join(newText.split())

    sentenceCount = 0
    index = 0
    prevIndex = 0
    textLength = len(text)
    textResult = ""
    while index < textLength:
        if text[index] in punctuationMarks:
            if index - prevIndex >= minSentenceLength:
                sentenceCount += 1
                textResult += text[prevIndex:index + 1]
                if (sentenceCount == 5):
                    break
            prevIndex = index + 1
        index += 1
    index -= 1
    if sentenceCount < 5:
        textResult += text[prevIndex:]
    return textResult


def setFirstUppercase(s):
    return s[0].upper() + s[1:]


if __name__ == '__main__':
    app.run(host='0.0.0.0')
