'''
	Quick script to check the average value of a given bin (inputted by
	 freq or time value. Just a quick sanity check on mods done by 
	other scripts


	Currently a defult radius of 3 is taken to see near by values. 
	No particular reason why 3.
'''

from lofasm.bbx import bbx
import argparse
from lofasm import parse_data

'''
Gather needed user input
''' 
parser = argparse.ArgumentParser()
parser.add_argument("-p", "--path", help="Path to input bbx file. ")
parser.add_argument("-t=", "--time", help="Time in seconds to average. ", type=int, default=None)
parser.add_argument("-f", "--freq", help="Frequancy in MHz to average. ", type=int, default=None)
args_dict = vars(parser.parse_args())
parser.add_argument("-r", "--radius", help="Range to inspect from desired freq. ", type=int, default=3))

time = args_dict['time']
freq = args_dict['freq']
radius = args_dict['radius']

print time
print freq



