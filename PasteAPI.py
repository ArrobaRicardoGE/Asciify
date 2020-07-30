#Simple script to make a pastw with paste.ee API

import requests,json

def createNewPaste(string,name,token):
    headers = {'Content-Type':'application/json','X-Auth-Token':token}
    payload = {'sections':[{'name':name, 'syntax':'text','contents':string}]}
    r = requests.post("https://api.paste.ee/v1/pastes",headers=headers,data=json.dumps(payload))
    if('201' in str(r)):
        return json.loads(r.text)["link"]
    else:
        return ""

