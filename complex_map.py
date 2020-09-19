#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 18 23:13:36 2020

@author: floriangruen
"""

import matplotlib.pyplot as plt
import numpy as np

plt.figure(figsize=(18,8))
plt.title('Complex mappings')

"""private"""
def convert2d(z):
    return z.real, z.imag

"""private"""
# function to generate the horizontal and vertical lines
def genData(numLines,low,up):
    numPoints = 1000
    x1 = np.linspace(low,up,numPoints)
    data1=[]
    data2 = []
    spacing  = (up-low) / (numLines-1)
    for i in range(numLines):
        y = np.array(numPoints * [low + i*spacing])
        data1.append(np.column_stack((x1,y)))
        data2.append(np.column_stack((y,x1)))
    data1 = np.array(data1)
    data2 = np.array(data2)
    return np.row_stack((data1,data2))

"""private"""
# plotting the domain space
def plotDomain(data,numLines):
    plt.subplot(1,2,1)
    plt.title('Domain')
    plt.xlabel('Re')
    plt.ylabel('Im')
    plt.grid()
    for i in range(numLines):
        plt.scatter(data[i,:,0],data[i,:,1], 0.1,'red')
        plt.scatter(data[i,:,1],data[i,:,0], 0.1,'blue')
    

"""private"""
# evaluating for each point and then plotting the image
def plotRange(data,numLines):
    plt.subplot(1,2,2)
    plt.title('Range')
    plt.xlabel('Re')
    plt.ylabel('Im')
    plt.grid()
    i= 0
    for line in data:
        i +=1
        s=0.1
        color = 'red'     # horizontal lines
        if i >numLines:     # vertical lines
            color = 'blue'
        if line[0][0] == 0:    # imaginary axis
            color = 'yellow'
            s=1
        if line[0][1] == 0:     # real axis
            color = 'green'
            s=1
        output = []
        for point in line:   # evaluate each point
            z = point[0] + point[1]*1j
            w = func1(z)
            u,v = convert2d(w)
            output.append(np.array([u,v]))
        output = np.array(output)
        plt.scatter(output[:,0], output[:,1], s,c=color)
        

# use any function you want, but needs to deal with complex numbers
# and be vectorized.
# be careful with division by zero
def func1(z):
    return z**2

# takes in, number of lines, and up and lower bounds for image
def user(l ,low, up):
    l = l
    data = genData(l,low,up)
    plotDomain(data,l)
    plotRange(data,l)

user(9,-2,2)  # some example









