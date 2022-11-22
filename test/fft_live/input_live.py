<<<<<<< HEAD:test_code/fft_live/input_live.py
import pyaudio
import wave
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.ticker import *
import numpy as np
import struct
import time

# plt.style.use('gray-background')

class Fourier:
    def __init__(self, scale, dt):
        self.scale = scale
        self.dt = dt * (10**-3)

    def fourier(self, f): # 人間の可聴域は20~20,000Hz
        byte_col = len(f)
        f_ = np.array([np.frombuffer(f[i], dtype='int16') for i in range(byte_col)]).reshape(-1)
        # f_ = np.delete(f_, np.s_[:10**5]) # 最初の約1秒（ノイズ）は削除
        F  = np.fft.fft(f_)
        _ = int(len(F)/2)

        # 周波数分布を平行移動
        # F_ = np.delete(F, np.s_[_-self.scale:_+self.scale])
        # F_ = np.concatenate([np.zeros(self.scale), F, np.zeros(self.scale)])
        # 周波数分布を定数倍
        zero_ = np.zeros([self.scale, _*2])
        # F_ = np.concatenate([np.array([F]), zero_]).reshape(-1, order='F') # 定数倍したときの隙間は0で補完
        F_ = np.broadcast_to(F, (self.scale,  _*2)).reshape(-1, order='F') # 定数倍したときの隙間は同じ値で補完
        
        inv_F = np.fft.ifft(F_).real #.tobytes()#.reshape([-1, self.culum_num])
        inv_F = np.array(inv_F, dtype='int16')
        binv_F = struct.pack('h' * len(inv_F), *inv_F) #バイナリへ変換
        freq = np.fft.fftfreq(len(f_), self.dt)
        return freq, F, binv_F

class Audio:
    def __init__(self):
        self.chunk = 2**11 #バッファのサイズ
        self.format = pyaudio.paInt16 #量子化ビット数(解像度)　※人間は16 bit 以上は聞き分けが難しくなる
        self.channels = 1 #入力に使用するマイクの本数
        self.rate = 44100 #サンプリング周波数
        self.record_time = 10 #録音時間
        self.interval = 0.1 #グラフを出力する時間間隔 [ms]
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
        #self.frames = []
        self.wavx = np.arange(-self.end_t*(self.scale-1), self.end_t, del_x)
        self.wavy = np.zeros(self.audio.chunk * self.scale)

    def draw_init(self, ax):
        ax.set_xlabel('Time')
        ax.set_ylabel('Amplitude')
            
    def draw(self):
        def plot(i):
            data = self.audio.stream.read(self.audio.chunk)
            wavy_ = np.frombuffer(data, dtype='int16')
            self.wavy = np.delete(self.wavy, np.s_[:self.audio.chunk])
            self.wavy = np.append(self.wavy, wavy_)
            self.wavx += self.end_t
            # if i%self.scale == 0:
            freq, F, binv_F = f.fourier(wavy_)
            amp = np.abs(F)
            frames.append(binv_F)
            
            # リアルタイムでグラフ表示
                
            if i%5 == 0:
                ax[0].cla()

            if i%3 == 0:
                ax[1].cla()
                self.draw_init(ax[1])
                ax[1].set_xlim((0,1000))
                ax[1].set_ylim((0,1000000))
                ax[1].plot(freq, amp)

            ax[0].set_title('Output of sound wave (sampling frequency = 44100 Hz)\n')
            self.draw_init(ax[0])
            ax[0].xaxis.set_major_locator(MultipleLocator(0.2)) # x座標のメモリの設定
            ax[0].set_xlim((np.min(self.wavx), np.max(self.wavx)))
            ax[0].set_ylim((-10000, 10000))
            ax[0].plot(self.wavx, self.wavy)

        f = Fourier(scale=2, dt=self.audio.interval)

        frames = []
        fig, ax = plt.subplots(2, 1, figsize=(16,7), facecolor="#424242")

        print("Recording ...")

        ani = animation.FuncAnimation(fig, plot, interval = self.audio.interval)
        #ani.save("./data/output.gif", writer="imagemagick")
        plt.show()

        print("Done.")

        return frames

    def write(self, frames): # データの書き込み
        wf = wave.open(self.audio.output_path, 'wb')
        wf.setnchannels(self.audio.channels)
        wf.setsampwidth(self.audio.p.get_sample_size(self.audio.format))
        wf.setframerate(self.audio.rate*2)
        # wf.setframerate(self.audio.rate)
        # wf.writeframes(frames)
        wf.writeframes(b''.join(frames))
        wf.close()

if __name__=="__main__":
    audio = Audio()
    # f = Fourier(scale=100, dt=audio.interval)
    output=Output(audio)
    frames = output.draw()
    # freq, F, binv_F = f.fourier(frames)
    output.write(frames)
    audio.exit()

    # plt.xlim(0,5000)
    # plt.plot(freq, F)
=======
import pyaudio
import wave
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.ticker import *
import numpy as np
import struct
import time

plt.style.use('gray-background')

class Fourier:
    def __init__(self, scale, dt):
        self.scale = scale
        self.dt = dt * (10**-3)

    def fourier(self, f): # 人間の可聴域は20~20,000Hz
        byte_col = len(f)
        f_ = np.array([np.frombuffer(f[i], dtype='int16') for i in range(byte_col)]).reshape(-1)
        # f_ = np.delete(f_, np.s_[:10**5]) # 最初の約1秒（ノイズ）は削除
        F  = np.fft.fft(f_)
        _ = int(len(F)/2)

        # 周波数分布を平行移動
        # F_ = np.delete(F, np.s_[_-self.scale:_+self.scale])
        # F_ = np.concatenate([np.zeros(self.scale), F, np.zeros(self.scale)])
        # 周波数分布を定数倍
        zero_ = np.zeros([self.scale, _*2])
        # F_ = np.concatenate([np.array([F]), zero_]).reshape(-1, order='F') # 定数倍したときの隙間は0で補完
        F_ = np.broadcast_to(F, (self.scale,  _*2)).reshape(-1, order='F') # 定数倍したときの隙間は同じ値で補完
        
        inv_F = np.fft.ifft(F_).real #.tobytes()#.reshape([-1, self.culum_num])
        inv_F = np.array(inv_F, dtype='int16')
        binv_F = struct.pack('h' * len(inv_F), *inv_F) #バイナリへ変換
        freq = np.fft.fftfreq(len(f_), self.dt)
        return freq, F, binv_F

class Audio:
    def __init__(self):
        self.chunk = 2**11 #バッファのサイズ
        self.format = pyaudio.paInt16 #量子化ビット数(解像度)　※人間は16 bit 以上は聞き分けが難しくなる
        self.channels = 1 #入力に使用するマイクの本数
        self.rate = 44100 #サンプリング周波数
        self.record_time = 10 #録音時間
        self.interval = 0.1 #グラフを出力する時間間隔 [ms]
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
        #self.frames = []
        self.wavx = np.arange(-self.end_t*(self.scale-1), self.end_t, del_x)
        self.wavy = np.zeros(self.audio.chunk * self.scale)

    def draw_init(self, ax):
        ax.set_xlabel('Time')
        ax.set_ylabel('Amplitude')
            
    def draw(self):
        def plot(i):
            data = self.audio.stream.read(self.audio.chunk)
            wavy_ = np.frombuffer(data, dtype='int16')
            self.wavy = np.delete(self.wavy, np.s_[:self.audio.chunk])
            self.wavy = np.append(self.wavy, wavy_)
            self.wavx += self.end_t
            # if i%self.scale == 0:
            freq, F, binv_F = f.fourier(wavy_)
            amp = np.abs(F)
            # frames.append(binv_F)
            
            # リアルタイムでグラフ表示
                
            if i%5 == 0:
                ax[0].cla()

            if i%3 == 0:
                ax[1].cla()
                self.draw_init(ax[1])
                ax[1].set_xlim((0,600))
                ax[1].set_ylim((0,1000000))
                ax[1].plot(freq, amp)

            ax[0].set_title('Output of sound wave (sampling frequency = 44100 Hz)\n')
            ax[0].set_ylabel('Amplitude')
            ax[0].xaxis.set_major_locator(MultipleLocator(0.2)) # x座標のメモリの設定
            minx = np.min(self.wavx)
            maxx = minx + (np.max(self.wavx) - minx)/2
            ax[0].set_xlim((minx, maxx))
            ax[0].set_ylim((-40000, 40000))
            ax[0].plot(self.wavx, self.wavy)

        f = Fourier(scale=2, dt=self.audio.interval)

        # frames = []
        fig, ax = plt.subplots(2, 1, figsize=(16,7), facecolor="#424242")

        print("Recording ...")

        ani = animation.FuncAnimation(fig, plot, interval = self.audio.interval)
        #ani.save("./data/output.gif", writer="imagemagick")
        plt.show()

        print("Done.")

        # return frames

    def write(self, frames): # データの書き込み
        wf = wave.open(self.audio.output_path, 'wb')
        wf.setnchannels(self.audio.channels)
        wf.setsampwidth(self.audio.p.get_sample_size(self.audio.format))
        wf.setframerate(self.audio.rate*2)
        # wf.setframerate(self.audio.rate)
        # wf.writeframes(frames)
        wf.writeframes(b''.join(frames))
        wf.close()

if __name__=="__main__":
    audio = Audio()
    # f = Fourier(scale=100, dt=audio.interval)
    output=Output(audio)
    frames = output.draw()
    # freq, F, binv_F = f.fourier(frames)
    # output.write(frames)
    audio.exit()

    # plt.xlim(0,5000)
    # plt.plot(freq, F)
>>>>>>> 539d7b0c1a348a012d6824d53c2d42870f691c9f:test/fft_live/input_live.py
    # plt.show()