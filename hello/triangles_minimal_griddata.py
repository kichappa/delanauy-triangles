# -*- coding: utf-8 -*-
"""
Created on Tue Sep 15 13:18:31 2020

@author: Kishore S Shenoy

A program to create triangulation that fills up a rectangle with color gradient.
"""

from numpy.random import randint
from numpy import array, sin, cos, pi
from scipy.spatial import Delaunay
from scipy.interpolate import interp2d, griddata

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
    def xyc(self):
        return [self.x, self.y, self.color]
    def xy(self):
        return [self.x, self.y]
    def printPoint(self):
        if self.type:
            print("[ color", self.index, " ] -- ", self.x, ",", self.y, ", color=rgb",self.color, " type=", self.type, " radius=", self.radius, sep="")
        else:
            print("[ color", self.index, " ] -- ", self.x, ",", self.y, ", color=rgb",self.color, " type=", self.type, sep="")

def createRndPoints(num, arr, xmax, ymax):
    for i in range(0, num):
        newPoint = point(i, randint(xmax), 1* randint(ymax))
        arr.append(newPoint)
        
def createRndClrPoints(clrarr, xmax, ymax, maincolors, bgcolors):
    maincolor = randint(len(maincolors)-1)
    thickx = int(xmax/4)
    thicky = int(ymax/4)
    for i in range(0, len(maincolors)):
        newPoint = colorPoint(i, randint(xmax), 1* randint(ymax), maincolors[i], 1, randint(20,30) if (i==maincolor) else randint(5,15))
        clrarr.append(newPoint)
    for i in range(0, len(bgcolors)):
        newPoint = colorPoint(len(maincolors)+i, randint(thickx)+randint(1)*(xmax-thickx), 1*randint(thicky)+randint(1)*(ymax-thicky), bgcolors[i], 0)
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
        svg += " style=\"fill:rgb" + str(colorArray[i]) + "\""
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

def getPointArr(colorPoint, xy, r, g, b, n=4): #n is the number of points
    if colorPoint.type == 0:
        xy.append(colorPoint.xy())
        r.append(colorPoint.color[0])
        g.append(colorPoint.color[1])
        b.append(colorPoint.color[2])
    else:
        for i in range(n):
            xy.append([
                colorPoint.x + cos((2*pi)/n * i), 
                colorPoint.y + sin((2*pi)/n * i)
                ])
            r.append(colorPoint.color[0])
            g.append(colorPoint.color[1])
            b.append(colorPoint.color[2])

def colorPointXYRGB(colorPoints):
    xy= []
    r = []
    g = []
    b = []
    for colorPoint in colorPoints:
        getPointArr(colorPoint, xy, r, g, b)
    # print(xy, r, g, b, sep="\n")
    return xy, [r, g, b]

def triangleColors(triangles, arr, colorPoints):
    centroids = centroidsArray(triangles, arr)
    colorArray = []
    colorXY, colorZ = colorPointXYRGB(colorPoints)
    print("colorXY=", colorXY)
    print("arrayXY=", array(colorXY))
    print("colorZ=", colorZ[0])
    print("arrayZ=", array(colorZ)[0])
    centrX=[]
    centrY=[]
    for centroid in centroids:
        centrX.append(centroid[0])
        centrY.append(centroid[0])
    print((centrX, centrY))
    r = griddata(array(colorXY), array(colorZ)[0], (array(centrX), array(centrY)))
    g = griddata(array(colorXY), array(colorZ)[1], (array(centrX), array(centrY)))
    b = griddata(array(colorXY), array(colorZ)[2], (array(centrX), array(centrY)))
    #print(max(min(int(r(3, 5)[0]), 255),0))
    print(r)
    for i in range(len(centroids)):
        colorArray.append(
                tuple([
                        # max(min(int(r[i]), 255),0),
                        # max(min(int(g[i]), 255),0),
                        # max(min(int(b[i]), 255),0)
                        ])
                )
    return colorArray



arr = []
size = [1080, 1920]
density = 150
createRndPoints(density, arr, size[0], size[1])
createAxisPoints(density, arr, size[0], size[1])
pointsxy = array(pointsAsxy(arr))
colors = [["#ed2e98", "#aa15a4"], ["#f6dab3", "#f6dab3"]]
colorPoints = []
createRndClrPoints(colorPoints, size[0], size[1], maincolors=colors[0], bgcolors=colors[1])
# for x in colorPoints:
#     x.printPoint()
tri = Delaunay(pointsxy)
tri = tri.simplices.copy()
svg = returnSVGTriangles(tri, arr, size[0], size[1], colorPoints)
f = open("image.svg", "w+")
f.write(svg)
#show_svg()



