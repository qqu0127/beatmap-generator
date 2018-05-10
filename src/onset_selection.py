# -*- coding: utf-8 -*-

import matplotlib
matplotlib.use('Agg')
from onset_detection import onset_detector
import numpy as np
import madmom
import os
import time
import matplotlib.pyplot as plt
from scipy.ndimage.filters import maximum_filter
from sklearn import preprocessing

PARAM_SETS = {1: [10, 3, 3, 0.3, 0.2]}

class onset_selector(object):
    def __init__(self, onsets, numOfLevel, m, w, alpha, phi):
        self.onsetsOrg = onsets
        self.onsetsNorm = preprocessing.scale(self.onsetsOrg).tolist() # normalize
        self.onsetsLen = onsets.shape[0] 
        self.onsetsPeakPos = []
        self.onsetsPeaks = []
        self.onsetStride = max(self.onsetsOrg) / float(numOfLevel)
        self.thres = 0
        self.thresQue = []
        self.alpha = alpha
        self.m = m
        self.w = w
        self.phi = phi
    
    def find_peaks(self):
        if(self.onsetsPeaks is not []):
            self.onsetsPeaks = []
            self.onsetsPeakPos = []
        for i in range(0, self.onsetsLen):
            if self.apply_std1(i) and self.apply_std2(i) and self.apply_std3(i):
                self.onsetsPeakPos.append(i);
                self.onsetsPeaks.append(self.onsetsOrg[i])
            else:
                self.onsetsPeaks.append(0)
            self.update_thres(i)
        return self.quantify()

    def quantify (self):
        return np.array(list(map(lambda x: int(x / self.onsetStride), self.onsetsPeaks)))
    
    def apply_std1 (self, i):
        if i - self.w < 0:
            j = 0
        else:
            j = i - self.w
        
        if i + self.w + 1 > self.onsetsLen:
            bound = self.onsetsLen  
        else:
            bound = i + self.w + 1
        
        while j < bound:
            if self.onsetsNorm[i] < self.onsetsNorm[j]:
                break
            j += 1        
        return j == bound
 
    def apply_std2 (self, i):
        if i - self.m * self.w < 0:
            left = 0
        else:
            left =  i - self.m * self.w

        if i + self.w + 1 > self.onsetsLen: # right cannot be reached
            right = self.onsetsLen 
        else:
            right = i + self.w + 1

        return self.onsetsNorm[i] >= sum(self.onsetsNorm[left: right]) / (right - left) + self.phi

    def apply_std3 (self, i):
        return self.onsetsNorm[i] >= self.thres

    def update_thres (self, i):
        self.thresQue.append(self.thres)
        self.thres = max(self.onsetsNorm[i], self.alpha * self.thres + (1 - self.alpha) * self.onsetsNorm[i])
   
    def channel_coalesce(self):
        #TBD
        pass
    
def test(path):
    myprocessor = onset_detector(2048, 441)

    start = time.time() 
    sf, time_interval = myprocessor.spectralflux(path)
    print("Running spectral flux use {} seconds.".format(time.time() - start))    
    print(sf.shape)
    print(time_interval)
   
    selector = onset_selector(sf[0, :], 10, 3, 3, 0.3, 0.2)
    quantified = selector.find_peaks()
    
    plt.figure()
    fig,left_axis=plt.subplots()    
    right_axis = left_axis.twinx()
    p1, = left_axis.plot(sf[0, : 2000])
    p2, = right_axis.plot(quantified[0 : 2000], 'r--')    
    #right_axis.set_ylim(0, 5)
    plt.savefig('sf.png')

    start = time.time() 
    sf, time_interval = myprocessor.superflux(path)
    print("Running super flux use {} seconds.".format(time.time() - start))   
    print(sf.shape)
    print(time_interval)
     
    selector = onset_selector(sf[0, :], 10, 3, 3, 0.3, 0.8)
    quantified = selector.find_peaks()
    
    plt.figure()
    fig,left_axis=plt.subplots()    
    right_axis = left_axis.twinx()
    p1, = left_axis.plot(sf[0, : 2000])
    p2, = right_axis.plot(quantified[0 :2000], 'r--')    
    #right_axis.set_ylim(0, 5)
    plt.savefig('superflux.png')

    start = time.time()  
    nwpd, time_interval = myprocessor.normalized_weighted_phase_deviation(path)
    print("Running normalizaed weighted phase deviation use {} seconds.".format(time.time() - start))
    print(nwpd.shape)
    print(time_interval)
    selector = onset_selector(sf[0, :], 10, 3, 3, 0.3, 0.8)
    quantified = selector.find_peaks()
    
    plt.figure()
    fig,left_axis=plt.subplots()    
    right_axis = left_axis.twinx()
    p1, = left_axis.plot(sf[0, : 2000])
    p2, = right_axis.plot(quantified[0 :2000], 'r--')    
    #right_axis.set_ylim(0, 5)
    plt.savefig('nwpd.png')

if __name__== '__main__':
    test('../data/beat_it.mp3')
