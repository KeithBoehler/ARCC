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

'''
Stream Data. Open the file we want to mod. 
Prep the file we are to write too.
'''
pars_dict = vars(parser.parse_args())
bbxFileHandel = bbx.LofasmFile(pars_dict['path'])
bbxfile = pars_dict['path']

bbxFileHeader = bbxFileHandel.header
outPath = os.getcwd()
outPath = outPath + '/' + pars_dict['outfile']

for i in range(int(bbxFileHeader['metadata']['dim1_len'])):
    bbxFileHandel.read_data(1) # Read one line of data
    spectra = bbxFileHandel.data[:, :] #.astype(np.float32)
    spectra[:,pdat.freq2bin(float(pars_dict['freq']))] = 0
    outFile = bbx.LofasmFile(outPath, bbxFileHeader, mode = 'write')
    outFile.add_data(spectra)
    outFile.write()    

outFile.write()
'''
data = bbxFileHandel.data[:, :].astype(np.float32)

# select frequancy to zero 
userin = float(pars_dict['freq'])
freqbin = pdat.freq2bin(userin)

# zero out that frequancy
data[:, freqbin] = 0
'''
'''
# write to new bbx file
path = os.getcwd()
path = path + '/' + pars_dict['outfile']
outFile = bbx.LofasmFile(path, bbxFileHeader, mode = 'write')
outFile.add_data(data)
outFile.write()
outFile.close()

'''
