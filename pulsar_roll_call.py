'''
Program to open the outputs of 'accelsearch' from presto and write the puslars in
the notes column to a text file.
^^^ <-- Kinda hard so im going to take the column of intrest into a seperate file for now.
Keith E. Boehler Jr.     7 Jan 2019
'''
import argparse 
import numpy

def open_roster(roster_path):
    # Opening file
    roster_file = open(roster_path, 'r')
    print roster_file
    for line in roster_file:
        print line
    roster_file.close()

parser = argparse.ArgumentParser()
parser.add_argument("-p", "--path", help="Path to roster of cands.")
flags_dict = vars(parser.parse_args())
roster_path = flags_dict['path']


