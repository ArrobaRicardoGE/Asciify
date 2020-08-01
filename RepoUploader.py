from github import Github

def postNewPage(g,name,string,page='Asciify/asciify.github.io'):
    repo = g.get_repo(page)
    response = repo.create_file("{}.html".format(name),name,string)
    return "https://asciify.github.io/{}.html".format(name)
