from PIL import Image, ImageFont, ImageDraw
import requests,io,math

def mapPalette(value,pallette):
    return pallette[int(value/(256/len(pallette)))]

def generate(img,fontPath,pallette = "@#r+=-., ",saveAs = ""):
    red = math.ceil(img.width/150)
    fontSize = 10
    img = img.convert(mode = "L")
    font = ImageFont.truetype(font=fontPath,size=fontSize)
    cellSize = int(font.getsize("A")[1])
    asc = Image.new(mode="L",size=(int(((img.width/red)*cellSize)),int(((img.height/red)*cellSize))),color=255)
    cnv = ImageDraw.Draw(asc)
    img = img.resize((int(img.width/red)+1,int(img.height/red)+1),Image.LANCZOS); 
    mat = [[0 for x in range(img.height)] for y in range(img.width)] 
    for i in range(img.width):
        for j in range(img.height):
            suma=img.getpixel((i,j))
            cnv.text(((i)*cellSize,(j)*cellSize),mapPalette(suma,pallette),font=font,fill="#000000")
            mat[i][j] = mapPalette(suma,pallette)
    if(saveAs != ""):
        asc.save(saveAs)
    return mat

def getImage(url):
    r = requests.get(url)
    img = Image.open(io.BytesIO(r.content))
    return img;    


def matrixToString(mat):
    s = '<link href="style.css" rel="stylesheet" type="text/css"/>\nPage generated with <3 by @AsciifyApp\nIf it does not display correctly, try on a bigger screen (e.g. use your computer)\n\n'
    for j in range(len(mat[0])):
        for i in range(len(mat)):
            s+=mat[i][j]
        s+='\n'
    return s