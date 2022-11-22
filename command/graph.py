from decimal import Clamped
from re import T
import sys
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.ticker import *
import numpy as np
import time
from .graphics import *
from .audio import Moyaudio

class GraphOut:
    def __init__(self, scale=5, freq=True):
        self.ma = Moyaudio(rate=11000)
        self.freq = freq
        self.dg = DrawGraph(freq=freq)
        
        self.scale = scale
        self.del_x = 1/self.ma.rate
        self.end_t = self.del_x * self.ma.chunk
        self.frames = []
        self.wavx = np.arange(- self.end_t * (self.scale - 1), self.end_t, self.del_x)
        self.wavy = np.zeros(self.ma.chunk * self.scale)

    def draw_wave(self, write=False):
        def plot(i):
            data, wavy = self.ma.input()
            self.frames.append(data)
            self.wavx += self.end_t
            self.wavy = np.delete(self.wavy, np.s_[:self.ma.chunk])
            self.wavy = np.append(self.wavy, wavy)
            self.dg.draw_onefunc(i, self.wavx, self.wavy)
        
        ani = animation.FuncAnimation(self.dg.fig, plot, interval=self.ma.interval)
        plt.show()
        if write:
            self.ma.write(self.frames)

    def draw_wave_freq(self, write=False):
        def plot(i):
            data, wavy = self.ma.input()
            self.frames.append(data)
            self.wavx += self.end_t
            self.wavy = np.delete(self.wavy, np.s_[:self.ma.chunk])
            self.wavy = np.append(self.wavy, wavy)
            dt = self.ma.interval*(10**-3)
            amp = np.fft.fft(wavy)
            freq = np.fft.fftfreq(len(wavy), dt)
            self.dg.draw_twofunc(i, freq, amp, self.wavx, self.wavy)

        ani = animation.FuncAnimation(self.dg.fig, plot, interval=self.ma.interval)
        plt.show()
        if write:
            self.ma.write(self.frames)

class Startgp:
    def plot_graph(self, scale=5, freq=True):
        gp = GraphOut(scale=scale, freq=freq)
        if freq:
            gp.draw_wave_freq()
        else:
            gp.draw_wave()
        gp.ma.autostop()
        print("Done.")

if __name__=='__main__':
    stgp = Startgp()
    if len(sys.argv) >= 2 and sys.argv[1]=='freq': 
        stgp.plot_graph(freq=True)
    else: 
        stgp.plot_graph(freq=False)
