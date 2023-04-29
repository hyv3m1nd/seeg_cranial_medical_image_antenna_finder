import os
import directories
import nrrd
import numpy as np
from datetime import datetime
import basicmath
import Calculator

air = -850
brain = 20
artifact = 1000
bone = 1800
beads = 3071
calculator = Calculator.Calculator()

basedir = "C:/Users/Imaging/Desktop/CT"
os.chdir(basedir)

targetscan='ct1.nrrd'

function = 'exponent'
exponentbase = 2.718281828467 #x in x^exponentrange
exponentrange = 7 #x in exponentbase^x
specifymin = True #define all voxels with hounsfield unit < specifiedmin as specifiedmin and treat them as the minimum value
specifiedmin = brain
specifymax = False
specifiedmax = bone
maxvoxel = 250
minvoxel = 0
capmethod = 'scale' #options: chop, scale, none
#   chop: calculate the exponent using voxel value, min, and max from the nrrd file, but then chop off anything below minvoxel or above maxvoxel
#   scale: calculate the exponent as a range from minvoxel to maxvoxel
#   none: calculate the exponent using voxel value, min, and max from the nrrd file, with no min or max
#   note: the code defaults to none in the case of a typo
report = True # print the progress

def pickcalculator():
    global calculator
    if function == 'exponent':
        calculator = Calculator.VoxelExponent()

def setparameters(filename, method, exponent):
    global targetscan, capmethod, exponentrange
    targetscan = filename
    capmethod = method
    exponentrange = exponent

def calcvoxel(voxel, datamax, datamin):
    setnewmin = capmethod == 'scale'
    setnewmax = capmethod == 'scale'
    
    x = voxel
    expparameters = (exponentbase, exponentrange)
    localdata = (datamin, datamax)
    choprawmin = (specifymin, specifiedmin)
    choprawmax = (specifymax, specifiedmax)
    setnewmin = (setnewmin, minvoxel)
    setnewmax = (setnewmax, maxvoxel)

    exp = calculator.f(x, expparameters, localdata, choprawmin, choprawmax, setnewmin, setnewmax)
    if capmethod == 'chop':
        exp = basicmath.putinrange(exp, minvoxel, maxvoxel)
    return exp

def calcimage(data, datamax, datamin):
    print("imported data of shape: ", data.shape)
    totalvoxels = data.shape[0] * data.shape[1] * data.shape[2]
    print("Voxels found: ", totalvoxels)
    rows = data.shape[0]
    cols = data.shape[1]
    depth = data.shape[2]
    output_data = np.zeros(data.shape)
    #iterator = 0
    for i in range(0,rows):
        for j in range(0,cols):
            for k in range(0,depth):
                origvoxel = data[i][j][k]
                newvoxel = calcvoxel(origvoxel, datamax, datamin)
                output_data[i][j][k] = newvoxel
    return output_data

def runonce(filename=targetscan, method=capmethod, exponent=exponentrange):
    setparameters(filename, method, exponent)
    filename, extension = directories.process_path(targetscan)
    data, header = directories.loadnrrd(targetscan, report)
    datamin, datamax = basicmath.findrange(data, report)
    
    print('Starting at: ', datetime.now())
    output_data = calcimage(data, datamax, datamin)
    print('Finished at: ', datetime.now())
    directories.savenrrd(filename+'_'+capmethod+'_exp'+str(exponentrange)+'_min'+str(minvoxel)+'_max'+str(maxvoxel)+'.nrrd', output_data, header, report)

pickcalculator()
runonce()