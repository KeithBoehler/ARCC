'''
Program made to find possible pulsars that were over head in a given LoFASM file. 
This is done by parsing the filename and header of a bbx file for needed information to feed into the ATNF catalog. 

Author: Keith E. Boehler Jr.
Last mod: 3 Jan 2019 
'''
import argparse 
import struct 
from lofasm import parse_data as pdat
from lofasm.bbx import bbx

def filename2dates(bbxHeader, packedStruct):
    # Strip the path to its date parts 
    blankStruckt = struct.unpack('iiiiii', packedStruct)
    dateString = bbxHeader['start_time']
    year = dateString[0:4]
    month = dateString[5:7]
    day = dateString[8:10]
    hour = dateString[11:13]
    minute = dateString[14:16]
    second = dateString[17:-1]
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
bbx_handel = bbx.LofasmFile(bbxFile['path'])
bbxHeader = bbx_handel.header

# Making empty struct.
date411 = struct.pack('iiiiii', 0, 0, 0, 0, 0, 0) # YMD_Hms

# Populate Struct
filename2dates(bbxHeader, date411)


