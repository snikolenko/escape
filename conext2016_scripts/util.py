import time,sys,os
import datetime
import numpy as np
import copy
from collections import Counter
from operator import itemgetter
import more_itertools

## time-wise graph resolution
GRAPH_RESOLUTION = 0.1

def my_print(s):
    print("[" + str(datetime.datetime.now()) + "] " + s)

def parse_trace_filename(fname):
	return (fname.split('/')[-1][:-4], "/".join(fname.split('/')[:-1]), fname[:-4])

def load_lasttimes(fname):
	lasttimes = {}
	with open(fname) as f:
		for line in f:
			arr = line.strip().split()
			lasttimes[(arr[2], arr[3], arr[4])] = float(arr[0])
	return lasttimes

def get_packet(line):
	arr = line.strip().split()
	return (float(arr[0][6:]), (arr[2], arr[4], arr[5]) )

