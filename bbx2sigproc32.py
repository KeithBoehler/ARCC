'''
To convert lofasm filterbank (bbx) into a PRESTO readable 
sigpproc filter bank. 
'''
# Imports 
import numpy as np
import sys, os
# Defining location for presto python scripts. Not using PYTHONPATH because install says not too
sys.path.append(os.environ.get('SCOTTPYTHON'))
import sigproc


