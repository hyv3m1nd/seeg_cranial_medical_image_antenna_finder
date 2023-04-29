import os
import directories
import nrrd
import numpy as np
from datetime import datetime

basedir =  "D:/Users/rih3d/Documents/ben/fusion"
os.chdir(basedir)

ctname = 'jn_ct.nrrd'
mriname = 't1.nrrd'
targetscan=ctname

air = -850
brain = 20
artifact = 1000
bone = 1800
beads = 3071

exponentrange = 7 #x in exponentbase^x
exponentbase = 2.718281828467 #x in x^exponentrange
maxvoxel = 250
minvoxel = 0
capmethod = 'scale' #options: chop, scale, none
#   chop: calculate the exponent using voxel value, min, and max from the nrrd file, but then chop off anything below minvoxel or above maxvoxel
#   scale: calculate the exponent as a range from minvoxel to maxvoxel
#   none: calculate the exponent using voxel value, min, and max from the nrrd file, with no min or max
#   note: the code defaults to none in the case of a typo
specifymin = True #define all voxels with hounsfield unit < specifiedmin as specifiedmin and treat them as the minimum value
specifiedmin = brain
report = True # print the progress


def setparameters(filename, method, exponent):
    global targetscan, capmethod, exponentrange
    targetscan = filename
    capmethod = method
    exponentrange = exponent

def load(nrrdname):
    #isnrrd = directories.is_format(nrrdname, 'nrrd')
    #if not isnrrd:
    #    raise Exception('unable to process '+nrrdname+': not a nrrd file')
    data, header = nrrd.read(nrrdname)
    if report:
        print('loaded '+nrrdname)
        print('dimensions: %3d x %3d x %3d' % (len(data), len(data[0]), len(data[0][0])))
    return data, header

def save(nrrdname, data, header):
    if report:
        print('saving '+nrrdname)
    nrrd.write(nrrdname, data, header)
    if report:
        print('saved')

def findmax(data):
    currmax = np.max(data)
    if report:
        print('maximum hounsfield unit: '+str(currmax))
    return currmax

def findmin(data):
    currmin = np.min(data)
    if report:
        print('minimum hounsfield unit: '+str(currmin))
    return currmin

def findrange(data):
    maximum = findmax(data)
    minimum = findmin(data)
    return maximum, minimum

def capvoxel(voxel, maximum, minimum):
    if voxel > maximum:
        return maximum
    elif voxel < minimum:
        return minimum
    else:
        return voxel

def percentofmax(voxel, datamax, datamin):
    span = datamax - datamin
    percentofmax = float(voxel-datamin)/span
    return percentofmax

def exponent(percent, maximum, minimum):
    rawexponent = percent - 1
    exp = exponentrange * rawexponent
    multiplier = exponentbase ** exp
    multiplierbase = maximum - minimum
    newval = multiplierbase * multiplier + minimum
    return newval

def calcvoxel(percent, datamax, datamin):
    if capmethod == 'chop':
        exp = exponent(percent, datamax, datamin)
        exp = capvoxel(exp, maxvoxel, minvoxel)
    elif capmethod == 'scale':
        exp = exponent(percent, maxvoxel, minvoxel)
    else:
        exp = exponent(percent, datamax, datamin)
    return exp

def eta(percentprogress, time0):
    timenow = datetime.now()
    timeelapsed = timenow-time0
    timeperprogress = timeelapsed/percentprogress
    remainingprogress = 1.0-percentprogress
    timeremaining = timeperprogress*remainingprogress
    eta = timenow+timeremaining
    return eta

def calcimage(data, datamax, datamin):
    print("imported data of shape: ", data.shape)
    totalvoxels = data.shape[0] * data.shape[1] * data.shape[2]
    print("Voxels found: ", totalvoxels)
    time0 = datetime.now()
    rows = data.shape[0]
    cols = data.shape[1]
    depth = data.shape[2]
    output_data = np.zeros(data.shape)
    #iterator = 0
    for i in range(0,rows):
        for j in range(0,cols):
            for k in range(0,depth):
                origvoxel = data[i][j][k]
                percent = percentofmax(origvoxel, datamax, datamin)
                #this part is used for specifymin
                if percent < 0.0:
                    percent = 0.0
                    origvoxel = specifiedmin
                newvoxel = calcvoxel(percent, datamax, datamin)
                output_data[i][j][k] = newvoxel
    return output_data
               
def runonce(filename=targetscan, method=capmethod, exponent=exponentrange):
    setparameters(filename, method, exponent)
    filename, extension = directories.process_path(targetscan)
    data, header = load(targetscan)
    datamax, datamin = findrange(data)
    if specifymin:
        if datamin < specifiedmin:
            datamin = specifiedmin
    print('Starting at: ', datetime.now())
    output_data = calcimage(data, datamax, datamin)
    print('Finished at: ', datetime.now())
    save(filename+'_'+capmethod+'_exp'+str(exponentrange)+'_min'+str(specifiedmin)+'_max'+str(maxvoxel)+'.nrrd', output_data, header)

runonce()