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


class QuestionScraper:

    firstLinkClass = "yuRUbf"

    def __init__(self, chromeDriverPath="/Users/mark/Documents/Rice/Junior - Fall/HackRice 11/StudyFlow/chromedriver-macOS", maximized=True, headless=False):
        chromeOptions = Options()
        if maximized:
            chromeOptions.add_argument("--kiosk")
        if headless:
            chromeOptions.add_argument("--headless")
        self.driver = webdriver.Chrome(chromeDriverPath, options=chromeOptions)
        self.driver.implicitly_wait(0.3)

    def search(self, question):
        print("Making search on question: " + question)
        self.driver.get("https://www.google.com/search?q=" + question)
        outerElem = self.driver.find_element_by_class_name(self.firstLinkClass)
        print("Found outer element: " + str(outerElem))
        link = outerElem.find_element_by_tag_name("a").get_attribute("href")
        textToSummarize = ""
        try:
            self.driver.get(link)
            print("Successfully navigated to main article")
            allParagraphs = self.driver.find_elements_by_css_selector("p")
            print("Printing all paragraph text:\n")
            for par in allParagraphs:
                if (len(par.text) > 30):
                    textToSummarize += par.text
            print("MADE IT")
        except Exception:
            pass
        return summarizeTextHelper(" ".join(textToSummarize.split()))


questionScraper = QuestionScraper(headless=True)

app = Flask(__name__)

@app.before_first_request
def doSomething():
    print("Handling first request")
    return

@app.route('/', methods=['GET'])
def index():
    return "Example response"


@app.route('/summarization', methods=['POST'])
def summarize():
    requestBody = request.form
    if 'text' not in requestBody:
        return Response(status=404, body="No text was sent in the request body")
    print("The text received is: " + requestBody['text'])
    r = summarizeTextHelper(requestBody['text'])
    print(r.text)
    response = Response("The summarized text is " + r.text)
    response.headers["Access-Control-Allow-Origin"] = "*"
    return response


@app.route('/askQuestion', methods=['POST'])
def askQuestion():
    requestBody = request.form
    if 'question' not in requestBody:
        return Response(status=404, body="No text was sent in the request body")
    r = questionScraper.search(requestBody['question'])
    print(r.text)
    response = Response("The answer to the question is " + r.text)
    response.headers["Access-Control-Allow-Origin"] = "*"
    return response


def summarizeTextHelper(text):
    return requests.post(
        "https://api.deepai.org/api/summarization",
        files={
            'text': text,
        },
        headers={'api-key': '62fe45ec-ddc4-4c46-b066-8601a1824018'}
    )


if __name__ == '__main__':
    app.run(host='0.0.0.0')
