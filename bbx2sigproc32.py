#!/usr/bin/env python

# Get needed header information for sigproc file format from lofasm files.
import time
from lofasm.bbx import bbx
from lofasm import parse_data as pdat
# These where in Scott's sigproc.py
import os
import struct
import math
import numpy as np
import warnings
from psr_constants import ARCSECTORAD
import sigproc
from filterbank import create_filterbank_file as filMake
import argparse
import gc
# My functions
'''
https://stackoverflow.com/questions/15008758/parsing-boolean-values-with-argparse/36031646

'''
def str2bool(v):
    if isinstance(v, bool):
       return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')


def robustWhitenning(data, mu=10.e3):
    Mu = mu
    data = np.array(data)
    Nr, Nc = data.shape
    result = np.zeros_like(data)
    for i in xrange(Nr):
        result[i,:] = data[i,:] / np.sqrt(abs(data[i,:])**2 + mu**2)
    return result

# Script

parser = argparse.ArgumentParser()
parser.add_argument("-p", "--path", help="Path to input bbx file.", type=str)
parser.add_argument("-w", "--whiten", help="Use Robust Whitenning filter during convert. \
                        Should be a boolean. (True or False)", type=str2bool, default=False)

lowFreq = 25.0
highFreq = 75.0

lowBin = pdat.freq2bin(lowFreq)
highBin = pdat.freq2bin(highFreq)


# Open file to translate
parseDict = vars(parser.parse_args())
inPath = parseDict['path'] # bring out the path from dict to str
print parseDict

print os.path.exists(inPath)
lf = bbx.LofasmFile(inPath)

# Get the file header dictionary
lofasmHeader = lf.header
print lofasmHeader
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
#print "The shape of the data is: {}".format(data.shape)
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

# Stream in Data and Write to disk
rowsToRead = nsamples
spectra = np.zeros((rowsToRead,highBin - lowBin ))
#data = np.zeros((1, highBin - lowBin))
print "number of samples or time bins is " + str(nsamples)
print "The shape of SPECTRA is: {}".format(spectra.shape)
# Getting rid of the otherwise zeros column


for i in range(rowsToRead):
    start_time = time.time()
    lf.read_data(1)
    #print "The shape of data is: {}".format(lf.data.shape)
    spectra = lf.data[:,lowBin:highBin].astype(np.float32)
    spectra = spectra[::-1]
    #spectra = np.reshape(spectra, (1, newHeader['nchans']))
    #print "The shape of SPECTRA is: {}".format(spectra.shape)
    if(parseDict['whiten']):
        spectra = robustWhitenning(spectra)
    fbfile.append_spectra(spectra)
    #print "processed row {}/{} in {}s...{}%".format(i+1, rowsToRead, time.time()-start_time,100*((i+1.0)/rowsToRead))
#    fbfile.append_spectra(lf.data[:][lowBin:highBin][::-1].astype(np.float32))


fbfile.close()
