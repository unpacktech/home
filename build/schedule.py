import os
import json
import requests


API_TOKEN = os.environ.get("API_TOKEN", "")
DATE = os.environ.get("DATE", "")
if API_TOKEN == "":
    raise RuntimeError("Please specify the API token")
if DATE == "":
    raise RuntimeError("Please specify the date")

with open(f"./content/{DATE}.json", "r") as f:
    source = f.read()
    parsed = json.loads(source)
print(parsed)

if "title" not in parsed:
    print(source)
    raise RuntimeError("Something's wrong with the content")

response = requests.get(f"https://unpack.tech/{DATE}-email")
response.raise_for_status()

CONTENT = response.text
print(CONTENT)

# if campaign exists already
url = "https://api.sender.net/v2/campaigns"

headers = {
    "Authorization": f"Bearer {API_TOKEN}",
    "Content-Type": "application/json",
    "Accept": "application/json",
}

payload = {
    "title": f"Unpack.tech {DATE}",
    "from": "Unpack.tech",
    "subject": "📦 " + parsed.get("title"),
    "reply_to": "mark@unpack.tech",
    "google_analytics": 1,
    "segments": ["dN8l8a"],
    "content_type": "html",
    "content": CONTENT,
}

response = requests.request('POST', url, headers=headers,json=payload)
response.raise_for_status()
RESPONSE = response.json()
print(RESPONSE)

success = RESPONSE.get("success")
if not success:
    raise RuntimeError("Got error response from sender.net")