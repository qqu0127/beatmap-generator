# -*- coding: utf-8 -*-
"""
Created on Thu May  3 23:33:23 2018

@author: yaxuan zhu
"""

import numpy as np
import madmom
import os
import matplotlib.pyplot as plt

class audio_processor(object):
    def __init__(self, frame_size = 2048, hop_size = 441):
        self.frame_size = frame_size
        self.hop_size = hop_size
    
###########################################
# Do onset detection using spectral flux algorithm
# Input： 
#       path: the path of the audio file
# Output:
#       sf: the spectral of change according to time;
#           the first dimension correspond to the channels
#       sample_rate: sample rate of the signal        
###########################################    
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
        
        sf = None
        for i in range(num_channels):
            tmp = sig[:, i]
            tmpframe = madmom.audio.signal.FramedSignal(tmp, frame_size = self.frame_size, hop_size = self.hop_size)
            tmpstft = madmom.audio.stft.STFT(tmpframe)
            tmpspec = madmom.audio.spectrogram.Spectrogram(tmpstft)
            tmpdiff = np.diff(tmpspec, axis = 0)
            tmppos = np.maximum(0, tmpdiff)
            tmpsf = np.sum(tmppos, axis = 1)
            if i == 0:
                sf = np.expand_dims(tmpsf, axis = 0)
            else:
                sf = np.append(sf, np.expand_dims(tmpsf, axis = 0), axis = 0) 
        
        return sf, sample_rate 
    

def test(path):
    myprocessor = audio_processor(2048, 441)
    sf, sample_rate = myprocessor.spectralflux(path)
    
    print(sf.shape)
    N = len(sf)
    for i in range(N):
        plt.figure()
        plt.plot(sf[i, : 2000])
        plt.savefig('sf_{}.png'.format(i))

if __name__== '__main__':
    test('beat_it.mp3')