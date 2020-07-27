from PIL import Image, ImageFont, ImageDraw
import requests,io

def mapPalette(value,pallette):
    return pallette[int(value/(256/len(pallette)))]

def generate(img,red,fontPath,fontSize,pallette = "@#r+=-., ",saveAs = ""):
    img = img.convert(mode = "L")
    font = ImageFont.truetype(font=fontPath,size=fontSize)
    cellSize = int(font.getsize("A")[1])
    asc = Image.new(mode="L",size=(int(((img.width/red)*cellSize)),int(((img.height/red)*cellSize))),color=255)
    cnv = ImageDraw.Draw(asc)
    img = img.resize((int(img.width/red)+1,int(img.height/red)+1),Image.LANCZOS); 
    for i in range(img.width):
        for j in range(img.height):
            suma=img.getpixel((i,j))
            cnv.text(((i)*cellSize,(j)*cellSize),mapPalette(suma,pallette),font=font,fill="#000000")
    if(saveAs != ""):
        asc.save(saveAs)
    return asc

def getImage(url):
    r = requests.get(url)
    img = Image.open(io.BytesIO(r.content))
    return img;    

