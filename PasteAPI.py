#Integration of the paste.ee API
#See https://pastee.github.io/docs/ for more information

import requests,json

class API:
    def __init__(self,token):
        self.token = token
    
    def createNewPaste(self,string,name = 'TW_ID'):
        headers = {'Content-Type':'application/json','X-Auth-Token':self.token}
        payload = {'sections':[{'name':name, 'syntax':'text','contents':string}]}
        r = requests.post("https://api.paste.ee/v1/pastes",headers=headers,data=json.dumps(payload))
        if(not '201' in str(r)): raise Exception('Unable to process the requests from createNewPaste: '+str(r))

    def retrieveLastId(self):
        headers = {'X-Auth-Token':self.token}
        id = self.getLastPaste()
        r = requests.get('https://api.paste.ee/v1/pastes/'+id,headers = headers)
        if(not '200' in str(r)): raise Exception('Unable to process the requests from retrieveLastId: '+str(r))
        return json.loads(r.text)['paste']['sections'][0]['contents']

    def deleteLastPaste(self):
        headers = {'X-Auth-Token':self.token}
        id = self.getLastPaste()
        r = requests.delete('https://api.paste.ee/v1/pastes/'+id,headers = headers)
        if(not '200' in str(r)): raise Exception('Unable to process the requests from deleteLastPaste: '+str(r))

    def getLastPaste(self):
        headers = {'X-Auth-Token':self.token}
        r = requests.get('https://api.paste.ee/v1/pastes',headers=headers)
        if(not '200' in str(r)): raise Exception('Unable to process the requests from getLastPaste: '+str(r))
        d = json.loads(r.text)
        if(len(d['data']) == 0):raise Exception('No pastes available')
        return d['data'][0]['id']

