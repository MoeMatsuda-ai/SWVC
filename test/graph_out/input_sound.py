from email.mime import audio
from turtle import color
import pyaudio
import wave
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.ticker import *
import numpy as np

class Audio:
    def __init__(self):
        self.chunk = 2**11 #バッファのサイズ
        self.format = pyaudio.paInt16 #量子化ビット数(解像度)　※人間は16 bit 以上は聞き分けが難しくなる
        self.channels = 1 #入力に使用するマイクの本数
        self.rate = 44100 #サンプリング周波数
        self.record_time = 10 #録音時間
        self.interval = 0.01 #グラフを出力する時間間隔
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
        self.frames = []
        self.wavx = np.arange(-self.end_t*(self.scale-1), self.end_t, del_x)
        self.wavy = np.zeros(self.audio.chunk * self.scale)
        
    def draw(self):
        def plot(i):
            data = self.audio.stream.read(self.audio.chunk)
            self.frames.append(data)

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

        fig, ax = plt.subplots(1, figsize=(16, 7), facecolor="#424242")
        
        print("Recording ...")

        ani = animation.FuncAnimation(fig, plot, interval = self.audio.interval)
        #ani.save("./data/output.gif", writer="imagemagick")
        plt.show()

        print("Done.")

    def write(self): # データの書き込み
        wf = wave.open(self.audio.output_path, 'wb')
        wf.setnchannels(self.audio.channels)
        wf.setsampwidth(self.audio.p.get_sample_size(self.audio.format))
        wf.setframerate(self.audio.rate)
        wf.writeframes(b''.join(self.frames))
        wf.close()

if __name__=="__main__":
    audio = Audio()
    output=Output(audio)
    output.draw()
    output.write()
    audio.exit()