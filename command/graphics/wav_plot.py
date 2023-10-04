import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator

# plt.style.use('gray-background')


class DrawGraph:
    def __init__(self, miny=-4000, maxy=4000, freq=False):
        if freq:
            self.fig, self.ax = plt.subplots(2, 1, figsize=(16, 7), facecolor="#424242")
            # self.fig, self.ax = plt.subplots(2, 1, figsize=(10, 5), facecolor='#424242')
        else:
            self.fig, self.ax = plt.subplots(1, figsize=(16, 7), facecolor="#424242")
            # self.fig, self.ax = plt.subplots(1, figsize=(10, 5), facecolor="#424242")

        self.miny = miny
        self.maxy = maxy

    def draw_onefunc(self, i, wavx, wavy):
        plt.cla()

        self.ax.set_facecolor("#424242")
        plt.title(
            "Output of sound wave (sampling frequency = 44100 Hz\n",
            loc="left",
            color="w",
            fontsize=20,
        )
        plt.xlabel("Time", color="w", fontsize=12)
        plt.ylabel("Amplitude", color="w", fontsize=12)

        self.ax.set_axisbelow(True)
        self.ax.yaxis.grid(color="#848484", linestyle="solid")
        self.ax.xaxis.grid(color="#848484", linestyle="solid")

        self.ax.spines["right"].set_visible(False)
        self.ax.spines["top"].set_visible(False)
        self.ax.spines["left"].set_color("w")
        self.ax.spines["bottom"].set_color("w")

        plt.xticks(color="w", fontsize=12)
        plt.yticks(color="w")
        self.ax.xaxis.set_major_locator(MultipleLocator(0.25))
        self.ax.xaxis.set_label_coords(0.5, -0.08)
        self.ax.set_ylim((-4000, 4000))

        self.ax.plot(wavx, wavy, linewidth=0.9, color="coral")

    def draw_twofunc(self, i, freq, amp, wavx, wavy):
        minx = np.min(wavx)
        maxx = minx + (np.max(wavx) - minx) / 2

        if i % 3 == 0:
            self.ax[1].cla()
            self.ax[1].set_xlabel("Time")
            self.ax[1].set_ylabel("Amplitude")
            self.ax[1].set_xlim((0, 600))
            self.ax[1].set_ylim((0, 1000000))
            self.ax[1].plot(freq, amp)
        if i % 7 == 0:
            self.ax[0].cla()

        self.ax[0].set_title("Output of sound wave (sampling freqency = 44100 Hz)\n")
        self.ax[0].set_ylabel("Amplitude")
        self.ax[0].xaxis.set_major_locator(MultipleLocator(0.2))
        self.ax[0].set_xlim((minx, maxx))
        self.ax[0].set_ylim((self.miny, self.maxy))
        self.ax[0].plot(wavx, wavy)
