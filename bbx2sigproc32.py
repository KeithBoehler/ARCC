'''
To convert lofasm filterbank (bbx) into a PRESTO readable 
sigpproc filter bank. 
'''
# Imports 
import numpy as np
import sys, os
import argparse
# Defining location for presto python scripts. Not using PYTHONPATH because install says not too
sys.path.append(os.environ.get('SCOTTPYTHON'))
import sigproc
from filterbank import create_filterbank_file as filMake

# Definitions 
def bbxFile(v):
    if v[-3:] != "bbx":
        print("Input file is not bbx. ")
        sys,exit(1)

# Options
parser = argparse.ArgumentParser()
parser.add_argument("-p", "--path", help="Path to input bbx file.", type=bbxFile)
#parser.add_argument()

parse_dict = vars(parser.parse_args())

