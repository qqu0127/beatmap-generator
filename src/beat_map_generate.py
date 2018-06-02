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
			python beat_map_generate.py --path=[AUDIO_PATH]
	'''
	detector = make_detector()
	sf, time_interval = detector.process_signal(param['path'], method = 'superflux', do_filtering=True)

	selector = make_selector({'sf': sf})
	beat_array = selector.find_peaks()

	mapper = make_mapper({'time_interval': time_interval})
	mapped = mapper.map_to_tracks(beat_array)
	mapper.write_to_json(mapped, './', 'test_mapped.json')


def make_detector(param={}):
	detector = onset_detector(2048, 441)
	return detector

def make_selector(param={}):
	selector = onset_selector(param['sf'], 10, 3, 3, 0.3, 0.2)
	return selector

def make_mapper(param={}):
	mapper = beat_mapper(param['time_interval'], 4)
	return mapper


def parse_args():
	parser = argparse.ArgumentParser()
	parser.add_argument('--path', type=str, required=True, 
		help='Please specify the input audio file.')
	return parser.parse_args()

if __name__ == '__main__':
	args = parse_args()
	beat_map_generate({'path': args.path})




