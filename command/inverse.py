import sys
import wave
import numpy as np
import time
from .audio import Moyaudio

class InverseAudio:
    def inverse(self, record_time=5, speed=1.0, 
                tofile_origin=False, tofile_chan=False, inv=True,
                original_path="./data/original_data.wav", 
                change_path="./data/inverse_data.wav"):
        self.ma = Moyaudio()
        self.record_time = record_time
        self.speed = speed
        self.del_x = 1/self.ma.rate
        self.end_t = self.del_x * self.ma.chunk
        self.frames = []
        
        self.original_path = original_path
        self.change_path = change_path
        self.tofile_chan = tofile_chan
        self.tofile_origin = tofile_origin

        print("Recording...")
        for i in range(0, int(self.ma.rate / self.ma.chunk * self.record_time)):
            binary,  data = self.ma.input()
            self.frames.append(data)
        
        print("Done.")
        
        if tofile_origin:
            print(f"Saved original data to {original_path}")
            self.ma.write(self.frames, output_file=original_path)
        self.frames = np.array(self.frames)

        if inv:
            self.inv_frames = np.fliplr(np.flipud(self.frames)).copy()
            self.ma.autostop()
        else:
            self.inv_frames = self.frames
            self.ma.autostop()
            
        au = Moyaudio(rate=int(self.ma.rate*self.speed))
        if self.tofile_chan:
            print(f"Saved transformed data to {self.change_path}")
            au.write(self.inv_frames, output_file=self.change_path)
        au.autostop()
        
        return self.inv_frames

    def write(self):
        print("Outpudding")
        au = Moyaudio(rate=int(self.ma.rate*self.speed))

        if self.tofile_chan:
            with wave.open(self.change_path, 'rb') as wf:
                data = wf.readframes(au.chunk)
                while len(data):
                    au.stream.write(data)
                    data = wf.readframes(au.chunk)
        else:
            au.output(self.inv_frames)
        
        au.autostop()
        print("Done.")

if __name__=="__main__":
    inv = InverseAudio()
    inv.inverse(tofile_chan=True, tofile_origin=True, speed=1)
    inv.write()
    
