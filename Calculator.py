# -*- coding: utf-8 -*-
"""
Created on Mon May 17 13:22:22 2021

@author: rih3d
"""

import basicmath

class Calculator:
    def __init__(self):
        pass
    
    #x = target in f(x)
    #argv = a list of parameters
    def f(self, x, *argv):
        return x

class VoxelExponent(Calculator):
    def __init__(self):
        super().__init__()

    #argv[0] = (exponentbase (float), exponentrange (float))      
    #argv[1] = (datalocalmin (int), datalocalmax(int))
    #argv[2] = (setlocalmin (boolean), definedlocalmin (int))
    #argv[3] = (setlocalmax (boolean), definedlocalmax (int))
    #argv[4] = (setnewmin (boolean), definednewmin (int))
    #argv[5] = (setnewmax (boolean), definednewmax (int))
    def f(self, x, *argv):
        if len(argv) < 6:
            raise Exception('not enough parameters to run VoxelExponent')
        #extracting variables
        (exponentbase, exponentrange) = argv[0]
        (datalocalmin, datalocalmax) = argv[1]
        (setlocalmin, definedlocalmin)= argv[2]
        (setlocalmax, definedlocalmax) = argv[3]
        (setnewmin, definednewmin) = argv[4]
        (setnewmax, definednewmax) = argv[5]
        
        if setlocalmin:
            datalocalmin = definedlocalmin
        if setlocalmax:
            datalocalmax = definedlocalmax
        x = basicmath.putinrange(x, datalocalmin, datalocalmax)
        if not setnewmin:
            definednewmin = definedlocalmin
        if not setnewmax:
            definednewmax = definedlocalmax
        
        xpercent = basicmath.percent(x, datalocalmin, datalocalmax)
        rawexponent = xpercent - 1
        resultrange = definednewmax - definednewmin
        exp = basicmath.exponent(rawexponent, resultrange, exponentbase, exponentrange)
        expinrange = exp + definednewmin
        
        return expinrange

"""
def test():
    x = 3
    localmin = -1500
    localmax = 3000
    exponentbase = 10
    exponentrange = 6.5
    setlocalmin = True
    definedlocalmin = 50
    setlocalmax = False
    definedlocalmax = 30
    setnewmin = True
    definednewmin = 0
    setnewmax = True
    definednewmax = 1000
    
    func = VoxelExponent()
    result = func.f(x, (exponentbase, exponentrange), (localmin, localmax), (setlocalmin, definedlocalmin), (setlocalmax, definedlocalmax), (setnewmin, definednewmin), (setnewmax, definednewmax))
    print(result)

test()
"""