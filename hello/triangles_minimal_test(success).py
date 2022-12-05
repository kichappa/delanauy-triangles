# -*- coding: utf-8 -*-
"""
Created on Tue Sep 15 13:18:31 2020

@author: Kishore S Shenoy

A program to create triangulation that fills up a rectangle with color gradient.
"""

from numpy.random import randint
from numpy import array, sin, cos, pi
from scipy.spatial import Delaunay
from json import dumps
from scipy.interpolate import SmoothBivariateSpline
import requests
from colour import Color, hex2hsl, hsl2hex, rgb2hex
# from scipy.interpolate import interp2d, SmoothBivariateSpline

#from IPython.display import SVG, display

#def show_svg():
#    display(SVG(url='image.svg'))
#    return (SVG(url='image.svg'))

class point:
    def __init__(self, index, x, y):
        self.index = index
        self.x = x
        self.y = y
    def xy(self):
        return [self.x, self.y]
    def printPoint(self):
        print("[ ", self.index, " ] -- ", self.x, ",", self.y, sep="")
        
class colorPoint:
    def __init__(self, index, x, y, color, point_type, radius=5):
    #def __init__(self, index, x, y, color):#, type, radius=5):
        self.index = index
        self.x = x
        self.y = y
        self.color = hexToRgb(color)
        self.type = point_type #1 for an interior type color point, 0 for a background type color point
        if point_type:
            self.radius = radius
    def xy(self):
        return [self.x, self.y, self.color]
    def printPoint(self):
        if self.type:
            print("[ color", self.index, " ] -- ", self.x, ",", self.y, ", color= ",rgb2hex(rgb=colourToColor(self.color, "rgb", "b")), " type=", self.type, " radius=", self.radius, sep="")
        else:
            print("[ color", self.index, " ] -- ", self.x, ",", self.y, ", color= ",rgb2hex(rgb=colourToColor(self.color, "rgb", "b")), " type=", self.type, sep="")

def createRndPoints(num, arr, xmax, ymax):
    for i in range(0, num):
        newPoint = point(i, randint(xmax), 1* randint(ymax))
        arr.append(newPoint)
        
def createRndClrPoints(clrarr, xmax, ymax, maincolors, bgcolors):
    maincolor = randint(len(maincolors)-1)
    thickx = int(xmax/4)
    thicky = int(ymax/4)
    # print("Length of clr array = ", len(clrarr))
    for i in range(0, len(maincolors)):
        # print("Choosing color #", i, sep="")
        # newPoint = colorPoint(i, randint(int(xmax/6), int(5*xmax/6)), 1* randint(int(ymax/6), int(5*ymax/6)), maincolors[i], 1, randint(25,35) if (i==maincolor) else randint(10,20))
        newPoint = colorPoint(i, randint(xmax), randint(ymax), maincolors[i], 1, randint(25,35) if (i==maincolor) else randint(10,20))        # print("Before while, newPoint=", end="")
        # newPoint.printPoint()
        j=0
        while not checkDist(newPoint, clrarr, 150**2) and j<5:
            # print("Inside while for color #", i, "\n\tnewPoint=", sep="", end="")
            # newPoint.printPoint()
            # print("\tclrarr=", clrarr)
            # j=j+1
            # newPoint = colorPoint(i, randint(int(xmax/6), int(5*xmax/6)), 1* randint(int(ymax/6), int(5*ymax/6)), maincolors[i], 1, randint(25,35) if (i==maincolor) else randint(10,20))
            newPoint = colorPoint(i, randint(xmax), randint(ymax), maincolors[i], 1, randint(25,35) if (i==maincolor) else randint(10,20))
            # isItFar = checkDist(newPoint, clrarr, 100**2)
            # print("isItFar?", isItFar)
        # print("while is over for color #", i, sep="")
        clrarr.append(newPoint)
    for i in range(0, len(bgcolors)):
        # newPoint = colorPoint(len(maincolors)+i, randint(thickx)+randint(2)*(xmax-thickx), 1*randint(thicky)+randint(2)*(ymax-thicky), bgcolors[i], 0)
        newPoint = colorPoint(len(maincolors)+i, randint(xmax), randint(ymax), bgcolors[i], 0)
        j=0
        while not checkDist(newPoint, clrarr, 100**2) and j<5:
            # j=j+1
            # newPoint = colorPoint(len(maincolors)+i, randint(thickx)+randint(2)*(xmax-thickx), 1*randint(thicky)+randint(2)*(ymax-thicky), bgcolors[i], 0)
            newPoint = colorPoint(len(maincolors)+i, randint(xmax), randint(ymax), bgcolors[i], 0)
        clrarr.append(newPoint)
        
def createAxisPoints(num, arr, xmax, ymax):
    num = int(num/7)
    for i in [0,1]:
        for j in [0,1]:
            arr.append(point(len(arr), xmax*i, 1*ymax*j))
            for k in range(randint(num)):
                newPoint = point(len(arr), xmax*j*(1-i)+i*randint(1, xmax-1), 1* (ymax*j*i+(1-i)*randint(1, ymax-1)))
                arr.append(newPoint)
       
        
         
            
def pointsAsxy(arr):
    pointxy = []
    for x in arr:
        pointxy.append(x.xy())
    return pointxy

def hexToRgb(hexcode):
    hexcode = hexcode.lstrip("#")
    return tuple(int(hexcode[i:i+2], 16) for i in (0, 2, 4))

def returnSVGTriangles(triangles, arr, xmax, ymax, colorPoints):
    colorArray = triangleColors(triangles, arr, colorPoints)                               
    svg = """<?xml version="1.0" encoding="utf-8"?>
<svg version="1.1" id="Layer_1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" height=\"""" + str(xmax) +"\" width=\""+ str(ymax)+"\">"

    for i in range(triangles.shape[0]):
        svg += "\n\t<polygon points=\""
        for y in triangles[i,:]:
            svg += str(arr[y].y) + "," + str(arr[y].x) + " "
        svg +="\""
        svg += " style=\"fill:rgb" + str(colorArray[i]) + ";stroke:purple;stroke-width:0\""
        svg +="/>"
    svg += "\n</svg>"
    return svg




def centroid(points):
    x=0
    y=0
    for i in range(3):
        x+=int(points[i].x/3)
        y+=int(points[i].y/3)
    return [x, y]

def centroidsArray(triangles, arr):
    centroids=[]
    for triangle in triangles:
        centroids.append(centroid([arr[triangle[0]],arr[triangle[1]],arr[triangle[2]]]))
    return centroids

def getPointArr(colorPoint, x, y, r, g, b, n=4): #n is the number of points
    if colorPoint.type == 0:
        x.append(colorPoint.x)
        y.append(colorPoint.y)
        r.append(colorPoint.color[0])
        g.append(colorPoint.color[1])
        b.append(colorPoint.color[2])
    else:
        for i in range(n):
            x.append(colorPoint.x + cos((2*pi)/n * i))
            y.append(colorPoint.y + sin((2*pi)/n * i))
            r.append(colorPoint.color[0])
            g.append(colorPoint.color[1])
            b.append(colorPoint.color[2])

def colorPointXYRGB(colorPoints):
    x = []
    y = []
    r = []
    g = []
    b = []
    for colorPoint in colorPoints:
        getPointArr(colorPoint, x, y, r, g, b)
    # print(x, y, r, g, b, sep="\n")
    return array(x), array(y), array([r, g, b])

def triangleColors(triangles, arr, colorPoints):
    centroids = centroidsArray(triangles, arr)
    colorArray = []
    colorX, colorY, colorZ = colorPointXYRGB(colorPoints)
    r = SmoothBivariateSpline(colorX, colorY, colorZ[0], kx=2, ky=2)
    g = SmoothBivariateSpline(colorX, colorY, colorZ[1], kx=2, ky=2)
    b = SmoothBivariateSpline(colorX, colorY, colorZ[2], kx=2, ky=2)
    # print(max(min(int(r(3, 5)[0]), 255),0))
    for centroid in centroids:
        colorArray.append(
                tuple([
                        max(min(int(r(centroid[0],centroid[1])[0]), 255),0),
                        max(min(int(g(centroid[0],centroid[1])[0]), 255),0),
                        max(min(int(b(centroid[0],centroid[1])[0]), 255),0)
                        ])
                )
    return colorArray

def checkDist(newPoint, otherPoints, minDistSq):
    if len(otherPoints)==0:
        # print("checkDist(): Color array is empty, so returning 1")
        return 1
    dx = (otherPoints[0].x - newPoint.x)
    dy = (otherPoints[0].y - newPoint.y)
    distanceSq=(dx * dx + dy * dy)
    for otherPoint in otherPoints:
        dx = (otherPoint.x - newPoint.x)
        dy = (otherPoint.y - newPoint.y)
        distanceSq=(dx * dx + dy * dy)
        if minDistSq > distanceSq:
            print("checkDist(): Minimum distance sq=", minDistSq, " not met, distance sq=", distanceSq, ". Hence passing 0", sep="")
            return 0    
    print("checkDist(): Minimum distance sq=", minDistSq, " met and distance sq=", distanceSq, ". Passing 1", sep="")
    return 1

def colourToColor(colorCode, mode, direction):
    if direction=="f":
        if mode=="rgb":
            return [int(colorCode[0]*256), int(colorCode[1]*256), int(colorCode[2]*256)]
        elif mode=="hsl":
            return [int(colorCode[0]*360), int(colorCode[1]*100), int(colorCode[2]*100)]
    elif direction=="b":
        if mode=="rgb":
            return (colorCode[0]/256, colorCode[1]/256, colorCode[2]/256)
        elif mode=="hsl":
            return (colorCode[0]/360, colorCode[1]/100, colorCode[2]/100)


arr = []
size = [1080, 1920]
density = 150
createRndPoints(density, arr, size[0], size[1])
createAxisPoints(density, arr, size[0], size[1])
pointsxy = array(pointsAsxy(arr))
color1=Color(hsl=(
    randint(0, 360)/360, 
    randint(65, 75)/100, 
    randint(35, 50)/100)
    )
color2=Color(hsl=( 
    (int(color1.hsl[0]*360)+[-1,1][randint(2)]*(randint(25)+45))/360,
    randint(65, 75)/100, 
    randint(35, 50)/100)
    )

color3=Color(hsl=(
    (color1.hsl[0]+color2.hsl[0])/2+0.5,
    randint(25, 35)/100, 
    randint(60, 75)/100)
    )

# url = "http://colormind.io/api/"
# print(color1.hex, color2.hex)
# data = {
# 	"model" : "default",
# 	"input" : [colourToColor(color1.rgb, "rgb", "f"), colourToColor(color2.rgb, "rgb", "f"), "N"]
# }
# # data = {"model" : "default","input" : [[155, 216, 226], "N"]}

# print("data=",data,"\ndumps(data)=", dumps(data), sep="")
# colormind = requests.post(url, data=dumps(data))
# print(colormind.text)

colors = [[color1.hex, color2.hex], [color3.hex, color3.hex]]
colorPoints = []
createRndClrPoints(colorPoints, size[0], size[1], maincolors=colors[0], bgcolors=colors[1])
for x in colorPoints:
    x.printPoint()
tri = Delaunay(pointsxy)
tri = tri.simplices.copy()
svg = returnSVGTriangles(tri, arr, size[0], size[1], colorPoints)
f = open("image.svg", "w+")
f.write(svg)
# print(type(rgb2hex(rgb=(205, 44, 29))))
#show_svg()



