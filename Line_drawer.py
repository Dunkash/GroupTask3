from PIL import Image
import numpy as np
from math import floor

class Point:

    def __init__(self, x = 0, y = 0):
        self.X = x
        self.Y = y

def lineBrez(beg,end,img):
    deltX = end.X - beg.X
    deltY = end.Y - beg.Y
    sX = np.sign(deltX)
    sY = np.sign(deltY)

    deltX = abs(deltX)
    deltY = abs(deltY)

    if deltX>deltY:
        pDelX, pDelY = sX, 0
        es, el = deltY,deltX
    else:
        pDelX,pDelY = 0, sY
        es, el = deltX,deltY

    err, t = round(el/2), 0
    img.putpixel((beg.X,beg.Y),(100,100,100,255))

    while (t<el):
        err -= es
        if err < 0:
            err += el
            beg.X += sX
            beg.Y += sY
        else:
            beg.X += pDelX
            beg.Y += pDelY
        t+=1
        img.putpixel((beg.X,beg.Y),(100,100,100,255))

def rfrac(x):
    return 1-(x%1)


def lineVu(beg,end,img):
    if (beg.X>end.X):
        beg.X,end.X = end.X,beg.X
        beg.Y,end.Y = end.Y,beg.Y
    delX = end.X - beg.X
    delY = end.Y - beg.Y
    if ((delX == 0) or (delY == 0)):
        lineBrez(beg,end,img)
        return
    
    mirror = False
    if (abs(delX)<abs(delY)):
        beg.X,beg.Y = beg.Y,beg.X
        end.X,end.Y = end.Y,end.X
        delX,delY = delY,delX
        mirror = True

    grad = delY/delX

    xend = round(beg.X)
    yend = beg.Y + grad * (xend - beg.X)
    xgap = rfrac(beg.X + 0.5)
    xpxl1 = xend
    ypxl1 = floor(yend)
    if (not mirror):
        img.putpixel((xpxl1,ypxl1),(100,100,100,round(255*rfrac(yend)*xgap)))
        img.putpixel((xpxl1,ypxl1+1),(100,100,100,round(255*(yend%1)*xgap)))
    else:
        img.putpixel((ypxl1,xpxl1),(100,100,100,round(255*rfrac(yend)*xgap)))
        img.putpixel((ypxl1+1,xpxl1),(100,100,100,round(255*(yend%1)*xgap)))
    intery = yend + grad

    xend = round(end.X)
    yend = end.Y + grad * (xend - end.X)
    xgap = (end.X + 0.5)%1
    xpxl2 = xend
    ypxl2 = floor(yend)
    if (not mirror):
        img.putpixel((xpxl2,ypxl2),(100,100,100,round(255*rfrac(yend)*xgap)))
        img.putpixel((xpxl2,ypxl2+1),(100,100,100,round(255*(yend%1)*xgap)))
    else:
        img.putpixel((ypxl2,xpxl2),(100,100,100,round(255*rfrac(yend)*xgap)))
        img.putpixel((ypxl2+1,xpxl2),(100,100,100,round(255*(yend%1)*xgap)))
    #img.putpixel((xpxl2,ypxl2),(100,100,100,round(255*rfrac(yend)*xgap)))
    #img.putpixel((xpxl2,ypxl2+1),(100,100,100,round(255*(yend%1)*xgap)))

    if (not mirror):
        for i in range(round(xpxl1),round(xpxl2)):
            img.putpixel((i,floor(intery)),(100,100,100,round(255*rfrac(intery))))
            img.putpixel((i,floor(intery)+1),(100,100,100,round(255 * (intery%1))))
            intery = intery + grad

    else:
        for i in range(round(xpxl1),round(xpxl2)):
            img.putpixel((floor(intery),i),(100,100,100,round(255*rfrac(intery))))
            img.putpixel((floor(intery)+1,i),(100,100,100,round(255 * (intery%1))))
            intery = intery + grad        
        
img = Image.new('RGB', (1000,1000))
img.putalpha(255)
lineVu(Point(100,100),Point(400,800),img)
lineVu(Point(500,500),Point(500,500),img)
lineBrez(Point(100,200),Point(500,201),img)
img.save('test.png')

img.show()
