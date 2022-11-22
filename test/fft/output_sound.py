import pyaudio
import wave
 
CHUNK_SIZE = 2**10
output_path = "./data/output.wav"

wf = wave.open(output_path, 'rb')
p = pyaudio.PyAudio()
stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                channels=wf.getnchannels(),
                rate=wf.getframerate(),
                output=True)

# 再生
data = wf.readframes(CHUNK_SIZE)
while len(data):
    stream.write(data)
    data = wf.readframes(CHUNK_SIZE)
 
stream.stop_stream()
stream.close()
p.terminate()
