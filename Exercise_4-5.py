# -*- coding: utf-8 -*-
"""
Created on Fri Dec 30 23:22:41 2016
Think DSP Exercise 4-5
@author: Stephen West
"""

import thinkdsp as td
import thinkplot as tp
import numpy as np


def bartlett_method(wave, seg_length=512, win_flag=True):
    """Estimates the power spectrum of a noise wave.
    
    wave: Wave
    seg_length: segment length
    """
    # make a spectrogram and extract the spectrums
    spectro = wave.make_spectrogram(seg_length, win_flag)
    spectrums = spectro.spec_map.values()
    
    # extract the power array from each spectrum
    psds = [spectrum.power for spectrum in spectrums]
    
    # compute the root mean power (which is like an amplitude)
    hs = np.sqrt(sum(psds) / len(psds))
    fs = next(iter(spectrums)).fs
    
    # make a Spectrum with the mean amplitudes
    spectrum = td.Spectrum(hs, fs, wave.framerate)
    return spectrum
    

class VossPinkNoise(td._Noise):
    
    def evaluate(self,ts):
        ''' uses voss_mcartney_algo to generate pink noise '''
        
        # Determine number of rows needed, need 1 for each bit in size of ts
        # if len(ts) is 6 need 3 bits, if len(ts) = n need log2(n) bits
        temp = 0x80
        num_rows = 0
        while not temp & len(ts):
            temp = temp>>1
        #counts sig bit bits in temp
        while temp & 0xFF:
            temp = temp>>1
            num_rows += 1
        
        #create array with all 0s 
        rows = np.zeros((num_rows,len(ts)))
        # IAW Voss-Mcartney Algo
        # elements in row 0 change every time
        # elements in row 1 change every other time
        # elements in row 2 change every 4th time
        # eleemnts in row i change every 1<<i th time
        for i in range(num_rows):
            cntr = 0
            tst = 0x01<<i
            for j in range(len(ts)):
                cntr += 1
                if cntr == tst or j == 0:
                    temp = np.random.uniform(-self.amp,self.amp)
                    cntr = 0
                rows[i][j] = temp
                    
        #initialize ys with array of size len(ts) filled with 0s
        ys = np.zeros(len(ts))
        
        #every element y[i] is the sum of the coulmn rows[i]
        for i in range(len(ts)):    
            for j in range(num_rows):
                ys[i] += rows[j][i]
        return ys
            
sig = VossPinkNoise()
wave = sig.make_wave(duration=10)
spect = wave.make_spectrum()
spect.plot_power()
tp.config(ylabel='Power',xlabel='Frequency (Hz)',xscale='log',yscale='log')
tp.show()

# resulting slope is around -1
print(spect.estimate_slope().slope)

spect = bartlett_method(wave)
spect.plot(high=100000,linewidth=1)
tp.config(ylabel='Power',xlabel='Frequency (Hz)',xscale='log',yscale='log')
tp.show()
print(spect.estimate_slope().slope)