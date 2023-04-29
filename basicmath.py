# -*- coding: utf-8 -*-
"""
Created on Mon May 17 14:07:26 2021

@author: rih3d
"""

import numpy as np

def percent(x, minimum, maximum):
    rawrange = maximum - minimum
    xinrawrange = x - minimum
    percent = float(xinrawrange)/rawrange
    return percent



def findmax(data, report):
    currmax = np.max(data)
    if report:
        print('maximum hounsfield unit: '+str(currmax))
    return currmax

def findmin(data, report):
    currmin = np.min(data)
    if report:
        print('minimum hounsfield unit: '+str(currmin))
    return currmin

def findrange(data, report):
    minimum = findmin(data, report)
    maximum = findmax(data, report)
    return minimum, maximum

def putinrange(x, minimum, maximum):
    if x < minimum:
        x = minimum
    elif x > maximum:
        x = maximum
    return x

#multiplier*base^(x*power)
def exponent(x, multiplier, base, power):
    exppower = x*power
    rawexponent = base ** exppower
    result = multiplier * rawexponent
    return result