from github import Github

class API:
    def __init__(self,key,page='Asciify/asciify.github.io'):
        self.gh = Github(key)
        self.repo = self.gh.get_repo(page)

    def postNewPage(self,name,string):
        response = self.repo.create_file("{}.html".format(name),name,string)
        return "https://asciify.github.io/{}".format(name)
