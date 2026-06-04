import requests

url = "http://127.0.0.1:8000/chat"
payload = {"query": "What is the expense ratio of all the five mutual funds?"}

response = requests.post(url, json=payload)
print(response.json())
