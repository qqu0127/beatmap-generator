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
from scipy import signal

class onset_detector(object):
    def __init__(self, frame_size = 2048, hop_size = 441):
        self.frame_size = frame_size
        self.hop_size = hop_size
        self.low_freq = 0.0
        self.high_freq = 1.0
        
    def filter_signal(self, fre_signal, low_freq, high_freq):
        N = fre_signal.shape[0]
        length = fre_signal.shape[1]
        low_fre_n = int(length * low_freq) + 1
        high_fre_n = int(length * high_freq)
        for i in range(N):
            fre_signal[i][0: low_fre_n] = np.zeros((low_fre_n))
            fre_signal[i][high_fre_n:] = np.zeros((length - high_fre_n))
        
        return fre_signal
    
    def process_signal(self, path = None, method = 'superflux', do_filtering = False, freq_list = [[40.0, 200.0]]):
        if method == 'spectralflux':
            return self.spectralflux(path, do_filtering, freq_list)
        elif method == 'superflux':
            return self.superflux(path, do_filtering, freq_list)
        elif method == 'normalized_weighted_phase_deviation':
            return self.normalized_weighted_phase_deviation(path, do_filtering, freq_list)
        else:
            print('Error: Please select a method by changing the method parameter')
            print('The valid methods are:')
            print('    spectralflux')
            print('    superflux')
            print('    normalized_weighted_phase_deviation')
            print('ps: If you do not know which one to choose, choose the superflux as default')
            return None, None
    
###############################################################################
# Do onset detection using spectral flux algorithm
# Input： 
#       path: the path of the audio file
#       do_filtering: indicate whether you want to filter the audio signal, please enter the 
#                     band you want to keep in the freq_list if you set it to True
#       freq_list: the bandwidth you want to keep, enter a list, each item in this list 
#                  is in the form of [low_freq, high_freq] 
# Output:
#       sf: the spectral of change according to time;
#           the first dimension is (the number of pass band you want * channels)
#       time_interval: time interval between 2 points in sf        
###############################################################################    
    def spectralflux(self, path = None, do_filtering = False, freq_list = [[40.0, 200.0]]):
        if path == None:
            print('Enter file name please!')
            return None, None
        if os.path.isfile(path) == False:
            print('File does not exist, please check you path!')
            return None, None
        sig = madmom.audio.signal.Signal(path)
        num_channels = sig.num_channels
        sample_rate = sig.sample_rate
        # covert analog frequency to digital frequency
        digit_freq_list = []
        if do_filtering:
            num_freq = len(freq_list)
            if num_freq <= 0:
                print('Error, please enter the passband if you want to do filtering')
                return None, None
            for i in range(num_freq):
                tmp_low = 2 * float(freq_list[i][0]) / sample_rate
                tmp_high = 2 * float(freq_list[i][1]) / sample_rate
                digit_freq_list.append([tmp_low, tmp_high])
        
        time_interval = self.hop_size / sample_rate
        
        sf = None
        
        for i in range(num_freq):
            for j in range(num_channels):
                tmp = sig[:, j]
                tmpframe = madmom.audio.signal.FramedSignal(tmp, frame_size = self.frame_size, hop_size = self.hop_size)
                tmpstft = madmom.audio.stft.STFT(tmpframe)
                if do_filtering:
                    if len(digit_freq_list[i]) != 2:
                        print('Error, please enter the passband in the form of [low_freq, high_freq]')
                        return None, None
                    tmp_low = digit_freq_list[i][0]
                    tmp_high = digit_freq_list[i][1]
                    tmpstft = self.filter_signal(tmpstft, tmp_low, tmp_high)
                    
                tmpspec = madmom.audio.spectrogram.Spectrogram(tmpstft)
                tmpdiff = np.zeros(tmpspec.shape)
                tmpdiff[1:] = np.diff(tmpspec, axis = 0)
                tmppos = np.maximum(0, tmpdiff)
                tmpsf = np.sum(tmppos, axis = 1)
                if i == 0 and j == 0:
                    sf = np.expand_dims(tmpsf, axis = 0)
                else:
                    sf = np.append(sf, np.expand_dims(tmpsf, axis = 0), axis = 0) 
        
        return sf, time_interval 

###############################################################################
# Do onset detection using super flux algorithm
# Input： 
#       path: the path of the audio file
#       do_filtering: indicate whether you want to filter the audio signal, please enter the 
#                     band you want to keep in the freq_list if you set it to True
#       freq_list: the bandwidth you want to keep, enter a list, each item in this list 
#                  is in the form of [low_freq, high_freq] 
# Output:
#       sf: the spectral of change according to time;
#           the first dimension is (the number of pass band you want * channels)
#       time_interval: time interval between 2 points in sf         
###############################################################################    
    def superflux(self, path = None, do_filtering = False, freq_list = [[40.0, 200.0]]):
        if path == None:
            print('Enter file name please!')
            return None, None
        if os.path.isfile(path) == False:
            print('File does not exist, please check you path!')
            return None, None
        sig = madmom.audio.signal.Signal(path)
        num_channels = sig.num_channels
        sample_rate = sig.sample_rate
        # covert analog frequency to digital frequency
        digit_freq_list = []
        if do_filtering:
            num_freq = len(freq_list)
            if num_freq <= 0:
                print('Error, please enter the passband if you want to do filtering')
                return None, None
            for i in range(num_freq):
                tmp_low = 2 * float(freq_list[i][0]) / sample_rate
                tmp_high = 2 * float(freq_list[i][1]) / sample_rate
                digit_freq_list.append([tmp_low, tmp_high])
        
        time_interval = self.hop_size / sample_rate
        
        sf = None
        for i in range(num_freq):
            for j in range(num_channels):
                tmp = sig[:, j]
                tmpframe = madmom.audio.signal.FramedSignal(tmp, frame_size = self.frame_size, hop_size = self.hop_size)
                tmpstft = madmom.audio.stft.STFT(tmpframe)
                if do_filtering:
                    if len(digit_freq_list[i]) != 2:
                        print('Error, please enter the passband in the form of [low_freq, high_freq]')
                        return None, None
                    tmp_low = digit_freq_list[i][0]
                    tmp_high = digit_freq_list[i][1]
                    tmpstft = self.filter_signal(tmpstft, tmp_low, tmp_high)
                tmpspec = madmom.audio.spectrogram.Spectrogram(tmpstft)
                tmpfilt_spec = madmom.audio.spectrogram.FilteredSpectrogram(tmpspec, filterbank=madmom.audio.filters.LogFilterbank, num_bands=24)
                tmplog_spec = madmom.audio.spectrogram.LogarithmicSpectrogram(tmpfilt_spec, add=1)
                tmpsize = (1, 3)
                tmpmax_spec = maximum_filter(tmplog_spec, size=tmpsize)
                tmpdiff = np.zeros(tmplog_spec.shape)
                tmpdiff[1:] = (tmplog_spec[1:] - tmpmax_spec[:-1])
                tmppos = np.maximum(0, tmpdiff)
                tmpsf = np.sum(tmppos, axis = 1)
                if i == 0 and j == 0:
                    sf = np.expand_dims(tmpsf, axis = 0)
                else:
                    sf = np.append(sf, np.expand_dims(tmpsf, axis = 0), axis = 0) 
        
        return sf, time_interval


###############################################################################
# Do onset detection using normalized weighted phase deviation algorithm
# Input： 
#       path: the path of the audio file
#       do_filtering: indicate whether you want to filter the audio signal, please enter the 
#                     band you want to keep in the freq_list if you set it to True
#       freq_list: the bandwidth you want to keep, enter a list, each item in this list 
#                  is in the form of [low_freq, high_freq] 
# Output:
#       sf: the spectral of change according to time;
#           the first dimension is (the number of pass band you want * channels)
#       time_interval: time interval between 2 points in nwpd          
###############################################################################
    def normalized_weighted_phase_deviation(self, path = None, do_filtering = False, freq_list = [[40.0, 200.0]]):
        if path == None:
            print('Enter file name please!')
            return None, None
        if os.path.isfile(path) == False:
            print('File does not exist, please check you path!')
            return None, None
        sig = madmom.audio.signal.Signal(path)
        num_channels = sig.num_channels
        sample_rate = sig.sample_rate
        # covert analog frequency to digital frequency
        digit_freq_list = []
        if do_filtering:
            num_freq = len(freq_list)
            if num_freq <= 0:
                print('Error, please enter the passband if you want to do filtering')
                return None, None
            for i in range(num_freq):
                tmp_low = 2 * float(freq_list[i][0]) / sample_rate
                tmp_high = 2 * float(freq_list[i][1]) / sample_rate
                digit_freq_list.append([tmp_low, tmp_high])
        
        time_interval = self.hop_size / sample_rate
        
        nwpd = None
        for i in range(num_freq):
            for j in range(num_channels):
                tmp = sig[:, j]
                tmpframe = madmom.audio.signal.FramedSignal(tmp, frame_size = self.frame_size, hop_size = self.hop_size)
                tmpstft = madmom.audio.stft.STFT(tmpframe)
                if do_filtering:
                    if len(digit_freq_list[i]) != 2:
                        print('Error, please enter the passband in the form of [low_freq, high_freq]')
                        return None, None
                    tmp_low = digit_freq_list[i][0]
                    tmp_high = digit_freq_list[i][1]
                    tmpstft = self.filter_signal(tmpstft, tmp_low, tmp_high)
                tmpphase = madmom.audio.stft.phase(tmpstft)
                tmpphase_diff = np.diff(tmpphase, axis = 0)
                tmpphase_diff_2nd = np.zeros(tmpphase.shape) 
                tmpphase_diff_2nd[2:] = np.diff(tmpphase_diff, axis = 0)
                tmpspec = madmom.audio.spectrogram.Spectrogram(tmpstft)
                tmpwpd = np.sum(np.abs(tmpspec * tmpphase_diff_2nd), axis = 1)
                tmpnormalization = np.sum(np.abs(tmpspec)) 
                tmpnwpd = tmpwpd / tmpnormalization

                if i == 0 and j == 0:
                    nwpd = np.expand_dims(tmpnwpd, axis = 0)
                else:
                    nwpd = np.append(nwpd, np.expand_dims(tmpnwpd, axis = 0), axis = 0) 
        
        return nwpd, time_interval 

    

def test(path):

    print(path)

    myprocessor = onset_detector(2048, 441)
    
    sf, time_interval = myprocessor.process_signal(path, method = 'fake_method', do_filtering = True)

    start = time.time()
    sf, time_interval = myprocessor.process_signal(path, method = 'spectralflux', do_filtering = True)
    print("Running spectral flux use {} seconds.".format(time.time() - start))
    if sf is not None:
        print(sf.shape)
        print(time_interval)
        N = len(sf)
        for i in range(N):
            plt.figure()
            plt.plot(sf[i, : 4000])
            plt.savefig('sf_{}.png'.format(i))

    start = time.time()
    sf, time_interval = myprocessor.process_signal(path, method = 'superflux', do_filtering = True)
    print("Running super flux use {} seconds.".format(time.time() - start))
    if sf is not None:
        print(sf.shape)
        print(time_interval)
        N = len(sf)
        for i in range(N):
            plt.figure()
            plt.plot(sf[i, : 4000])
            plt.savefig('superflux_{}.png'.format(i))
       
    start = time.time()  
    nwpd, time_interval = myprocessor.process_signal(path, method = 'normalized_weighted_phase_deviation', do_filtering = True)
    print("Running normalizaed weighted phase deviation use {} seconds.".format(time.time() - start))
    if nwpd is not None:
        print(nwpd.shape)
        print(time_interval)

        #quantize
        N = len(nwpd)


        #visualize
        for i in range(N):
            nwpd[nwpd < 0.0001] = 0

        for i in range(N):
            plt.figure()
            plt.plot(nwpd[i, :4000])
            plt.savefig('nwpd_{}.png'.format(i))
  
if __name__== '__main__':
    test('../data/beat_it.mp3')
