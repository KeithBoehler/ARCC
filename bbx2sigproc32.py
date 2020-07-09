'''
To convert lofasm filterbank (bbx) into a PRESTO readable 
sigpproc filter bank.
Python 3.7 version
'''
# Imports 
import numpy as np
import sys, os
import argparse
from lofasm import parse_data as pdat
from lofasm.bbx import bbx
# Defining location for presto python scripts. Not using PYTHONPATH because install says not too
sys.path.append(os.environ.get('SCOTTPYTHON'))
import sigproc
from filterbank import create_filterbank_file as filMake

# Definitions 
'''
Intent : Verify input files are of bbx format
'''
def bbxFile(v):
    if v[-3:] != "bbx":
        print("Input file is not bbx. ")
        sys.exit(1)
    return v
'''
Intent : Find the coresponding bin for the input frequencies in MHz
'''
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
'''
Intent : With the prospect of feeding multiple bbx files to argparse each output file will need its own header, thus needs to be called multiple times. 
Preconditions : The existance of a LoFASM BBX file
Postcondition : A sigproc header file that is consistant this link, http://sigproc.sourceforge.net/sigproc.pdf
Issues : Perhaps instead pass in the args dictionary to reduce u_freq and in_path params to one.
'''
def prepHeader(bbx_hdr, u_bin, l_bin, u_freq, in_path):
    t_start = (float(bbx_hdr['dim1_start']) / 86400.0) + 51545.0 # first convert to days, then add the MDJ offset.
    t_samp = float(bbx_hdr['dim1_span']) / float(bbx_hdr['metadata']['dim1_len'])
    num_samples = int(bbx_hdr['metadata']['dim1_len'])
    resolution_bandwidth = float(bbx_hdr['dim2_span'])*1e-6 / float(bbx_hdr['metadata']['dim2_len'])
    freq_channel1 = u_freq - (resolution_bandwidth / 2)
    sig_header = {
            'telescope_id': 6, # 6 = GBT; 1 = AO
            'machine_id': 0,
            'data_type': 1,
            'rawdatafile': in_path,
            'tstart': t_start,
            'tsamp': t_samp,
            'nbits': 32,
            'fch1': freq_channel1,
            'foff': -1 * resolution_bandwidth, # Decending Freq Channels
            'nchans': u_bin - l_bin,
            'nifs': 1,
            'source_name': 'LoFASM',
            'Telescope' : str(bbx_hdr['station']),
            'src_raj' : '033259.368',
            'src_dej' : '543443.57',
            }
    return sig_header
'''
Intent : This will be the for loop in the python 2 version. Made a function so that it can be called for multiple input bbx. 
'''
def fbTranscribe(parse_dict, bbx_hdr, sig_hdr, upper_bin, lower_bin, lf_obj):
    leaf = os.path.basename(parse_dict["path"]) 
    out_file = os.path.splitext(leaf)[0] + ".fil"
    fb_file = filMake(out_file, sig_hdr, nbits=32, verbose=True)
    print("Output file name ", out_file)
    spectra = np.zeros((bbx_hdr['metadata']['dim1_len'], upper_bin - lower_bin))
    for i in range(int(bbx_hdr['metadata']['dim1_len'])):
        lf_obj.read_data(1)
        spectra = lf.data[:,lower_bin:upper_bin].astype(np.float32)
        spectra = spectra[::-1]
        fb_file.append_spectra(spectra)
    fb_file.close()

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
new_header = prepHeader(lf.header, upper_bin, lower_bin, parse_dict["upper_freq"], parse_dict["path"])

# Some extra 411 
if parse_dict["verbose"]:
    print("Low Freq ", parse_dict["lower_freq"], "MHz is now bin: ", str(lower_bin))
    print("High Freq ", parse_dict["upper_freq"], "MHz is now bin: ", str(upper_bin))
    print("Input bbx: ", parse_dict["path"])
    print(new_header)

fbTranscribe(parse_dict,lf.header, new_header, upper_bin, lower_bin, lf)
