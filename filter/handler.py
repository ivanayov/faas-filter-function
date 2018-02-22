import requests
import json

def handle(st):
    req=json.loads(st)
    if not "RT" in message['text']:
        message={"text": req["text"] + " " + req["username"] + " " + req["link"]}
    else:
        message={"text": "This is a filtered message"}
    r=requests.post("https://hooks.slack.com/services", json=message)
    print(r)
