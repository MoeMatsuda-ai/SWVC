import pyaudio
import wave
import numpy as np


class Moyaudio:
    def __init__(
        self,
        chunk=2**10,
        format=pyaudio.paInt16,
        channels=1,
        rate=44100,
        record_time=10,
        interval=0.1,
    ):
        self.chunk = chunk
        self.format = format
        self.channels = channels
        self.rate = rate
        self.record_time = record_time
        self.interval = interval

        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(
            format=self.format,
            channels=self.channels,
            rate=self.rate,
            input=True,
            output=True,
            frames_per_buffer=self.chunk,
        )

    def input(self):
        data = self.stream.read(self.chunk)
        wav = np.frombuffer(data, dtype="int16")
        return data, wav

    def output(self, f):
        f = np.array(f, dtype="int16")
        b_data = b"".join(f)
        self.stream.write(b_data)

    def write(
        self,
        frames,
        output_file="./data/output.wav",
        change_freq="False",
        freq_mult=1,
        new_rate=44100,
    ):
        wf = wave.open(output_file, "wb")
        wf.setnchannels(self.channels)
        wf.setsampwidth(self.p.get_sample_size(self.format))
        if change_freq == "mult":
            wf.setframerate(self.rate * freq_mult)
        elif change_freq == "ps":
            wf.setframerate(new_rate)
        elif change_freq == "False":
            wf.setframerate(self.rate)
        else:
            wf.setframerate(self.rate)
            print("Error : change_freq is invalid value")
        wf.writeframes(b"".join(frames))
        wf.close()

    def autostop(self):
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()
