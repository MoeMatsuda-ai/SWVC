import pyaudio
import wave
 
CHUNK = 2**10 #バッファのサイズ(リアルタイムに処理したいときは値を小さくする。)
FORMAT = pyaudio.paInt16 #量子化ビット数(解像度)　※人間は16 bit 以上は聞き分けが難しくなる
CHANNELS = 1 #入力に使用するマイクの本数
RATE = 44100 #サンプリング周波数
record_time = 5 #録音時間
output_path = "./data/output.wav" #データ出力するファイル名
 
p = pyaudio.PyAudio() #インスタンスの設定
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK) #パラメータの設定
 
print("Recording ...")

# 録音
frames = []
for i in range(0, int(RATE / CHUNK * record_time)):
    data = stream.read(CHUNK)
    frames.append(data)
print("Done.")
stream.stop_stream()
stream.close()
p.terminate()

# データの書き込み
wf = wave.open(output_path, 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(p.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(b''.join(frames))
wf.close()