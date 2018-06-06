# -*- coding: utf-8 -*-

'''
@author: Quincy Qu

This file contains the utility class for state machine implmentation used in beat_mapping. 
	class State  (and its children classes)
	class StateMachine
	and testing functions

One base class STATE, it has 4 children classes.
StateMachine contains the a few states and the transition table.


TODO:
1. generate more tests and validate the code
2. substitute current random transition table

'''

import numpy as np
import random
random.seed(5678)

class State:
	def __init__(self, name):
		self.name = name
	def __str__(self):
		return self.name

	def get_name(self):
		return self.name

	def make_state(name):
		if(name == 'random'):
			return RandomState(name)
		elif(name == 'stair'):
			return StairState(name)
		elif(name == 'stair_rev'):
			return StairRevState(name)
		elif(name == 'switch'):
			return SwitchState(name)
		else:
			return None
	def do_mapping(self):
		'''
		The mapping function to be specified by each state
		'''
		pass

class RandomState(State):
	def __init__(self, name):
		State.__init__(self, name)
		

	def do_mapping(self, num_track):
		#random mapping TBD
		if(num_track == 0):
			print('123')
			return
		k = random.randint(0, num_track - 1)
		return k


class StairState(State):
	def __init__(self, name):
		State.__init__(self, name)
		self.prev = -1

	def do_mapping(self, num_track):
		if(num_track == 0):
			print('345')
			return
		k = (self.prev + 1) % num_track
		self.prev = k
		return k

class StairRevState(State):
	def __init__(self, name):
		State.__init__(self, name)
		self.prev = 0

	def do_mapping(self, num_track):
		if(num_track == 0):
			print('456')
			return
		k = (self.prev - 1) % num_track
		self.prev = k
		return k

class SwitchState(State):
	def __init__(self, name):
		State.__init__(self, name)
		self.start = 0
		self.end = 0
		self.cnt = 0
		self.change_threshold = 8
	def do_mapping(self, num_track):
		#switch mapping TBD
		if(num_track == 0):
			print('678')
			return
		if(self.cnt == 0):
			self.start = random.randint(0, num_track - 1)
			self.end = random.randint(0, num_track - 1)
		self.cnt = (self.cnt + 1) % self.change_threshold
		if(self.cnt % 2 == 1):
			return self.start
		else:
			return self.end



class StateMachine:
	def __init__(self, beat_array, num_track):
		self.state_list = []
		self.state_dict = dict()
		self.mapped = np.zeros((len(beat_array), num_track), dtype=int)
		self.num_track = num_track
		self.beat_array = beat_array
		self.change_threshold = 4 # number of beats that remain in each state

	def add_state(self, state):
		self.state_list.append(state)
		self.state_dict[state.get_name()] = state

	def add_state_list(self, state_list):
		self.state_list.addAll(state_list)
		for state in state_list:
			self.state_dict[state.get_name()] = state

	def next_state(self, current_state):
		# return random state for current version, to be complete
		rand_int = random.randint(0, len(self.state_list) - 1)
		return self.state_list[rand_int]

	def run(self):
		current_state = self.state_dict['random'] # suppose always start with random state
		current_cnt = 0
		pos = 0
		cnt = 0
		#print(current_state)
		while(pos < len(self.beat_array)):
			if(self.beat_array[pos] > 0):
				current_cnt += 1
				cnt += 1
				ch = current_state.do_mapping(self.num_track)
				self.mapped[pos][ch] = 1
			if(current_cnt >= self.change_threshold):
				current_cnt = 0
				current_state = self.next_state(current_state) # to be complete, random state transition used in current version
				#print(current_state)
			pos += 1
		return cnt

	def test(self):
		print("number of state: {}".format(len(self.state_list)))
		print("number of tracks: {}".format(self.num_track))
		print("beat_array: " + str(self.beat_array))

def test_state():
	'''
		This test is designed to test how the factory method State.make_state() work.
		We aim to initialize a list of state (of its sub-class) by its name, and call its corresponding mapping function.

		You should see the output: 

		123
		True
		345
		False
		123
		True
		678
		False
		456
		False

	'''
	name_list = ['random', 'stair', 'random', 'switch', 'stair_rev']
	for name in name_list:
		state = State.make_state(name)
		if(state != None):
			state.do_mapping(0)
			print(state.get_name() == 'random')


def test_state_machine():
	'''
		This test is designed to do the sanity check of state_machine.
		There should be 4 states in this case and 4 tracks.
		The mapping algorithm is printed for view.
		The mapping result is printed for view.
	'''
	beat_array = [1,0,1,3,0,2,0,0,1,0,2,2,1,0,1,5]
	state_machine = StateMachine(beat_array, 4)
	name_list = ['random', 'stair', 'random', 'switch', 'stair_rev']
	for name in name_list:
		state_machine.add_state(State.make_state(name))

	state_machine.test()
	state_machine.run()
	print("mapped: ")
	print(state_machine.mapped)


if __name__ == '__main__':
	test_state_machine()
