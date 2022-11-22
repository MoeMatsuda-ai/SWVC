from tracemalloc import start
import pyaudio
import wave
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.ticker import *
import numpy as np
import struct
import time
from scipy import interpolate

plt.style.use('gray-background')

class Fourier:
    def __init__(self, scale, dt):
        self.scale = scale

    def fourier(self, f): # 人間の可聴域は20~20,000Hz
        f = np.array([f]).reshape(-1)
        len_f = len(f)
        # resize
        inv_F_ = np.resize(f, int(len_f*self.scale))
        # リサンプリング
        t = np.arange(0, len(inv_F_))
        f_linear = interpolate.interp1d(t, inv_F_, kind='cubic')
        t = np.arange(0, len(inv_F_)-1.0, self.scale)
        inv_F_ = f_linear(t)
        inv_F_ = np.array(inv_F_, dtype='int16')
        binv_F = struct.pack('h' * len(inv_F_), *inv_F_) #バイナリへ変換
        return binv_F

class Audio:
    def __init__(self, chunk=2**10, format=pyaudio.paInt16, channels=1, rate=44100,
     record_time=50, interval=0.01, output_path="./data/output.wav"):

        self.chunk = chunk #バッファのサイズ
        self.format = format #量子化ビット数(解像度)　※人間は16 bit 以上は聞き分けが難しくなる
        self.channels = channels #入力に使用するマイクの本数
        self.rate = rate #サンプリング周波数
        self.record_time = record_time #録音時間
        self.interval = interval #グラフを出力する時間間隔 [ms]
        self.output_path = output_path #データ出力するファイル名

        self.p = pyaudio.PyAudio() #インスタンスの設定
        self.stream = self.p.open(format=self.format,
                        channels=self.channels,
                        rate=self.rate,
                        input=True, output=True,
                        frames_per_buffer=self.chunk) #パラメータの設定

    def exit(self):
        self.stream.stop_stream() # 再生・録音の一時停止
        self.stream.close() # ストリームの終了
        self.p.terminate() # インスタンスの破棄


class Output:
    def __init__(self, audio, scale=1):
        self.audio = audio
        del_x = 1/self.audio.rate
        self.end_t = del_x*self.audio.chunk
        self.scale = scale
        #self.frames = []

    def draw_init(self, ax):
        ax.set_xlabel('Time')
        ax.set_ylabel('Amplitude')
            
    def draw(self):
        frames = []
        f = Fourier(scale=self.scale, dt=self.audio.interval)
        print("Recording ...")

        # for i in range(0, int(self.audio.rate / self.audio.chunk * self.audio.record_time)):
        while self.audio.stream.is_active():
            data = self.audio.stream.read(self.audio.chunk)    

            wavy_ = np.frombuffer(data, dtype='int16')
            binv_F = f.fourier(wavy_)
            self.audio.stream.write(binv_F)

            # frames.append(binv_F)
            
        print("Done.")

        return frames

    def write(self, frames): # データの書き込み
        wf = wave.open(self.audio.output_path, 'wb')
        wf.setnchannels(self.audio.channels)
        wf.setsampwidth(self.audio.p.get_sample_size(self.audio.format))
        wf.setframerate(self.audio.rate*self.scale)
        wf.writeframes(b''.join(frames))
        wf.close()

if __name__=="__main__":
    scale = 2.0
    audio = Audio()
    output=Output(audio, scale=scale)
    frames = output.draw()
    # output.write(frames)
    audio.exit()