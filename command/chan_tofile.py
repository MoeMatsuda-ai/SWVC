from .transform.chanfreq import *
from .audio import Moyaudio
import wave

class TransformCl:
    def transform(self, tofile_origin=False, tofile_chan=False,
                  type="mult", ps_scale=50, mult_scale=1.5,
                  record_time=5, graph=False, 
                  original_path="./data/original_data.wav", change_path="./data/change_data.wav"):
        self.original_path = original_path
        self.change_path = change_path
        self.tofile_origin = tofile_origin
        self.tofile_chan = tofile_chan
        if type=="mult":
            if mult_scale > 1:
                au = Moyaudio(chunk=2**11+1000)
                print(mult_scale)
            else:
                au = Moyaudio(chunk=2**14)
        else :
            au = Moyaudio(chunk=2**12)
        self.cf = ChangeFreq(audio=au, record_time=record_time)
        F,F_ = self.cf.read(tofile_origin=tofile_origin, tofile_chan=tofile_chan,
                type=type, ps_scale=ps_scale, mult_scale=mult_scale, 
                original_path=original_path, change_path=change_path)
        if graph:
            fg = plt.figure(figsize=(10, 5))
            ax1 = fg.add_subplot(2, 1, 1)
            ax2 = fg.add_subplot(2,1,2)
            ax1.plot(F)
            ax2.plot(F_)
            plt.show()
        print("Done.")

    def write(self):
        print("Outpudding")
        if self.tofile_chan:
            au = Moyaudio()
            with wave.open(self.change_path, 'rb') as wf:
                data = wf.readframes(au.chunk)
                while len(data):
                    au.stream.write(data)
                    data = wf.readframes(au.chunk)
            au.autostop()
        else:
            self.cf.ma.output(self.cf.tr_frames)
        self.cf.ma.autostop()
        print("Done.")

if __name__=='__main__':
    TransformCl().transform(tofile_origin=True, tofile_chan=True, 
                type="ps", ps_scale=50, mult_scale=1.5, record_time=10)
