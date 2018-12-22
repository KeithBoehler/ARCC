''' By Keith Boehler, 06/25/2018, bbxChannelMod

	The onjective of the program is to proform manipulations to specific frequancy bands. 
	We will start out by selecting a channel and applying a running median. 
'''
# set imports 
from lofasm.bbx import bbx
from lofasm import parse_data as pdat
import numpy as np
import os
import argparse

# Set the parser stuff
parser = argparse.ArgumentParser()
parser.add_argument("-p","--path", help="Path to input bbx file.")
parser.add_argument("-f", "--freq", help="Set frequancy channel to be removed. In MHz.")
parser.add_argument("-o", "--outfile", help="Name for file created.")

#Open the file we want to mod
pars_dict = vars(parser.parse_args())
bbxfile = pars_dict['path']
bbxFileHandel  = bbx.LofasmFile(bbxfile)
bbxFileHandel.read_data()
data = bbxFileHandel.data[:, :].astype(np.float32)
bbxFileHeader = bbxFileHandel.header

# select frequancy to zero 
userin = float(pars_dict['freq'])
freqbin = pdat.freq2bin(userin)

# zero out that frequancy
data[:, freqbin] = 0

# write to new bbx file
path = os.getcwd()
path = path + '/' + pars_dict['outfile']
outFile = bbx.LofasmFile(path, bbxFileHeader, mode = 'write')
outFile.add_data(data)
outFile.write()
outFile.close()
