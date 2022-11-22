# coding:utf-8

from cProfile import label
from select import select
import tkinter as tk
from tkinter import ANCHOR, CENTER, END, Listbox, StringVar, ttk
import tkinter.font as f
from turtle import color

class Test:
    def transform(self, command):
        print(command)

def dibox_freq(command):

    root = tk.Tk()  
    root.configure(background="black")
    root.geometry("1000x800") # ダイアログボックスのサイズ
    root.title('Transform frequency') # title

    font_def = f.Font(family="Times News", weight="bold", size=15)

    # listbox
    frame_list = tk.Frame(root, background="black")
    frame_list.place(x=100, y=100)

    label_list = tk.Label(frame_list, text='type', anchor=CENTER,
                    width=15, background="black", foreground="white", font=font_def)
    
    font_list = f.Font(family="Times News", weight="bold", size=12)
    # Radiobutton 1
    var_list = StringVar()
    lb_mult = tk.Radiobutton(
        frame_list,
        text='mult',
        value='mult',
        font=font_list,
        variable=var_list)
    # Radiobutton 2
    lb_ps = tk.Radiobutton(
        frame_list,
        text='ps',
        value='ps',
        font=font_list,
        variable=var_list)
    label_list.grid(row=0, column=0, ipadx=5, ipady=10)
    lb_mult.grid(row=0, column=1, padx=10, pady=10, ipadx=50, ipady=10)
    lb_ps.grid(row=0, column=2, padx=10, pady=10, ipadx=50, ipady=10)

    # mult
    frame_mult = tk.Frame(root, background="black")
    frame_mult.place(x=100, y=200)
    label_mult = tk.Label(frame_mult, text='mult', anchor=CENTER, font=font_def,
                    width=15, background="black", foreground="white")
    var_mul = tk.StringVar()
    entry_mult = tk.Entry(frame_mult, textvariable=var_mul, borderwidth=5, font=font_def)
    entry_mult.place(width=10, height=20)
    entry_mult.insert(0, 1.5)
    """
    pad : boxごとの隙間の幅
    ipad : boxごとの幅
    """
    label_mult.grid(row=1, column=0, ipadx=5, ipady=10)
    entry_mult.grid(row=1, column=1, pady=10, padx=10, ipadx=50, ipady=10)

    # parallel shift 
    frame_ps = tk.Frame(root, background="black")
    frame_ps.place(x=100, y=300)
    label_ps = tk.Label(frame_ps, text='parallel shift', anchor=CENTER, font=font_def,
                    width=15, background="black", foreground="white")
    var_ps = tk.StringVar()
    entry_ps = tk.Entry(frame_ps, textvariable=var_ps, borderwidth=5, font=font_def)
    entry_ps.place(width=10, height=20)
    label_ps.grid(row=2, column=0, ipadx=5, ipady=15)
    entry_ps.grid(row=2, column=1, pady=10, padx=10, ipadx=50, ipady=10)
    entry_ps.insert(0, 100)

    # record time 
    frame_time = tk.Frame(root, background="black")
    frame_time.place(x=100, y=400)
    label_time = tk.Label(frame_time, text='record time', anchor=CENTER, font=font_def,
                    width=15, background="black", foreground="white")
    var_time = tk.StringVar()
    entry_time = tk.Entry(frame_time, textvariable=var_time, borderwidth=5, font=font_def)
    entry_time.place(width=10, height=20)
    label_time.grid(row=3, column=0, ipadx=5, ipady=15)
    entry_time.grid(row=3, column=1, pady=10, padx=10, ipadx=50, ipady=10)
    entry_time.insert(0, 5)

    # save to file or not 
    frame_save = tk.Frame(root, background="black")
    frame_save.place(x=100, y=500)
    label_save = tk.Label(frame_save, text='original data', anchor=CENTER, font=font_def,
                    width=15, background="black", foreground="white")
    var_save = tk.StringVar()
    var_save.set(True) # チャックボックスの初期値
    font_save = f.Font(family="Times News", weight="bold", size=12)
    cb = tk.Checkbutton(frame_save, text='save original data',
                        onvalue=True, offvalue=False,
                        font=font_save,
                        background="black",
                        activebackground="black",
                        foreground="white",
                        activeforeground="white",
                        selectcolor="black",
                        indicatoron=True,
                        variable=var_save)
    label_save.grid(row=4, column=0, ipadx=5, ipady=15)
    cb.grid(row=4, column=1, pady=10, padx=10, ipadx=50, ipady=10)
    
    # save to file or not 
    frame_save_ts = tk.Frame(root, background="black")
    frame_save_ts.place(x=100, y=600)
    label_save_ts = tk.Label(frame_save_ts, text='transformed data', anchor=CENTER, font=font_def,
                    width=15, background="black", foreground="white")
    var_save_ts = tk.StringVar()
    var_save_ts.set(True) # チェックボックスの初期値
    font_save_ts = f.Font(family="Times News", weight="bold", size=12)
    cb = tk.Checkbutton(frame_save_ts, text='save transformed data',
                        onvalue=True, offvalue=False,
                        font=font_save_ts,
                        background="black",
                        activebackground="black",
                        foreground="white",
                        activeforeground="white",
                        selectcolor="black",
                        indicatoron=True,
                        variable=var_save_ts)
    button_save_ts = tk.Button(
        frame_save_ts,
        width=10,
        font=font_def,
        relief=tk.RAISED,
        borderwidth=5, 
        text='execution',
        command=lambda: command.transform(tofile_origin=int(var_save.get()), 
                                        tofile_chan=int(var_save_ts.get()),
                                        type=var_list.get(), 
                                        ps_scale=int(var_ps.get()), 
                                        mult_scale=float(var_mul.get()),
                                        record_time=float(var_time.get()), 
                                        graph=False,
                                        original_path="./data/original_data.wav", 
                                        change_path="./data/change_data.wav"))
    label_save_ts.grid(row=5, column=0, ipadx=5, ipady=15)
    cb.grid(row=5, column=1, pady=10, padx=10, ipadx=50, ipady=10)
    button_save_ts.grid(row=5, column=2, ipadx=10, ipady=10)
    
    # ウィンドウの表示開始
    root.mainloop()

if __name__=='__main__':
    dibox_freq(Test())
