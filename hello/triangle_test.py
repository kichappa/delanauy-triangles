# -*- coding: utf-8 -*-
"""
Created on Wed Sep 16 14:14:08 2020

@author: Kishore S Shenoy
"""

from math import pi
from numpy import array, cos, sin

theta = array(range(4)) *pi/2
r = 10
cords = array([list(r * cos(theta)), list(r*sin(theta))]).transpose()
newcords=[]
for x in cords:
    newcords.append([x[0], x[1]])
        
#print(theta)
#print(cords)
#print(newcords)

randint(int(1920/4))+randint(1)*(1920-int(1920/4))