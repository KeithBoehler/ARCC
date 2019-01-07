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

def getStationID(bbxHeader):
    return bbxHeader['station']

def filename2dates(bbxHeader, packedStruct):
    # Strip the path to its date parts 
    blankStruckt = struct.unpack('iiiiif', packedStruct)
    dateString = bbxHeader['start_time']
    year = int(dateString[0:4]) # Year
    month = int(dateString[5:7])# Month
    day = int(dateString[8:10])# Day
    hour = int(dateString[11:13])# Hour
    minute = int(dateString[14:16])# Minute
    second = float(dateString[17:-1])# Seconds
    blankStruct = struct.pack("iiiiii", year, month, day, hour, minute, second)
    return blankStruct # now filled 

# Getting and opening the file we want.
parser = argparse.ArgumentParser()
parser.add_argument("-p", "--path", help="Path to input bbx file")
bbxFile = vars(parser.parse_args()) # This is a one element dict.
bbx_handel = bbx.LofasmFile(bbxFile['path'])
bbxHeader = bbx_handel.header

# Making empty struct.
date411 = struct.pack('iiiiii', 0, 0, 0, 0, 0, 0) # YMD_Hms

# Populate Struct
date411 = filename2dates(bbxHeader, date411)
print struct.unpack("iiiiif", date411)

