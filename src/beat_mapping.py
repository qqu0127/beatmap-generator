# -*- coding: utf-8 -*-

'''
@author: Quincy Qu
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
import json
import random

class beat_mapper(object):
	'''
		This class deals with beat mapping, the final step in audio signal processing module.
		Beat_mapper processes the output of onset_selector and generate a json file for visualization module.

	'''
	def __init__(self, sf, quantified, time_interval, num_track = 4, rand_seed = 666):
		self.sf = sf
		self.quantified = quantified
		self.time_interval = time_interval
		self.num_track = num_track
		self.mapped = np.zeros((len(quantified), num_track), dtype=int)
		self.beat_cnt = 0
		random.seed(rand_seed)

	def map_to_tracks(self):
		'''
			The mapping function that maps the selected beats to specified tracks.

			@output:
				a ndarray with size (len(sf), num_track)
		'''
		cnt = 0
		for i in self.quantified:
			if(i == 1):
				k = random.randint(0, self.num_track - 1)
				self.mapped[cnt][k] = 1
				self.beat_cnt += 1
			cnt += 1
		return self.mapped

	def write_to_json(self, output_path, file_name = 'mapped.json'):
		'''
			This method writes all the mapping info to a json file, which is everything needed for the Unity module.

			@input:
				output_file, output folder to store the file.
				file_name, optional, name of the file

			@output:
				null
		'''
		dict = {
				'num_track': self.num_track,
				'time_interval': self.time_interval,
				'beat_cnt': self.beat_cnt,
				'mapped': self.mapped.tolist()
				}
		json_file=json.dumps(dict)

		with open(os.path.join(output_path, file_name), 'w') as f:
			f.write(json_file)
			f.close()

def test():
	# initialize the audio detector and conduct filtering
	ad = onset_detector(2048, 411)
	sf, time_interval = ad.spectralflux('../data/beat_it.mp3')
	# initialize onset selector for beat selection
	selector = onset_selector(sf[0, :], 3, 3, 0.3, 0.8)
	quantified = selector.find_peaks()

	print("Finish detection and beat selection.")

	start = time.time()
	# start beat mapping, this test case map the beats into 4 tracks
	bm = beat_mapper(sf, quantified, time_interval, 4)
	mapped = bm.map_to_tracks() # this is the essential method

	print("Finish mapping.")
	print("Running time {} seconds.".format(time.time() - start))

	# now write necessary info to a json file for visualization module
	print("Start writting json file.")
	start = time.time()
	bm.write_to_json('./')
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
