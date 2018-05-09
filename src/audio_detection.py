# -*- coding: utf-8 -*-
"""
Created on Thu May  3 23:33:23 2018

@author: yaxuan zhu
"""

import numpy as np
import madmom
import os
import time
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.ndimage.filters import maximum_filter

class audio_detector(object):
    def __init__(self, frame_size = 2048, hop_size = 441):
        self.frame_size = frame_size
        self.hop_size = hop_size
    
###############################################################################
# Do onset detection using spectral flux algorithm
# Input： 
#       path: the path of the audio file
# Output:
#       sf: the spectral of change according to time;
#           the first dimension correspond to the channels
#       time_interval: time interval between 2 points in sf        
###############################################################################    
    def spectralflux(self, path = None):
        if path == None:
            print('Enter file name please!')
            return None, None
        if os.path.isfile(path) == False:
            print('File does not exist, please check you path!')
            return None, None
        sig = madmom.audio.signal.Signal(path)
        num_channels = sig.num_channels
        sample_rate = sig.sample_rate
        time_interval = self.hop_size / sample_rate
        
        sf = None
        for i in range(num_channels):
            tmp = sig[:, i]
            tmpframe = madmom.audio.signal.FramedSignal(tmp, frame_size = self.frame_size, hop_size = self.hop_size)
            tmpstft = madmom.audio.stft.STFT(tmpframe)
            tmpspec = madmom.audio.spectrogram.Spectrogram(tmpstft)
            tmpdiff = np.zeros(tmpspec.shape)
            tmpdiff[1:] = np.diff(tmpspec, axis = 0)
            tmppos = np.maximum(0, tmpdiff)
            tmpsf = np.sum(tmppos, axis = 1)
            if i == 0:
                sf = np.expand_dims(tmpsf, axis = 0)
            else:
                sf = np.append(sf, np.expand_dims(tmpsf, axis = 0), axis = 0) 
        
        return sf, time_interval 

###############################################################################
# Do onset detection using super flux algorithm
# Input： 
#       path: the path of the audio file
# Output:
#       sf: the sufer flux spectral of change according to time;
#           the first dimension correspond to the channels
#       time_interval: time interval between 2 points in sf         
###############################################################################    
    def superflux(self, path = None):
        if path == None:
            print('Enter file name please!')
            return None, None
        if os.path.isfile(path) == False:
            print('File does not exist, please check you path!')
            return None, None
        sig = madmom.audio.signal.Signal(path)
        num_channels = sig.num_channels
        sample_rate = sig.sample_rate
        time_interval = self.hop_size / sample_rate
        
        sf = None
        for i in range(num_channels):
            tmp = sig[:, i]
            tmpframe = madmom.audio.signal.FramedSignal(tmp, frame_size = self.frame_size, hop_size = self.hop_size)
            tmpstft = madmom.audio.stft.STFT(tmpframe)
            tmpspec = madmom.audio.spectrogram.Spectrogram(tmpstft)
            tmpfilt_spec = madmom.audio.spectrogram.FilteredSpectrogram(tmpspec, filterbank=madmom.audio.filters.LogFilterbank, num_bands=24)
            tmplog_spec = madmom.audio.spectrogram.LogarithmicSpectrogram(tmpfilt_spec, add=1)
            tmpsize = (1, 3)
            tmpmax_spec = maximum_filter(tmplog_spec, size=tmpsize)
            tmpdiff = np.zeros(tmplog_spec.shape)
            tmpdiff[1:] = (tmplog_spec[1:] - tmpmax_spec[:-1])
            tmppos = np.maximum(0, tmpdiff)
            tmpsf = np.sum(tmppos, axis = 1)
            if i == 0:
                sf = np.expand_dims(tmpsf, axis = 0)
            else:
                sf = np.append(sf, np.expand_dims(tmpsf, axis = 0), axis = 0) 
        
        return sf, time_interval


###############################################################################
# Do onset detection using normalized weighted phase deviation algorithm
# Input： 
#       path: the path of the audio file
# Output:
#       nwpd: the weighted phase deviation of change according to time;
#           the first dimension correspond to the channels
#       time_interval: time interval between 2 points in nwpd          
###############################################################################
    def normalized_weighted_phase_deviation(self, path = None):
        if path == None:
            print('Enter file name please!')
            return None, None
        if os.path.isfile(path) == False:
            print('File does not exist, please check you path!')
            return None, None
        sig = madmom.audio.signal.Signal(path)
        num_channels = sig.num_channels
        sample_rate = sig.sample_rate
        time_interval = self.hop_size / sample_rate
        
        nwpd = None
        for i in range(num_channels):
            tmp = sig[:, i]
            tmpframe = madmom.audio.signal.FramedSignal(tmp, frame_size = self.frame_size, hop_size = self.hop_size)
            tmpstft = madmom.audio.stft.STFT(tmpframe)
            tmpphase = madmom.audio.stft.phase(tmpstft)
            tmpphase_diff = np.diff(tmpphase, axis = 0)
            tmpphase_diff_2nd = np.zeros(tmpphase.shape) 
            tmpphase_diff_2nd[2:] = np.diff(tmpphase_diff, axis = 0)
            tmpspec = madmom.audio.spectrogram.Spectrogram(tmpstft)
            tmpwpd = np.sum(np.abs(tmpspec * tmpphase_diff_2nd), axis = 1)
            tmpnormalization = np.sum(np.abs(tmpspec)) 
            tmpnwpd = tmpwpd / tmpnormalization

            if i == 0:
                nwpd = np.expand_dims(tmpnwpd, axis = 0)
            else:
                nwpd = np.append(nwpd, np.expand_dims(tmpnwpd, axis = 0), axis = 0) 
        
        return nwpd, time_interval 

    

def test(path):
<<<<<<< HEAD:src/audio_process.py

    print(path)

    myprocessor = audio_processor(2048, 441)
=======
    myprocessor = audio_detector(2048, 441)
>>>>>>> 0b14a2ffaf536427e8f8ea0d2e645f5dd9f0b6dc:src/audio_detection.py

    # start = time.time()
    # sf, time_interval = myprocessor.spectralflux(path)
    # print("Running spectral flux use {} seconds.".format(time.time() - start))
    # print(sf.shape)
    # print(time_interval)
    # N = len(sf)
    # for i in range(N):
    #     plt.figure()
    #     plt.plot(sf[i, : 2000])
    #     plt.savefig('sf_{}.png'.format(i))
    #
    # start = time.time()
    # sf, time_interval = myprocessor.superflux(path)
    # print("Running super flux use {} seconds.".format(time.time() - start))
    # print(sf.shape)
    # print(time_interval)
    # N = len(sf)
    # for i in range(N):
    #     plt.figure()
    #     plt.plot(sf[i, : 2000])
    #     plt.savefig('superflux_{}.png'.format(i))
       
    start = time.time()  
    nwpd, time_interval = myprocessor.normalized_weighted_phase_deviation(path)
    print("Running normalizaed weighted phase deviation use {} seconds.".format(time.time() - start))
    print(nwpd.shape)
    print(time_interval)

    #quantize
    N = len(nwpd)


    #visualize
    for i in range(N):
        nwpd[nwpd < 0.0001] = 0

    for i in range(N):
        plt.figure()
        plt.plot(nwpd[i, :2000])
        plt.savefig('nwpd_{}.png'.format(i))
    
if __name__== '__main__':
<<<<<<< HEAD:src/audio_process.py
    test("/Users/wzq/cs130/beatmap/beatmap-generator/data/" + "beat_it.mp3")
    # test('./data/beat_it.mp3')
=======
    test('../data/beat_it.mp3')
>>>>>>> 0b14a2ffaf536427e8f8ea0d2e645f5dd9f0b6dc:src/audio_detection.py
