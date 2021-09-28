from PIL import Image
import numpy as np

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


def lineVu(beg,end,img):
    if (beg.X>end.X):
        beg.X,end.X = end.X,beg.X
        beg.Y,end.Y = end.Y,beg.Y

    delX = end.X - beg.X
    delY = end.Y - beg.Y
    grad = delY/delX

    yend = beg.Y + grad * (round(beg.X) - beg.X)
    xgagp = 1 - ((beg.X + 0.5) - int(beg.X + 0.5))
    xpxl1 = round(beg.X)
    ypxl1 = int(yend)
    img.putpixel((xpxl1,ypxl1),(100,100,100,round(255*(1-(yend-int(yend)))*xgagp)))
    img.putpixel((xpxl1,ypxl1+1),(100,100,100,round(255*(yend-int(yend))*xgagp)))
    intery = yend + grad

    yend = end.Y + grad*(round(end.X) - end.X)
    xgap = (end.X + 0.5) - int(end.X + 0.5)
    xpxl2 = round(end.X)
    ypxl2 = int(yend)
    img.putpixel((xpxl2,ypxl2),(100,100,100,round(255*(1-(yend-int(yend)))*xgap)))
    img.putpixel((xpxl2,ypxl2+1),(100,100,100,round(255*(yend-int(yend))*xgap)))

    for i in range(xpxl1+1,xpxl2):
        img.putpixel((i,int(intery)),(100,100,100,round(255*(1-(intery - int(intery))))))
        img.putpixel((i,int(intery)+1),(100,100,100,round(255 * (intery - int(intery)))))
        intery = intery + grad
        
img = Image.new('RGB', (100,100))
img.putalpha(255)
lineVu(Point(21,10),Point(50,50),img)
lineVu(Point(20,20),Point(40,40),img)

img.show()
