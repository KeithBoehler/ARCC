'''
To convert lofasm filterbank (bbx) into a PRESTO readable 
sigpproc filter bank. 
'''
# Imports 
import numpy as np
import sys, os, time
import argparse
from lofasm import parse_data as pdat
from lofasm.bbx import bbx
# Defining location for presto python scripts. Not using PYTHONPATH because install says not too
sys.path.append(os.environ.get('SCOTTPYTHON'))
import sigproc
from filterbank import create_filterbank_file as filMake

# Definitions 
def bbxFile(v):
    if v[-3:] != "bbx":
        print("Input file is not bbx. ")
        sys.exit(1)
    return v

def boundarySet(p_dict):
    lower_freq = parse_dict["lower_freq"]
    upper_freq = parse_dict["upper_freq"]
    lower_bin = 0
    upper_bin = 0
    if lower_freq < upper_freq:
        lower_bin = pdat.freq2bin(lower_freq)
        upper_bin = pdat.freq2bin(upper_freq)
    elif lower_freq == uppe_freq:
        print("Frequency boundry cannot be equal.")
        sys.exit(1)
    else:
        print("Upper and lower entered under wrong flag... Do it right!")
        lower_bin = pdat.freq2bin(upper_freq)
        upper_bin = pdat.freq2bin(lower_freq)
        lower_freq = parse_dict["lower_freq"]
    
    return lower_bin, upper_bin

# Options
parser = argparse.ArgumentParser()
parser.add_argument("-p", "--path", help="Path to input bbx file.", type=bbxFile)
parser.add_argument("-l", "--lower-freq", help="Enter the lower bound frequency in MHz. default=25.0", type=float, default=25.0)
parser.add_argument("-u", "--upper-freq", help="Enter the upper bound frequency in MHz. default=75.0", type=float, default=75.0)
parser.add_argument("-v", "--verbose", help="Some extra prints", action="store_true")
parse_dict = vars(parser.parse_args())

lf = bbx.LofasmFile(parse_dict["path"])
# Setting and checking boundary conditions, lower first, upper seccond
lower_bin, upper_bin = boundarySet(parse_dict)
if parse_dict["verbose"]:
    print("Low Freq ", parse_dict["lower_freq"], "MHz is now bin: ", str(lower_bin))
    print("High Freq ", parse_dict["upper_freq"], "MHz is now bin: ", str(upper_bin))
    print("Input bbx: ", parse_dict["path"])
    print(lf.header)

