#Modify a Gitlab project with the APIv4
import gitlab,base64

class API:
    def __init__(self,token,id =20359415):
        self.api = gitlab.Gitlab('https://gitlab.com',private_token=token)
        self.api.auth()
        self.project = self.api.projects.get(id)
    
    def getFile(self,name):
        return self.project.files.get(name,ref = 'master')

    def getFileStr(self,name):
        f = self.getFile(name)
        return f.decode().decode('utf-8')
    
    def updateFile(self,name,content):
        f = self.getFile(name)
        f.content = content
        f.save(branch = 'master', commit_message = 'UpdatedId'+content)

    def uploadFile(self,name,content,user = 'ArrobaRicardoGE',mail = 'mail@domain.com',extension = '.html'):
        encodedData = encodedData = base64.b64encode(bytes(content,'utf-8'))
        payload = {
            'file_path':name+extension,
            'branch':'master',
            'content':encodedData.decode('utf-8'),
            'author_email':mail,
            'author_name':user,
            'encoding':'base64',
            'commit_message':name
        }
        self.project.files.create(payload)
        return 'https://asciifyapp.netlify.app/'+name
    