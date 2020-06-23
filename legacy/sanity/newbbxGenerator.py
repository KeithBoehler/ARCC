'''
	This was a script that was made to create bbx files from scratch. We had wanted to test presto with some white noise. 
'''

#from lofasm import parse_data as pdat
import numpy as np
from lofasm.bbx import bbx

# Define Inputs
path = "/home/keith/Desktop/testingLOFASM/workspace/WhiteNoiseProject/whiteNoise.bbx"
timeBins = 2 * 3577 #raw_input("Number of time bins? ")
freqBins =  512 #raw_input("Number of frequancy bins? ")
timePhys =  2 * 300 #dim1_span
freqPhys =  50000000#'1000000' #dim2_span
header = {	 
		 'channel': 'AA',
		 'data_label': 'power spectrum (arbitrary)',
 	 	 'data_offset': '0',
		 'data_scale': '1',
		 'data_type': 'real64',
		 'dim1_label': 'time (s)',
		 'dim1_span': timePhys,
		 'dim1_start': '539875099.391',
		 'dim2_label': 'frequency (Hz)',
		 'dim2_span': str(freqPhys),
		 'dim2_start': '25000000.0', # 0.0 orig
		 'frequency_offset_DC': '0 (Hz)',
		 'hdr_type': 'LoFASM-filterbank',
		 'hdr_version': '0000803F',
		 'metadata': {
				'complex': '1',
			        'dim1_len': timeBins, # time bins
			        'dim2_len': freqBins, #''freq bins ''''
			        'encoding': 'raw256',
			        'nbits': 64
			     },
		 'start_time': '2017-02-09T13:18:19.391000Z',
		 'station': '4',
		 'time_offset_J2000': '0 (s)'
}
#gaussNoise = np.random.normal(size = (int(timeBins), int(freqBins)))
gaussNoise = np.random.normal(size = (int(freqBins), int(timeBins)))

# Creating the bbx
lf = bbx.LofasmFile(path, header, mode = 'write')
lf.add_data(gaussNoise)
lf.write()
lf.close()


