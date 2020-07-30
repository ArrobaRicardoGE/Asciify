from github import Github

def postNewPage(g,name,string,page='ArrobaRicardoGE/arrobaricardoge.github.io'):
    repo = g.get_repo(page)
    response = repo.create_file("asciify/{}.html".format(name),name,string)
    return "https://arrobaricardoge.github.io/asciify/{}.html".format(name)
