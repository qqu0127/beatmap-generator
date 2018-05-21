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

PARAM_SETS = {1: [10, 3, 3, 0.3, 0.2], "nwpd": [10, 3, 3, 0.3, 0.5]}

class onset_selector(object):
    def __init__(self, onsets, numOfLevel, m, w, alpha, phi):
        self.__onsetsOrg = onsets
        self.__onsetsNorm = preprocessing.scale(self.__onsetsOrg).tolist() # normalize
        self.__onsetsLen = onsets.shape[0] 
        self.__onsetsPeakPos = []
        self.__onsetsPeaks = []
        self.__onsetStride = max(self.__onsetsOrg) / float(numOfLevel)
        self.__thres = 0
        self.__thresQue = []
        self.__alpha = alpha
        self.__m = m
        self.__w = w
        self.__phi = phi
    
    def find_peaks(self):
        if(self.__onsetsPeaks is not []):
            self.__onsetsPeaks = []
            self.__onsetsPeakPos = []
        for i in range(0, self.__onsetsLen):
            if self.__check_std1(i) and self.__check_std2(i) and self.__check_std3(i):
                self.__onsetsPeakPos.append(i);
                self.__onsetsPeaks.append(self.__onsetsOrg[i])
            else:
                self.__onsetsPeaks.append(0)
            self.__update_thres(i)
        return self.__quantify()

    def __quantify (self):
        if self.__onsetStride >= 1.0:
            return np.array(list(map(lambda x: int((x + self.__onsetStride - 1) / self.__onsetStride), self.__onsetsPeaks)))
        else:
            res = []
            for item in self.__onsetsPeaks:
                if item == 0: 
                    res.append(item)
                else:
                    catalog = int(item / self.__onsetStride)
                    if catalog == 0:
                        res.append(1)  
                    elif catalog >= 10:
                            res.append(10)
                    else:
                        res.append(item)
            return np.array(res)
    
    def __check_std1 (self, i):
        if i - self.__w < 0:
            j = 0
        else:
            j = i - self.__w
        
        if i + self.__w + 1 > self.__onsetsLen:
            bound = self.__onsetsLen  
        else:
            bound = i + self.__w + 1
        
        while j < bound:
            if self.__onsetsNorm[i] < self.__onsetsNorm[j]:
                break
            j += 1        
        return j == bound
 
    def __check_std2 (self, i):
        if i - self.__m * self.__w < 0:
            left = 0
        else:
            left =  i - self.__m * self.__w

        if i + self.__w + 1 > self.__onsetsLen: # right cannot be reached
            right = self.__onsetsLen 
        else:
            right = i + self.__w + 1

        return self.__onsetsNorm[i] >= sum(self.__onsetsNorm[left: right]) / (right - left) + self.__phi

    def __check_std3 (self, i):
        return self.__onsetsNorm[i] >= self.__thres

    def __update_thres (self, i):
        self.__thresQue.append(self.__thres)
        self.__thres = max(self.__onsetsNorm[i], self.__alpha * self.__thres + (1 - self.__alpha) * self.__onsetsNorm[i])
   
    def __channel_coalesce(self):
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
    p2, = right_axis.plot(quantified[0 : 2000], 'r--')    
    #right_axis.set_ylim(0, 5)
    plt.savefig('superflux.png')

    start = time.time()  
    nwpd, time_interval = myprocessor.normalized_weighted_phase_deviation(path)
    print("Running normalizaed weighted phase deviation use {} seconds.".format(time.time() - start))
    print(nwpd.shape)
    print(time_interval)
    selector = onset_selector(nwpd[0, :], 10, 3, 3, 0.3, 0.5) # this set of params reduce probability of false negative
    quantified = selector.find_peaks()
    
    plt.figure()
    fig,left_axis=plt.subplots()    
    right_axis = left_axis.twinx()
    p1, = left_axis.plot(nwpd[0, : 2000])
    p2, = right_axis.plot(quantified[0 : 2000], 'r--')    
    #right_axis.set_ylim(0, 5)
    plt.savefig('nwpd.png')

if __name__== '__main__':
    test('../data/beat_it.mp3')
