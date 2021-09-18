import requests
from flask import Flask, Response, request
import os

dirname = os.path.dirname(__file__)

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
    return Response("The summarized text is " + r.text)


@app.route('/askQuestion', methods=['POST'])
def test():
    requestBody = request.form
    if 'question' not in requestBody:
        return Response(status=404, body="No text was sent in the request body")
    r = searchQuestion(requestBody['question'])
    print(r.text)
    return Response("The answer to the question is " + r.text)


def summarizeTextHelper(text):
    return requests.post(
        "https://api.deepai.org/api/summarization",
        files={
            'text': text,
        },
        headers={'api-key': '62fe45ec-ddc4-4c46-b066-8601a1824018'}
    )

def searchQuestion(text):
    return ""


if __name__ == '__main__':
    app.run(host='0.0.0.0')
