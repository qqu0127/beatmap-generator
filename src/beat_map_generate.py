# -*- coding: utf-8 -*-

'''
@author: Quincy Qu

This document contains the command line entry point for the whole algorithm pipeline.
The wrapper method: beat_map_generate()
and other utility functions.
'''
import numpy as np
import madmom
import os
import time
import matplotlib
import json
import random
import argparse

from onset_detection import onset_detector
from onset_selection import onset_selector
from beat_mapping import beat_mapper
from state_machine import State, StateMachine

def beat_map_generate(param):
	'''
		This is the entry point that starts the processing pipeline, with all bells and whistles.

		Usage:
			python beat_map_generate.py 
				--input=[AUDIO_PATH]
				--num_tracks=[NUM_TRACKS]
				--output=[OUTPUT_PATH]
				--method=[DETECTION_METHOD]
				--free_beat_range=[FREE_BEAT_RANGE]
	'''
	detector = make_detector()
	sf, time_interval = detector.process_signal(param.input, method=param.method, do_filtering=True)
	param.sf = sf
	param.time_interval = time_interval

	selector = make_selector(param)
	beat_array = selector.find_peaks(param.free_beat_range)

	mapper = make_mapper(param)
	mapped = mapper.map_to_tracks(beat_array)
	mapper.write_to_json(mapped, param.output)


def make_detector():
	detector = onset_detector(2048, 441)
	return detector

def make_selector(param):
	selector = onset_selector(param.sf, 10, 3, 3, 0.3, 0.2)
	return selector

def make_mapper(param):
	mapper = beat_mapper(param.time_interval, param.num_tracks)
	return mapper

def parse_args():
	parser = argparse.ArgumentParser()
	parser.add_argument('--input', type=str, required=True, 
		help='Please specify the input audio file.')
	parser.add_argument('--num_tracks', type=int, required=False, default=4,
		help='You can specify the number of tracks to map on.')
	parser.add_argument('--output', type=str, required=False, default='beat_map.json',
		help='You can specify the output file name.')
	parser.add_argument('--method', type=str, required=False, default='superflux', choices=['superflux', 'spectralflux', 'nwpd'],
		help='You can specify the detection method, please refer to onset_detection.')
	parser.add_argument('--free_beat_range', type=int, required=False, default=20,
		help='You can specify the free beat range for beat selection.')
	return parser.parse_args()

if __name__ == '__main__':
	args = parse_args()
	beat_map_generate(args)

