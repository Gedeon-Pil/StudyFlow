import requests

r = requests.post(
    "https://api.deepai.org/api/summarization",
    files={
        'text': open('test_files/tennis.txt', 'rb'),
    },
    headers={'api-key': '62fe45ec-ddc4-4c46-b066-8601a1824018'}
)
print(r.json())
