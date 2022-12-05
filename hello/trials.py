# -*- coding: utf-8 -*-
"""
Created on Sat Sep 12 17:39:47 2020

@author: Kishore S Shenoy

A program to create triangle mesh grid that fills up a rectangle.

"""
#Importing matplotlib as 'plt'
import matplotlib.pyplot as plt
import matplotlib.lines as lines
from numpy.random import randint
from numpy import array
from scipy.spatial import Delaunay
from scipy.interpolate import interp2d
"""
#Defining a figure
fig = plt.figure()

#Difining a subplot in fig element
ax = fig.add_subplot(111)

#Creating an array of x's and y's
x_points = range(0,100)
y_points = range(0,100)

p = ax.plot(x_points, y_points, 'o')

#Definihg the range of axes, labels and figure title
ax.axis([0, 6, 0, 20])
#ax.set_xlabel('x-points')
#ax.set_ylabel('y-points')
#ax.set_title('Simple XY point plot')

#Showing the figure
fig.show()
"""


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
    def __init__(self, index, x, y, color):
        self.index = index
        self.x = x
        self.y = y
        self.color = hexToRgb(color)
    def xy(self):
        return [self.x, self.y, self.color]
    def printPoint(self):
        print("[ color", self.index, " ] -- ", self.x, ",", self.y, ", color=rgb",self.color, sep="")

class pointPair:
    def __init__(self, point1, point2, distance):
        self.point1 = point1
        self.point2 = point2
        self.distance = distance
        
    def getxx(self):
        return [self.point1.x, self.point2.x]
    
    def getyy(self):
        return [self.point1.y, self.point2.y]
        
def createRndPoints(num, arr, xmax, ymax):
    for i in range(0, num):
        newPoint = point(i, randint(xmax), 1* randint(ymax))
        arr.append(newPoint)
        
def createRndClrPoints(colors, clrarr, xmax, ymax):
    for i in range(0, len(colors)):
        newPoint = colorPoint(i, randint(xmax), 1* randint(ymax), colors[i])
        clrarr.append(newPoint)
        
def createAxisPoints(num, arr, xmax, ymax):
    num = int(num/7)
    for i in [0,1]:
        for j in [0,1]:
            arr.append(point(len(arr), xmax*i, 1*ymax*j))
            for k in range(randint(int(num))):
                newPoint = point(len(arr), xmax*j*(1-i)+i*randint(1, xmax-1), 1* (ymax*j*i+(1-i)*randint(1, ymax-1)))
                arr.append(newPoint)
                #newPoint.printPoint()
    





def showPoints(points, fig = plt.figure(), show=1):
    xcor = []
    ycor = []
    max_xcor = 0
    max_ycor = 0
    for point in points:
        if point.x > max_xcor : max_xcor = point.x
        if point.y > max_ycor : max_ycor = point.y
        xcor.append(point.x)
        ycor.append(point.y)
    ax = fig.add_subplot(111)
    ax.plot(xcor, ycor, 'o')
    #ax.axis([0, (int(max_xcor / 10) + 1) * 10, 0, (int(max_ycor / 10) + 1) * 10])
    if show : fig.show()

def showPair(pointPairs, fig = plt.figure(), show=1):
    ax = plt.gca()
    ax.add_line(lines.Line2D(pointPairs.getxx(), pointPairs.getyy()))
    if show : fig.show()
    
def showPlot(*args, fig = plt.figure(), show=1):
    for x in args:
        if x is list and len[x] > 0:
            if isinstance(x[0], point): showPoints(x, fig, 0)
        elif isinstance(x, pointPair): showPair(x, fig, 0)
    if show : fig.show()
    
def printPoints(points):
    for point in points:
        point.printPoint()

def pointsAsxy(arr):
    pointxy = []
    for x in arr:
        pointxy.append(x.xy())
    return pointxy

def returnCor(arr, cordinate):
    cordinates = []
    for element in arr:
        cordinates.append(element.x) if cordinate == "x" else cordinates.append(element.y)
    return cordinates

def generateShade(color, bound):
    color = color.lstrip('#')
    rgb = list(int(color[i:i+2], 16) for i in (0, 2, 4))
    for i in range(3):
        rgb[i] = int(rgb[i] * (1 + (randint(2*bound) - bound)/100))
    return ("rgb"+str(tuple(rgb)))

def hexToRgb(hexcode):
    hexcode = hexcode.lstrip("#")
    return tuple(int(hexcode[i:i+2], 16) for i in (0, 2, 4))

def returnSVGTriangles(triangles, arr, xmax, ymax, colorPoints):
    #base_color = base_color.lstrip('#')
    
    colorArray = triangleColors(triangles, arr, colorPoints)                               
    svg = """<?xml version="1.0" encoding="utf-8"?>
<svg version="1.1" id="Layer_1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" height=\"""" + str(xmax) +"\" width=\""+ str(ymax)+"\">"

    #svg += "\n\t<style type=\"text/css\">\n"  
    #for i in range(colors):
    #    svg+= "\t\t.st" + str(i) + "{fill:"+ generateShade(base_color, 30)+";}\n"
    #svg += "\t</style>"
    #print(triangles.shape[0])
    #print(triangles[133,:])
    for i in range(triangles.shape[0]):
        #i = triangles.index(x)
        #print(triangles[i,:])
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

def colorPointXYRGB(colorPoints):
    x = []
    y = []
    r = []
    g = []
    b = []
    for colorPoint in colorPoints:
        x.append(colorPoint.x)
        y.append(colorPoint.y)
        r.append(colorPoint.color[0])
        g.append(colorPoint.color[1])
        b.append(colorPoint.color[2])
    return x, y, [r, g, b]

def triangleColors(triangles, arr, colorPoints):
    centroids = centroidsArray(triangles, arr)
    colorArray = []
    colorX, colorY, colorZ = colorPointXYRGB(colorPoints)
    r = interp2d(colorX, colorY, colorZ[0])
    g = interp2d(colorX, colorY, colorZ[1])
    b = interp2d(colorX, colorY, colorZ[2])
    print(max(min(int(r(3, 5)[0]), 255),0))
    for centroid in centroids:
        colorArray.append(
                tuple([
                        max(min(int(r(centroid[0],centroid[1])[0]), 255),0),
                        max(min(int(g(centroid[0],centroid[1])[0]), 255),0),
                        max(min(int(b(centroid[0],centroid[1])[0]), 255),0)
                        ])
                )
    return colorArray

def distancePoints(p1, p2):
    dx = (p1.x - p2.x)
    dy = (p1.y - p2.y)
    return (dx * dx + dy * dy)
    
def findClosestPair(points):
    return 0

#merge sort points
def sortPoints(arr, criteria):
    #b = [point(-1, 0, 0)] * len(arr)
    b = arr.copy()
    #segment size
    ss = 1
    while ss < len(arr):
        mergePass (arr, b, ss, criteria)
        ss += ss
        mergePass (b, arr, ss, criteria)
        ss += ss
        
def mergePass(x, y, ss, criteria):
    i = 0
    ss2 = 2 * ss
    while i < (len(x) - ss2):
        merge(x, y, i, i + ss - 1, i + ss2 - 1, criteria)
        i += ss2
    if (i + ss) < len(x):
        merge(x, y, i, i + ss - 1, len(x) - 1, criteria)
    else:
        for j in range(i, len(x)):
            y[j] = x[j]

#sof - start of first, eof - end of first, eos - end of second 
def merge(c, d, sof, eof, eos, criteria):
    first = sof
    second = eof + 1
    result = sof
    while ((first <= eof) and (second <= eos)):
        condition = (c[first].x <= c[second].x if (criteria == "x") else c[first].y <= c[second].y)
        if condition:
            d[result] = c[first]
            first += 1
        else:
            d[result] = c[second]
            second += 1
        result += 1
    if first > eof:
        for j in range(second, eos + 1):
            d[result] = c[j]
            result += 1
    else:
        for j in range(first, eof + 1): 
            d[result] = c[j]
            result += 1
            
def closestPair(x):
    if len(x) < 2:
        return arr
    sortPoints(x, "x")
    y = x.copy()
    sortPoints(y, "y")
    z = x.copy()
    return closestPairs(x, y, z, 0, len(x) - 1)

def closestPairs(x, y, z, l, r):
    if r - l == 1: #only two points
        return pointPair(x[l], x[r], distancePoints(x[l], x[r]))
    
    if r - l == 2: #three points
        d1 = distancePoints(x[l], x[l+1])
        d2 = distancePoints(x[l+1], x[r])
        d3 = distancePoints(x[l], x[r])
        if d1 <= d2 and d1 <= d3:
            return pointPair(x[l], x[l+1], d1)
        if d2 < d3:
            return pointPair(x[l+1], x[r], d2)
        else:
            return pointPair(x[l], x[r], d3)
    
    #more than 3 points; divide into 2
    m = int((l + r) / 2 )#x[l:m] in A, rest in B
    
    #create sorted-by-y lists in z[l:m] & z[m+1:r]
    f = l
    g = m + 1
    for i in range(l, r + 1):
        if y[i].index > m:
            z[g] = y[i]
            g += 1
        else:
            z[f] = y[i]
            f += 1
    #solve the two parts
    best = closestPairs(x, z, y, l, m)
    right = closestPairs(x, z, y, m+1, r)
    
    #make best closest pair
    if(right.distance < best.distance):
        best = right
    
    merge(z, y, l, m, r, "y")
    k = l
    for i in range(l, r+1):
        if pow(x[m].x - y[i].x, 2) < best.distance:
            z[k] = y[i]
            k += 1
    #search for closer category 3 pair
    for i in range(l, k):
        for j in range(i+1, k):
            if(z[j].y - z[i].y < best.distance):
                dp = distancePoints(z[i], z[j])
                if dp < best.distance:
                    best = pointPair(x[z[i].index], x[z[j].index], dp)
            else: break
    return best

arr = []
"""
point( 0,31,79)
point( 1,63,20)
point( 2,53,66)
point( 3,9,41)
arr = [point(0, 63,20),point(1,31,79), point( 2,53,66),point( 3,9,41)]
"""

size = [1080, 1920]
density = 60
fig = plt.figure()
#fig.add_subplot(111).axis([0, size[0], 0, size[1]])
fig.add_subplot(111).axis([0, 1920, 0, 1920])
createRndPoints(density, arr, size[0], size[1])
createAxisPoints(density, arr, size[0], size[1])
#rgb = tuple(int("603189"[i:i+2], 16) for i in (0, 2, 4))
#print(rgb)
#color = "#603189"
#for i in range(5):
#    print(generateShade(color, 5))
#printPoints(arr)
#newarr = arr
#showPoints(arr, fig, show=1)
#closest = closestPair(arr.copy())
#print(closest.getxx(), closest.getyy())
pointsxy = array(pointsAsxy(arr))
#print("Points XY:")
#print(pointsxy)
#print("Points [:,0]:")
#print(pointsxy[:,0])
#print("Points [:,1]:")
#print(pointsxy[:,1])

#print (svg)

                         
colors = ["#ed2e98", "#aa15a4", "#f6dab3"]
colorPoints = []
createRndClrPoints(colors, colorPoints, size[0], size[1])

for x in colorPoints:
    x.printPoint()
    
tri = Delaunay(pointsxy)
triangles = tri.simplices.copy()

#print(triangles)
#print(triangles[2,:])

#for x in range(triangles.size):
#    print(triangles[:,x])

svg = returnSVGTriangles(triangles, arr, size[0], size[1], colorPoints)
#print(centroidsArray(triangles, arr))
f = open("image.svg", "w+")
f.write(svg)
#print(triangles)
plt.triplot(pointsxy[:,0], pointsxy[:,1], triangles)
plt.plot(pointsxy[:,0], pointsxy[:,1], 'o')
plt.show()
#showPlot(arr, closest, fig=fig, show=1)
#fig.show()
#printPoints(newarr)
#showPoints(newarr)



    















