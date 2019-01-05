'''
Program made to find possible pulsars that were over head in a given LoFASM file. 
This is done by parsing the filename and header of a bbx file for needed information to feed into the ATNF catalog. 

Author: Keith E. Boehler Jr.
Last mod: 3 Jan 2019 
'''
import argparse 
import struct 
from lofasm import parse_data as pdat
import os

def filename2dates(path, packedStruct):
    # Strip the path to its date parts 
    blankStruckt = struct.unpack('iiiiii', packedStruct)
    path = os.path.basename(path)
    year = path[0:4]
    month = path[4:6]
    day = path[6:8]
    hour = path[9:11]
    minute = path[11:13]
    second = path[13:15]
    print "the year is " + year
    print "the month is " + month
    print "the day is " + day
    print "the hour is " + hour
    print "the minute is " + minute
    print "the secound is " + second

# Getting and opening the file we want.
parser = argparse.ArgumentParser()
parser.add_argument("-p", "--path", help="Path to input bbx file")
bbxFile = vars(parser.parse_args()) # This is a one element dict.

# Making empty struct.
date411 = struct.pack('iiiiii', 0, 0, 0, 0, 0, 0) # YMD_Hms

# Populate Struct
filename2dates(bbxFile['path'], date411)


