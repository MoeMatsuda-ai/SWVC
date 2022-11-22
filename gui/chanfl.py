# coding:utf-8

from cProfile import label
from select import select
import tkinter as tk
from tkinter import ANCHOR, CENTER, END, Listbox, StringVar, ttk
import tkinter.font as f
from tkinter.tix import COLUMN
from turtle import color

class Test:
    def transform(self, command):
        print(command)

def mult_select(select, sl_low, sl_high):
    if select == "high":
        ret = float(sl_high)/100
    elif select == "low":
        ret = float(sl_low)/100
    else:
        ret = 1
    return ret

def dibox_freq(command):

    root = tk.Tk()  
    root.configure(background="black")
    root.geometry("1000x1000")
    root.title('ボイスチェンジャー') 
    font_def = f.Font(family="Times News", weight="bold", size=15)
    
    frame_list = tk.Frame(root, background="black")
    frame_list.place(x=100, y=100)
    font_list = f.Font(family="Times News", weight="bold", size=12)
    label_list = tk.Label(frame_list, text='タイプ ', anchor=CENTER,
                          width=15, background="black", foreground="white", font=font_def)
    label_list.grid(row=0, column=0, ipadx=5, ipady=10)
    var_list = StringVar()
    lb_mult = tk.Radiobutton(frame_list, text='音の高さ', value='mult',
                             font=font_list, variable=var_list)
    lb_ps = tk.Radiobutton(frame_list, text='しゅるい', value='ps',
                           font=font_list, variable=var_list)
    lb_mult.grid(row=0, column=1, padx=10, pady=10, ipadx=50, ipady=10)
    lb_ps.grid(row=0, column=2, padx=10, pady=10, ipadx=50, ipady=10)

    frame_mult = tk.Frame(root, background="black")
    frame_mult.place(x=100, y=200)
    label_mult = tk.Label(frame_mult, text='音の高さ', anchor=CENTER, font=font_def,
                          width=15, background="black", foreground="white")
    label_mult.grid(row=0, column=0, ipadx=5, ipady=10)
    var_rb = StringVar()
    lb_mult_high = tk.Radiobutton(frame_mult, text='高くする', value='high',
                                  font=font_list, variable=var_rb)
    lb_mult_low = tk.Radiobutton(frame_mult, text='ひくくする', value='low',
                                 font=font_list, variable=var_rb)
    lb_mult_low.grid(row=0, column=1, padx=10, pady=10, ipadx=10, ipady=10)
    lb_mult_high.grid(row=1, column=1, padx=10, pady=10, ipadx=10, ipady=10)
    frame_scale_low = ttk.Frame(root, padding=10)
    frame_scale_low.place(x=500, y=209)
    label_low_min = tk.Label(frame_scale_low, text='0.5', anchor=CENTER,
                             width=3, background="black", foreground="white", font=font_def)
    label_low_max = tk.Label(frame_scale_low, text='1', anchor=CENTER,
                             width=3, background="black", foreground="white", font=font_def)
    var_scale_low = tk.DoubleVar()
    sc_scale_low = ttk.Scale(frame_scale_low, variable=var_scale_low, orient=tk.HORIZONTAL,
                             length=200, from_=50, to=100)
    label_low_min.grid(row=0, column=1)
    sc_scale_low.grid(row=0, column=2, sticky=(tk.N, tk.E, tk.S, tk.W))
    label_low_max.grid(row=0, column=3)
    frame_scale_high = ttk.Frame(root, padding=10)
    frame_scale_high.place(x=500, y=270)
    label_high_min = tk.Label(frame_scale_high, text='1', anchor=CENTER,
                              width=3, background="black", foreground="white", font=font_def)
    label_high_max = tk.Label(frame_scale_high, text='10', anchor=CENTER,
                              width=3, background="black", foreground="white", font=font_def)
    var_scale_high = tk.DoubleVar()
    sc_scale_high = ttk.Scale(frame_scale_high, variable=var_scale_high, orient=tk.HORIZONTAL,
                              length=200, from_=100, to=1000)
    label_high_min.grid(row=0, column=1)
    sc_scale_high.grid(row=0, column=2, sticky=(tk.N, tk.E, tk.S, tk.W))
    label_high_max.grid(row=0, column=3)

    frame_ps = tk.Frame(root, background="black")
    frame_ps.place(x=100, y=350)
    label_ps = tk.Label(frame_ps, text='しゅるい', anchor=CENTER, font=font_def,
                        width=15, background="black", foreground="white")
    var_ps = StringVar()
    lb_syou = tk.Radiobutton(frame_ps, text='はんにん', value=-25,
                             font=font_list, variable=var_ps)
    lb_han = tk.Radiobutton(frame_ps, text='しょうげんしゃ',
                             value=30, font=font_list, variable=var_ps)
    lb_utyu = tk.Radiobutton(frame_ps, text='きかい音',
                             value=300, font=font_list, variable=var_ps)
    lb_suzu = tk.Radiobutton(frame_ps, text='すず虫',
                             value=500, font=font_list, variable=var_ps)
    label_ps.grid(row=0, column=0, ipadx=5, ipady=15)
    lb_syou.grid(row=0, column=1, padx=10, pady=5, ipadx=10, ipady=5)
    lb_han.grid(row=0, column=2, padx=10, pady=5, ipadx=10, ipady=5)
    lb_utyu.grid(row=0, column=3, padx=10, pady=5, ipadx=10, ipady=5)
    lb_suzu.grid(row=0, column=4, padx=10, pady=5, ipadx=10, ipady=5)

    frame_time = tk.Frame(root, background="black")
    frame_time.place(x=100, y=450)
    label_time = tk.Label(frame_time, text='ろくおんじかん [s]', anchor=CENTER, font=font_def,
                          width=15, background="black", foreground="white")
    label_time.grid(row=0, column=0, ipadx=5, ipady=15)
    var_time = tk.StringVar()
    entry_time = tk.Entry(frame_time, textvariable=var_time, borderwidth=5, font=font_def)
    entry_time.place(width=10, height=20)
    entry_time.grid(row=0, column=1, pady=10, padx=10, ipadx=0, ipady=10)
    entry_time.insert(0, 5)

    frame_save = tk.Frame(root, background="black")
    frame_save.place(x=100, y=550)
    label_save = tk.Label(frame_save, text='オリジナルデータ', anchor=CENTER, font=font_def,
                          width=15, background="black", foreground="white")
    label_save.grid(row=0, column=0, ipadx=5, ipady=15)
    var_save = tk.StringVar()
    var_save.set(True) 
    font_save = f.Font(family="Times News", weight="bold", size=12)
    cb = tk.Checkbutton(frame_save, text='セーブ',
                        onvalue=True, offvalue=False,
                        width=30,
                        font=font_save,
                        background="black",
                        activebackground="black",
                        foreground="white",
                        activeforeground="white",
                        selectcolor="black",
                        indicatoron=True,
                        variable=var_save)
    cb.grid(row=0, column=1, pady=10, padx=10, ipadx=50, ipady=10)
    
    frame_save_ts = tk.Frame(root, background="black")
    frame_save_ts.place(x=100, y=650)
    label_save_ts = tk.Label(frame_save_ts, text='変換後のデータ', anchor=CENTER, font=font_def,
                    width=15, background="black", foreground="white")
    label_save_ts.grid(row=0, column=0, ipadx=5, ipady=15)
    var_save_ts = tk.StringVar()
    var_save_ts.set(True) 
    font_save_ts = f.Font(family="Times News", weight="bold", size=12)
    cb = tk.Checkbutton(frame_save_ts, text='セーブ',
                        onvalue=True, offvalue=False,
                        width=30,
                        font=font_save_ts,
                        background="black",
                        activebackground="black",
                        foreground="white",
                        activeforeground="white",
                        selectcolor="black",
                        indicatoron=True,
                        variable=var_save_ts)
    cb.grid(row=0, column=1, pady=10, padx=10, ipadx=50, ipady=10)

    frame_exec = tk.Frame(root, background="black")
    frame_exec.place(x=300, y=750)
    button_exec = tk.Button(frame_exec, width=10, font=font_def,
                            relief=tk.RAISED, borderwidth=5, text='ろくおん',
                            command=lambda: command.transform(tofile_origin=int(var_save.get()), 
                                                              tofile_chan=int(var_save_ts.get()),
                                                              type=var_list.get(), 
                                                              ps_scale=int(var_ps.get()), 
                                                              mult_scale=mult_select(var_rb.get(),
                                                              var_scale_low.get(), var_scale_high.get()),
                                                              record_time=float(var_time.get()), 
                                                              graph=False,
                                                              original_path="./data/original_data.wav", 
                                                              change_path="./data/change_data.wav"))
    button_exec.grid(row=0, column=1, ipadx=10, ipady=10)
    button_out = tk.Button(frame_exec,
                           width=10,
                           font=font_def,
                           relief=tk.RAISED,
                           borderwidth=5, 
                           text='さいせい',
                           command=lambda: command.write())
    button_out.grid(row=0, column=2, padx=50, pady=10, ipadx=10, ipady=10)
    
    root.mainloop()

if __name__=='__main__':
    dibox_freq(Test())
