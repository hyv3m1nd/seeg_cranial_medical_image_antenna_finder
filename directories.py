# -*- coding: utf-8 -*-
"""
Created on Wed May 12 14:52:57 2021

@author: Ben Hsieh
"""

import os
import nrrd

def check_dir(path):
    path_exists = os.path.exists(path)
    if not path_exists:
        os.makedirs(path)

#turns a path into filename and extension
def process_path(case_path):
    full_name = case_path.split('\\')[-1]
    extension = full_name.split('.')[-1]
    isfolder = full_name == extension
    if isfolder:
        return full_name, 'folder'
    name_length = len(full_name)-len(extension)-1
    filename = full_name[0:name_length]
    return filename, extension

def is_format(case_path, extension):
    name, ext = process_path(case_path)
    return ext == extension

def loadnrrd(nrrdname, report):
    #isnrrd = directories.is_format(nrrdname, 'nrrd')
    #if not isnrrd:
    #    raise Exception('unable to process '+nrrdname+': not a nrrd file')
    data, header = nrrd.read(nrrdname)
    if report:
        print('loaded '+nrrdname)
        print('dimensions: %3d x %3d x %3d' % (len(data), len(data[0]), len(data[0][0])))
    return data, header

def savenrrd(nrrdname, data, header, report):
    nrrd.write(nrrdname, data, header)
    if report:
        print('saved as '+nrrdname)
