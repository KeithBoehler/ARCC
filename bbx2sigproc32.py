# Get needed header information for sigproc file format from lofasm files.

from lofasm.bbx import bbx
from lofasm import parse_data as pdat
# These where in Scott's sigproc.py 
import os
import struct
import sys
newpath = ['/home/arcc/Documents/sandbox/presto/lib/python'] #temporary while repo is updated
newpath.extend(sys.path)
sys.path = newpath
import math
import numpy as np
import warnings
from psr_constants import ARCSECTORAD
import sigproc
from filterbank import create_filterbank_file as filMake
import argparse 

parser = argparse.ArgumentParser()
parser.add_argument("-p", "--path", help="Path to input bbx file.")

lowFreq = 25.0
highFreq = 75.0

lowBin = pdat.freq2bin(lowFreq)
highBin = pdat.freq2bin(highFreq)

# Open file to translate 
lofasmFile = vars(parser.parse_args())
inPath = lofasmFile['path'] # bring out the path from dict to str
print lofasmFile
lf = bbx.LofasmFile(inPath)
lf.read_data()
# Get the file header dictionary 
lofasmHeader = lf.header
print lofasmHeader
data = lf.data[:,lowBin:highBin].astype(np.float32) # uncomment 9/27/2018
#data = lf.data[lowBin:highBin, :].astype(np.float32) # uncomment 8/6/2018 # recomment at above uncomment
#data = lf.data.astype(np.float32)
#new filterbank file name
filName = 'newlofasm32.fil'

tstart = float(lofasmHeader['dim1_start'])/86400.0 + 51545.0 # first we convert to days then to the start of J2000
#tsamp = float(lofasmHeader['dim1_span']) / float(lofasmHeader['timebins'])
tsamp = float(lofasmHeader['dim1_span']) / float(lofasmHeader['metadata']['dim1_len']) 
# The change here is that timebins seems to have been renamed.
# There is a dictionary inside a dictionary, so we need those two [][]
nsamples = int(lofasmHeader['metadata']['dim1_len']) # swaped out 'timebins'
print "The value of dim 1 len is: {}".format(nsamples)
rbw = float(lofasmHeader['dim2_span'])*1e-6 / float(lofasmHeader['metadata']['dim2_len']) #resolution bandwith. Changed freqbins to lofasmHeader['metadata']['dim2_len']
print "rbw: {}".format(rbw)
fch1 = highFreq - (rbw/2)
print "The shape of the data is: {}".format(data.shape)
#populate new header
newHeader = {
    'telescope_id': 6, # we are using the number one for now to say we are using AO. 6 for GBT
    'machine_id': 0,
    'data_type': 1,
    'rawdatafile': inPath,
    'tstart': tstart,
    'tsamp': tsamp,
    'nbits': 32,
    'nsamples': nsamples,
    'fch1': fch1,
    'foff': -1* rbw, #descending frequency channels
    'nchans': highBin-lowBin,
    'nifs': 1,
    'source_name': 'keith',
    'Telescope': 'GBT',
    'src_raj' : '033259.368',
    'src_dej' : '543443.57',
    }
print "NEW HEADER"
for k in newHeader.keys():
    print "{}: {}".format(k, newHeader[k])
#write header to filterbank file
fbfile = filMake(filName, newHeader, nbits=32, verbose=True)

for i in range(nsamples):
    spectra = data[i,:][::-1]#spectra = data[:,i][::-1]
    #print "The spectra shape is: {}".format(spectra.shape)
    #spectra = np.reshape(spectra, (1, newHeader['metadata']['dim2_len'])) 
    spectra = np.reshape(spectra, (1, newHeader['nchans']))
    fbfile.append_spectra(spectra)

fbfile.close()


