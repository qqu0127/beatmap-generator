# -*- coding: utf-8 -*-

import matplotlib
matplotlib.use('Agg')
import audio_process as ap
import numpy as np
import madmom
import os
import time
import matplotlib.pyplot as plt
from scipy.ndimage.filters import maximum_filter
from sklearn import preprocessing

PARAM_SET = {1: [3, 3, 0.3, 0.8]}

class onsetSel (object):
    def __init__(self, onsetSeq, m, w, alpha, phi):
        self.onsetSeqOrg = onsetSeq
        self.onsetSeq = preprocessing.scale(self.onsetSeqOrg).tolist() # normalize
        self.onsetSeqLen = onsetSeq.shape[0] 
        self.peakPos = []
        self.peaks = []
        self.thres = 0
        self.thresQue = []
        self.alpha = alpha
        self.m = m
        self.w = w
        self.phi = phi
    
    def find_peaks(self):
        for i in range(0, self.onsetSeqLen):
            if self.apply_std1(i) and self.apply_std2(i) and self.apply_std3(i):
                self.peakPos.append(i);
                self.peaks.append(1)
            else:
                self.peaks.append(0)
            self.update_thres(i)
        return self.quantify()

    def quantify (self):
        return self.peaks
    
    def apply_std1 (self, i):
        if i - self.w < 0:
            j = 0
        else:
            j = i - self.w
        
        if i + self.w + 1 > self.onsetSeqLen:
            bound = self.onsetSeqLen  
        else:
            bound = i + self.w + 1
        
        while j < bound:
            if self.onsetSeq[i] < self.onsetSeq[j]:
                break
            j += 1        
        return j == bound
 
    def apply_std2 (self, i):
        if i - self.m * self.w < 0:
            left = 0
        else:
            left =  i - self.m * self.w

        if i + self.w + 1 > self.onsetSeqLen: # right cannot be reached
            right = self.onsetSeqLen 
        else:
            right = i + self.w + 1

        return self.onsetSeq[i] >= sum(self.onsetSeq[left: right]) / (right - left) + self.phi

    def apply_std3 (self, i):
        return self.onsetSeq[i] >= self.thres

    def update_thres (self, i):
        self.thresQue.append(self.thres)
        self.thres = max(self.onsetSeq[i], self.alpha * self.thres + (1 - self.alpha) * self.onsetSeq[i])

def main(path):
    myprocessor = ap.audio_processor(2048, 441)

    start = time.time() 
    sf, time_interval = myprocessor.spectralflux(path)
    print("Running spectral flux use {} seconds.".format(time.time() - start))    
    print(sf.shape)
    print(time_interval)
   
    selector = onsetSel(sf[0, :], 3, 3, 0.3, 0.8)
    quantified = selector.find_peaks()
    
    plt.figure()
    fig,left_axis=plt.subplots()    
    right_axis = left_axis.twinx()
    p1, = left_axis.plot(sf[0, : 2000])
    p2, = right_axis.plot(quantified[0 :2000], 'r--')    
    right_axis.set_ylim(0, 5)
    plt.savefig('sf.png')

    start = time.time() 
    sf, time_interval = myprocessor.superflux(path)
    print("Running super flux use {} seconds.".format(time.time() - start))   
    print(sf.shape)
    print(time_interval)
     
    selector = onsetSel(sf[0, :], 3, 3, 0.3, 0.8)
    quantified = selector.find_peaks()
    
    plt.figure()
    fig,left_axis=plt.subplots()    
    right_axis = left_axis.twinx()
    p1, = left_axis.plot(sf[0, : 2000])
    p2, = right_axis.plot(quantified[0 :2000], 'r--')    
    right_axis.set_ylim(0, 5)
    plt.savefig('superflux.png')

    start = time.time()  
    nwpd, time_interval = myprocessor.nwpd(path)
    print("Running normalizaed weighted phase deviation use {} seconds.".format(time.time() - start))
    print(nwpd.shape)
    print(time_interval)
    selector = onsetSel(sf[0, :], 3, 3, 0.3, 0.8)
    quantified = selector.find_peaks()
    
    plt.figure()
    fig,left_axis=plt.subplots()    
    right_axis = left_axis.twinx()
    p1, = left_axis.plot(sf[0, : 2000])
    p2, = right_axis.plot(quantified[0 :2000], 'r--')    
    right_axis.set_ylim(0, 5)
    plt.savefig('nwpd.png')

if __name__== '__main__':
    main('../data/beat_it.mp3')
