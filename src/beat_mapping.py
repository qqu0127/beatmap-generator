# -*- coding: utf-8 -*-

'''
@author: Quincy Qu

This document contains beat mapping stuff as the last module in the processing pipeline.
	class beat_mapper
	class parse_beat_map_row
	and testing functions
	
'''

import numpy as np
import madmom
import os
import time
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.ndimage.filters import maximum_filter
from onset_detection import onset_detector
from onset_selection import onset_selector
from state_machine import StateMachine, State
import json
import random

class beat_mapper(object):
	'''
		This class deals with beat mapping, the final step in audio signal processing module.
		Beat_mapper processes the output of onset_selector and generate a json file for visualization module.
		
		The constructor method expect the following variable

		@input:
			time_interval: time interval between two adjacent beats
			num_track: number of tracks to map on, default set to 4
			rand_seed: random seed, default set to 666
	'''
	def __init__(self, time_interval, num_track = 4, rand_seed = 666):
		#self.beat_array = beat_array
		self.time_interval = time_interval
		self.num_track = num_track
		#self.mapped = np.zeros((beat_array.shape[1], num_track), dtype=int)
		self.beat_cnt = 0

		#self.mapping_state_machine = StateMachine(beat_array, num_track)
		#self.setup_state_machine()

		random.seed(rand_seed)

	def setup_state_machine(self, this_state_machine):
		'''
			setup specified state machine with defined state

			name_list is set as default inside the method
			
			@input:
				this_state_machine: the state_machine object to setup
			@output:
				null
		'''
		name_list = ['random', 'stair', 'switch', 'stair_rev']
		for name in name_list:
			this_state_machine.add_state(State.make_state(name))

	def map_to_tracks(self, beat_array):
		'''
			The mapping function that maps the selected beats to specified tracks.
			Update 5/30, mapping with state machine as backend.

			inpelement with state machine, please also see state_machine.py
			
			@input:
				beat_array: 2D np.array with shape (NUM_CHANNEL, TIME_LENGTH)
			@output:
				a ndarray with size (len(sf), num_track)
		'''
		mapped = np.zeros((beat_array.shape[1], self.num_track), dtype=int)
		for channel_beat_array in beat_array:
			mapping_state_machine = StateMachine(channel_beat_array, self.num_track)
			self.setup_state_machine(mapping_state_machine)
			self.beat_cnt += mapping_state_machine.run()

			mapped = np.max((mapped, mapping_state_machine.mapped), axis=0)

		return mapped

	def write_to_json(self, mapped, output = 'mapped.json'):
		'''
			This method writes all the mapping info to a json file, which is everything needed for the Unity module.

			@input:
				mapped, the complete beat map dictory file
				output_path, output folder to store the file.
				file_name, optional, name of the file

			@output:
				null
		'''
		mapped_buf = []
		for row in mapped.tolist():
			par = parse_beat_map_row(row)
			mapped_buf.append(par.get_parse())

		dict = {
				'num_track': self.num_track,
				'time_interval': self.time_interval,
				'beat_cnt': self.beat_cnt,
				'length': len(mapped.tolist()),
				'mapped': mapped_buf
				}
		json_file=json.dumps(dict)

		with open(output, 'w') as f:
			f.write(json_file)
			f.close()


class parse_beat_map_row(object):
	'''
		This class aim to parse a list to a "beats" object at each time point, for beatmap file.
		The input is a list of integer. 
		We use dict() for internal data storage.
		e.g., {"a": 0, "b": 1, "c": 0, "d": 0}

	'''
	def __init__(self, row):
		self.num_track = len(row)
		self.row_dict = dict()
		for num in range(self.num_track):
			self.row_dict[chr(num + ord('a'))] = row[num]

	def __str__(self):
		return str(self.row_dict)
	def get_parse(self):
		return self.row_dict

def test_parse():
	par = parse_beat_map_row([1,3,5,7])
	print(par)

def test():
	# initialize the audio detector and conduct filtering
	detector = onset_detector(2048, 411)
	sf, time_interval = detector.spectralflux('../data/beat_it.mp3', True)
	# initialize onset selector for beat selection
	selector = onset_selector(sf, 10, 3, 3, 0.3, 0.8)
	
	beat_array = selector.find_peaks()

	print("Finish detection and beat selection.")
	print(beat_array.shape)
	start = time.time()
	# start beat mapping, this test case map the beats into 4 tracks
	bm = beat_mapper(time_interval, 4)
	mapped = bm.map_to_tracks(beat_array) # this is the essential method
	print(len(mapped.tolist()))
	print("Finish mapping.")
	print("Running time {} seconds.".format(time.time() - start))

	# now write necessary info to a json file for visualization module
	print("Start writting json file.")
	start = time.time()
	bm.write_to_json(mapped)
	print("Complete.\nRunning time {} seconds.".format(time.time() - start))

	# plot some figures in this test
	for k in range(4):
		plt.figure()
		fig,left_axis=plt.subplots()    
		right_axis = left_axis.twinx()
		p1, = left_axis.plot(sf[0, : 2000])
		p2, = right_axis.plot(mapped[0:2000, k], 'r--')
		right_axis.set_ylim(0, 5)
		plt.savefig("mapped_{}.png".format(k))

if __name__ == '__main__':
	test()
