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
        self.__onsetsNorm = preprocessing.scale(self.__onsetsOrg, axis=1) # normalize
        self.__onsetsLen = onsets.shape[1] 
        self.__onsetsChl = onsets.shape[0] 
        #self.__onsetsPeakPos = [[] for i in range(self.__onsetsChl)]
        self.__onsetsPeaks = [[] for i in range(self.__onsetsChl)]
        self.__onsetStride = np.amax(self.__onsetsOrg, axis=1) / float(numOfLevel)
        self.__thres = [0 for i in range(self.__onsetsChl)]
        #self.__thresQue = []
        self.__alpha = alpha
        self.__m = m
        self.__w = w
        self.__phi = phi
        self.__flip = 0 

    def find_peaks(self, intvl = 200):
        try:
            return self.__onsetsQuan
        except AttributeError:        
            for chl in range(self.__onsetsChl):
                for i in range(self.__onsetsLen):
                    if self.__check_std1(chl, i) and self.__check_std2(chl, i) and self.__check_std3(chl, i):
                        #self.__onsetsPeakPos[chl].append(i);
                        self.__onsetsPeaks[chl].append(self.__onsetsOrg[chl, i])
                    else:
                        self.__onsetsPeaks[chl].append(0)
                    self.__update_thres(chl, i)
            self.__filter(intvl)
            self.__quantify()
            #self.__channel_orthogonalize()
            return np.array(self.__onsetsQuan)

    def __filter (self, intvl):
        for chl in range(self.__onsetsChl):
            nextPos = 0 
            for i in range(self.__onsetsLen):
                if i > nextPos and self.__onsetsPeaks[chl][i] > 0:
                    nextPos = i + intvl
                else:
                    self.__onsetsPeaks[chl][i] = 0


    def __quantify (self):
        self.__onsetsQuan = []
        for chl in range(self.__onsetsChl):
            if self.__onsetStride[chl] >= 1.0:
                self.__onsetsQuan.append(list(map(lambda x: int((x + self.__onsetStride[chl] - 1) / self.__onsetStride[chl]), self.__onsetsPeaks[chl])))
            else:
                self.__onsetsQuan.append([])
                for item in self.__onsetsPeaks[chl]:
                    if item == 0: 
                        self.__onsetsQuan[-1].append(item)
                    else:
                        catalog = int(item / self.__onsetStride[chl])
                        if catalog == 0:
                            self.__onsetsQuan[-1].append(1)  
                        elif catalog >= 10:
                                self.__onsetsQuan[-1].append(10)
                        else:
                            self.__onsetsQuan[-1].append(item)
    
    def __check_std1 (self, chl, i):
        if i - self.__w < 0:
            j = 0
        else:
            j = i - self.__w
        
        if i + self.__w + 1 > self.__onsetsLen:
            bound = self.__onsetsLen  
        else:
            bound = i + self.__w + 1
        
        while j < bound:
            if self.__onsetsNorm[chl, i] < self.__onsetsNorm[chl, j]:
                break
            j += 1        
        return j == bound
 
    def __check_std2 (self, chl, i):
        if i - self.__m * self.__w < 0:
            left = 0
        else:
            left =  i - self.__m * self.__w

        if i + self.__w + 1 > self.__onsetsLen: # right cannot be reached
            right = self.__onsetsLen 
        else:
            right = i + self.__w + 1

        return self.__onsetsNorm[chl, i] >= sum(self.__onsetsNorm[chl, left: right]) / (right - left) + self.__phi

    def __check_std3 (self, chl, i):
        return self.__onsetsNorm[chl, i] >= self.__thres[chl]

    def __update_thres (self, chl, i):
        self.__thres[chl] = max(self.__onsetsNorm[chl, i], self.__alpha * self.__thres[chl] + (1 - self.__alpha) * self.__onsetsNorm[chl, i])
   
    def __channel_orthogonalize(self, strategy = 1):
        if strategy:
            for i in range(self.__onsetsLen):
                chl = 0
                while self.__onsetsPeaks[chl][i] > 0:
                    chl += 1
                    if chl == self.__onsetsChl:
                        for j in range(self.__onsetsChl):
                            self.__onsetsPeaks[j][i]  = self.__onsetsPeaks[j][i] if j == self.__onsetsChl else 0 
                        self.__flip  = (self.__flip + 1) % self.__onsetsChl
                        break
        else:
            for i in range(self.__onsetsLen):
                if self.__onsetsPeaks[1][i] == self.__onsetsPeaks[1][i] and self.__onsetsPeaks[0] != 0:
                    self.__onsetsPeaks[self.flip][i] = 0
                    self.__flip = ~self.__flip
                elif self.__onsetsPeaks[1][i] > self.__onsetsPeaks[0][i]:
                    self.__onsetsPeaks[0][i] = 0
                elif self.__onsetsPeak[1][i] < self.__onsetsPeaks[0][i]:
                    self.__onsetsPeaks[1][i] = 0
                     
         
def test(path):
    myprocessor = onset_detector(2048, 441)

    start = time.time() 
    sf, time_interval = myprocessor.spectralflux(path, True)
    print("Running spectral flux use {} seconds.".format(time.time() - start))    
    print(sf.shape)
    print(time_interval)
   
    selector = onset_selector(sf, 10, 3, 3, 0.3, 0.2)
    quantified = selector.find_peaks()
    
    plt.figure()
    fig,left_axis=plt.subplots()    
    right_axis = left_axis.twinx()
    p1, = left_axis.plot(sf[0, : 2000])
    p2, = right_axis.plot(quantified[0, 0 : 2000], 'r--')    
    #right_axis.set_ylim(0, 5)
    plt.savefig('sf0.png')

    plt.figure()
    fig,left_axis=plt.subplots()    
    right_axis = left_axis.twinx()
    p1, = left_axis.plot(sf[1, : 2000])
    p2, = right_axis.plot(quantified[1, 0 : 2000], 'r--')    
    #right_axis.set_ylim(0, 5)
    plt.savefig('sf1.png')

    start = time.time() 
    sf, time_interval = myprocessor.superflux(path, True)
    print("Running super flux use {} seconds.".format(time.time() - start))   
    print(sf.shape)
    print(time_interval)
     
    selector = onset_selector(sf, 10, 3, 3, 0.3, 0.8)
    quantified = selector.find_peaks()
    
    plt.figure()
    fig,left_axis=plt.subplots()    
    right_axis = left_axis.twinx()
    p1, = left_axis.plot(sf[0, : 2000])
    p2, = right_axis.plot(quantified[0, 0 : 2000], 'r--')    
    #right_axis.set_ylim(0, 5)
    plt.savefig('superflux0.png')

    plt.figure()
    fig,left_axis=plt.subplots()    
    right_axis = left_axis.twinx()
    p1, = left_axis.plot(sf[1, : 2000])
    p2, = right_axis.plot(quantified[1, 0 : 2000], 'r--')    
    #right_axis.set_ylim(0, 5)
    plt.savefig('superflux1.png')

    start = time.time()  
    nwpd, time_interval = myprocessor.normalized_weighted_phase_deviation(path, True)
    print("Running normalizaed weighted phase deviation use {} seconds.".format(time.time() - start))
    print(nwpd.shape)
    print(time_interval)
    selector = onset_selector(nwpd, 10, 3, 3, 0.3, 0.5) # this set of params reduce probability of false negative
    quantified = selector.find_peaks()
    
    plt.figure()
    fig,left_axis=plt.subplots()    
    right_axis = left_axis.twinx()
    p1, = left_axis.plot(nwpd[0, : 2000])
    p2, = right_axis.plot(quantified[0, 0 : 2000], 'r--')    
    #right_axis.set_ylim(0, 5)
    plt.savefig('nwpd0.png')

    plt.figure()
    fig,left_axis=plt.subplots()    
    right_axis = left_axis.twinx()
    p1, = left_axis.plot(nwpd[1, : 2000])
    p2, = right_axis.plot(quantified[1, 0 : 2000], 'r--')    
    #right_axis.set_ylim(0, 5)
    plt.savefig('nwpd1.png')
if __name__== '__main__':
    test('../data/beat_it.mp3')
