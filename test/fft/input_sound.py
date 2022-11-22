# from email.mime import audio
# from tkinter import Frame, Scale
# from turtle import color
# from typing import Concatenate
# from distutils.file_util import write_file
import pyaudio
import wave
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.ticker import *
import numpy as np
import struct

class Fourier:
    def __init__(self, scale, dt):
        self.scale = scale
        self.dt = dt * (10**-3)

    def fourier(self, f): # 人間の可聴域は20~20,000Hz
        byte_col = len(f)
        f_ = np.array([np.frombuffer(f[i], dtype='int16') for i in range(byte_col)]).reshape(-1)
        f_ = np.delete(f_, np.s_[:10**5]) # 最初の約1秒（ノイズ）は削除
        freq = np.fft.fftfreq(len(f_), self.dt) # 周波数軸
        F  = np.fft.fft(f_)

        _ = int(len(F)/2)

        # 周波数分布を平行移動
        F_ = np.delete(F, np.s_[_-self.scale:_+self.scale])
        F_ = np.concatenate([np.zeros(self.scale), F, np.zeros(self.scale)])
        # 周波数分布を定数倍
        # zero_ = np.zeros([self.scale, _*2])
        # F_ = np.concatenate([np.array([F]), zero_]).reshape(-1, order='F') # 定数倍したときの隙間は0で補完
        # F_ = np.broadcast_to(F, (self.scale,  _*2)).reshape(-1, order='F') # 定数倍したときの隙間は同じ値で補完
        
        fig = plt.figure(figsize=(10, 10))
        ax1 = fig.add_subplot(211)
        ax2 = fig.add_subplot(212)
        ax1.plot(F)
        ax2.plot(F_)
        ax1.set_xlim(0, 10000)
        ax2.set_xlim(0, 10000)
        # ax1.plot(freq, F)
        # ax2.plot(freq, F)
        #ax2.plot(F[_-25000:_+25000])
        plt.show()

        inv_F = np.fft.ifft(F_)#.tobytes()#.reshape([-1, self.culum_num])
        inv_F = np.array(inv_F, dtype='int16')
        binv_F = struct.pack('h' * len(inv_F), *inv_F) #バイナリへ変換
        return freq, F, inv_F, binv_F

class Audio:
    def __init__(self):
        self.chunk = 2**11 #バッファサイズ
        self.format = pyaudio.paInt16 #量子化ビット数 ※人間は16 bit 以上は聞き分けが難しくなる
        self.channels = 1 #入力に使用するマイクの本数
        self.rate = 44100 #サンプリング周波数
        self.record_time = 10 #録音時間
        self.interval = 0.01 #グラフを出力する時間間隔 [ms]
        self.output_path = "./data/output.wav" #データ出力するファイル名

        self.p = pyaudio.PyAudio() #インスタンスの設定
        self.stream = self.p.open(format=self.format,
                        channels=self.channels,
                        rate=self.rate,
                        input=True,
                        frames_per_buffer=self.chunk) #パラメータの設定

    def exit(self):
        self.stream.stop_stream() # 再生・録音の一時停止
        self.stream.close() # ストリームの終了
        self.p.terminate() # インスタンスの破棄


class Output:
    def __init__(self, audio):
        self.audio = audio
        del_x = 1/self.audio.rate
        self.end_t = del_x*self.audio.chunk
        self.scale = 5
        self.bf = []
        self.wavx = np.arange(-self.end_t*(self.scale-1), self.end_t, del_x)
        self.wavy = np.zeros(self.audio.chunk * self.scale)
        
    def draw(self):
        def plot(i):
            data = self.audio.stream.read(self.audio.chunk)
            self.bf.append(data)

            wavy_ = np.frombuffer(data, dtype='int16')
            self.wavy = np.delete(self.wavy, np.s_[:self.audio.chunk])
            self.wavy = np.append(self.wavy, wavy_)

            # リアルタイムでグラフ表示 <- 横軸どうするか…
            plt.cla()
            # title & label
            ax.set_facecolor("#424242")
            plt.title('Output of sound wave (sampling frequency = 44100 Hz)\n', 
                loc='left', color='w', fontsize = 20)
            plt.xlabel('Time', color='w', fontsize=12)
            plt.ylabel('Amplitude', color='w', fontsize=12)
            # grid
            ax.set_axisbelow(True)
            ax.yaxis.grid(color='#848484', linestyle='solid')
            ax.xaxis.grid(color='#848484', linestyle='solid')
            # spines
            ax.spines['right'].set_visible(False)
            ax.spines['top'].set_visible(False)
            ax.spines['left'].set_color('w')
            ax.spines['bottom'].set_color('w')
            # ticks
            plt.xticks(color='w', fontsize=12)
            plt.yticks(color='w')
            ax.xaxis.set_major_locator(MultipleLocator(0.25)) # x座標のメモリの設定
            ax.set_ylim((-10000, 10000))

            ax.plot(self.wavx, self.wavy, linewidth = 0.8, color='coral')

            self.wavx += self.end_t

        self.bf = []
        fig, ax = plt.subplots(1, figsize=(16, 7), facecolor="#424242")
        
        print("Recording ...")

        ani = animation.FuncAnimation(fig, plot, interval = self.audio.interval) # リアルタイムで出力
        #ani.save("./data/output.gif", writer="imagemagick") # 動画として保存
        plt.show()

        print("Done.")

    def write(self, frames): # データの書き込み
        write_f = wave.open(self.audio.output_path, 'wb')
        write_f.setnchannels(self.audio.channels)
        write_f.setsampwidth(self.audio.p.get_sample_size(self.audio.format))
        write_f.setframerate(self.audio.rate)
        write_f.writeframes(frames)
        #write_f.writeframes(b''.join(frames))
        write_f.close()

if __name__=="__main__":
    audio = Audio()
    f = Fourier(scale=5000, dt=audio.interval) # scale -> 周波数分布を変える目安
    output=Output(audio)
    output.draw()
    freq, F, inv_F, binv_F = f.fourier(output.bf)
    output.write(binv_F)
    audio.exit()