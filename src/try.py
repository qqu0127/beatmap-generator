# -*- coding: utf-8 -*-
"""
Created on Wed May  2 23:19:28 2018

@author: zhuya
"""
import matplotlib
matplotlib.use('Agg')
import numpy as np
import madmom
import matplotlib.pyplot as plt
#import signal
sig = madmom.audio.signal.Signal("../data/beat_it.mp3")

left_channel = sig[:,0]
right_channel = sig[:,1]

diff = np.abs(left_channel) - np.abs(right_channel)
sample_rate = sig.sample_rate

N = len(left_channel)
t = 1.0 / sample_rate * np.arange(N, dtype = np.float32)

'''
#check its spectrogram
left_f = np.fft.fft(left_channel)
right_f = np.fft.fft(right_channel)
Nf = len(left_channel)
f = (np.arange(Nf, dtype = np.float32) - Nf * 0.5) * 1.0 / Nf * sample_rate
plt.figure()
plt.plot(f, np.abs(left_f))
plt.savefig('left_f.png')
plt.show()

plt.figure()
plt.plot(f, np.abs(right_f))
plt.savefig('right_f.png')
plt.show()
'''

#do stft
left_frame = madmom.audio.signal.FramedSignal(left_channel, frame_size = 2048, hop_size = 441)
right_frame = madmom.audio.signal.FramedSignal(right_channel, frame_size = 2048, hop_size = 441)

left_stft = madmom.audio.stft.STFT(left_frame)
right_stft = madmom.audio.stft.STFT(right_frame)

left_spec = madmom.audio.spectrogram.Spectrogram(left_stft)
right_spec = madmom.audio.spectrogram.Spectrogram(right_stft)

print(left_frame.shape)
print(left_stft.shape)
print(left_spec.shape)


#how to add value to the axis
plt.figure()
plt.imshow(left_spec[:200,: 200].T, aspect = 'auto', origin = 'lower')
plt.savefig('left_spec.png')
plt.figure()
plt.imshow(right_spec[:200,: 200].T, aspect = 'auto', origin = 'lower')
plt.savefig('right_spec.png')

left_diff = np.diff(left_spec, axis = 0)
right_diff = np.diff(right_spec, axis = 0)
left_pos = np.maximum(0, left_diff)
right_pos = np.maximum(0, right_diff)
left_sf = np.sum(left_pos, axis = 1)
right_sf = np.sum(right_pos, axis = 1)

plt.figure()
plt.plot(left_sf[5000: 5200])
plt.savefig('left_sf.png')

plt.figure()
plt.plot(right_sf[5000: 5200])
plt.savefig('right_sf.png')

