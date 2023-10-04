import numpy as np
from scipy import interpolate


class Transdata:
    def parallel_shift(data, ps_scale=100, dt=10**-3):
        f = np.array(data).reshape(-1)
        F = np.fft.fft(f)
        F[0] = 0
        mid = int(len(F) / 2)
        if ps_scale <= 0:
            F_ = np.delete(F, np.s_[:(-ps_scale)])
            F_ = np.delete(F_, np.s_[-(-ps_scale):])
            F_ = np.concatenate([F_[:mid], np.zeros((-ps_scale) * 2), F_[mid + 1 :]])
        elif ps_scale > 0:
            F_ = np.delete(F, np.s_[mid - ps_scale : mid + ps_scale])
            F_ = np.concatenate([np.zeros(ps_scale), F_, np.zeros(ps_scale)])
        inv_F = np.fft.ifft(F_).real
        inv_F = inv_F.astype("int16")
        freq = np.fft.fftfreq(len(f), dt)
        return freq, inv_F, F, F_

    def const_multi(data, mult_scale=1.2):
        f = np.array(data).reshape(-1)
        len_f = len(f)
        inv_F_ = np.resize(f, int(len_f * mult_scale))
        t = np.arange(0, len(inv_F_))
        f_linear = interpolate.interp1d(t, inv_F_, kind="cubic")
        t = np.arange(0, len(inv_F_) - 1.0, mult_scale)
        inv_F_ = f_linear(t)
        inv_F_ = np.array(inv_F_, dtype="int16")
        F = np.fft.fft(f)
        F_ = np.fft.fft(inv_F_)
        return inv_F_, F, F_


class ChangeFreq:
    def __init__(self, audio, type="mult", record_time=5):
        self.ma = audio
        self.type = type
        self.record_time = record_time
        self.del_x = 1 / self.ma.rate
        self.end_t = self.del_x * self.ma.chunk
        self.frames = []
        self.tr_frames = []

    def read(
        self,
        tofile_origin=False,
        tofile_chan=False,
        type="mult",
        ps_scale=50,
        mult_scale=1.5,
        original_path="./data/original_data.wav",
        change_path="./data/change_data.wav",
    ):
        print("Recording...")
        for i in range(0, int(self.ma.rate / self.ma.chunk * self.record_time)):
            binary, data = self.ma.input()
            self.frames.append(data)

        print("Done.")

        if tofile_origin:
            print(f"Saved original data to {original_path}")
            self.ma.write(self.frames, output_file=original_path)
        self.frames = np.array(self.frames)

        if type == "mult":
            for i, ordata in enumerate(self.frames):
                trans_F, F, F_ = Transdata.const_multi(ordata, mult_scale=mult_scale)
                self.tr_frames.append(trans_F)
        elif type == "ps":
            for i, ordata in enumerate(self.frames):
                freq, trans_F, F, F_ = Transdata.parallel_shift(
                    ordata, dt=self.del_x, ps_scale=ps_scale
                )
                self.tr_frames.append(trans_F)
        else:
            self.tr_frames = self.frames
            F = np.fft.fft(self.tr_frames)
            F_ = F

        if tofile_chan:
            print(f"Saved transformed data to {change_path}")
            self.ma.write(self.tr_frames, output_file=change_path)
        return F, F_
