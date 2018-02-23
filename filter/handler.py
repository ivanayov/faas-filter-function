import requests, json, os

def handle(st):

    slack_hook_positive = os.getenv("slack_hook_positive")
    slack_hook_negative = os.getenv("slack_hook_negative")
    gateway_hostname = os.getenv("gateway_hostname", "gateway")

    req=json.loads(st)
    if not "RT" in req['text']:
        message={"text": req["text"] + " " + req["username"] + " " + req["link"]}
        res = requests.post('http://' + gateway_hostname + ':8080/function/sentimentanalysis', data=req["text"])
        

        if res.json()['polarity']  >  0.2:
            r=requests.post(slack_hook_positive, json=message)
        else:
            r=requests.post(slack_hook_negative, json=message)

        print(r)
