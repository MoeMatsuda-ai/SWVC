from importlib.metadata import PathDistribution
from logging import root
from operator import inv
import tkinter as tk
from tkinter import CENTER, ttk
import tkinter.font as f


class Test:
    def inverse(self, command):
        print(command)

    def write(self):
        print("Done.")


def dibox_inv(command):
    root = tk.Tk()
    root.configure(background="black")
    root.geometry("780x750")
    root.title("inverse sound")

    font_def = f.Font(family="Times News", weight="bold", size=15)

    frame_time = tk.Frame(root, background="black")
    frame_time.place(x=100, y=100)
    label_time = tk.Label(
        frame_time,
        text="ろくおんじかん [s]",
        background="black",
        foreground="white",
        anchor=CENTER,
        width=20,
        font=font_def,
    )
    var_time = tk.StringVar()
    entry_time = tk.Entry(
        frame_time, textvariable=var_time, borderwidth=5, font=font_def
    )
    label_time.grid(row=0, column=0, ipadx=5, ipady=15)
    entry_time.grid(row=0, column=1, ipadx=0, ipady=10)
    entry_time.insert(0, 5)

    frame_speed = tk.Frame(root, background="black")
    frame_speed.place(x=100, y=200)
    label_speed = tk.Label(
        frame_speed,
        text="さいせいそくど",
        background="black",
        foreground="white",
        anchor=CENTER,
        width=20,
        font=font_def,
    )
    var_speed = tk.StringVar()
    entry_speed = tk.Entry(
        frame_speed, textvariable=var_speed, borderwidth=5, font=font_def
    )
    label_speed.grid(row=0, column=0, ipadx=5, ipady=15)
    entry_speed.grid(row=0, column=1, ipadx=0, ipady=10)
    entry_speed.insert(0, 1)

    frame_inv = tk.Frame(root, background="black")
    frame_inv.place(x=100, y=300)
    label_inv = tk.Label(
        frame_inv,
        text="オプション",
        anchor=CENTER,
        font=font_def,
        width=20,
        background="black",
        foreground="white",
    )
    var_inv = tk.StringVar()
    var_inv.set(True)
    font_inv = f.Font(family="Times News", weight="bold", size=12)
    cb_inv = tk.Checkbutton(
        frame_inv,
        text="ぎゃくさいせい",
        onvalue=True,
        offvalue=False,
        width=10,
        font=font_inv,
        background="black",
        activebackground="black",
        foreground="white",
        activeforeground="white",
        selectcolor="black",
        indicatoron=True,
        variable=var_inv,
    )
    label_inv.grid(row=0, column=0, ipadx=5, ipady=15)
    cb_inv.grid(row=0, column=1, pady=10, padx=10, ipadx=50, ipady=10)

    frame_save = tk.Frame(root, background="black")
    frame_save.place(x=100, y=400)
    label_save = tk.Label(
        frame_save,
        text="オリジナルデータ",
        anchor=CENTER,
        font=font_def,
        width=20,
        background="black",
        foreground="white",
    )
    var_save = tk.StringVar()
    var_save.set(True)
    font_save = f.Font(family="Times News", weight="bold", size=12)
    cb_save = tk.Checkbutton(
        frame_save,
        text="セーブ",
        onvalue=True,
        offvalue=False,
        width=10,
        font=font_save,
        background="black",
        activebackground="black",
        foreground="white",
        activeforeground="white",
        selectcolor="black",
        indicatoron=True,
        variable=var_save,
    )
    label_save.grid(row=0, column=0, ipadx=5, ipady=15)
    cb_save.grid(row=0, column=1, pady=10, padx=10, ipadx=50, ipady=10)

    frame_save_ts = tk.Frame(root, background="black")
    frame_save_ts.place(x=100, y=500)
    label_save_ts = tk.Label(
        frame_save_ts,
        text="変換後のデータ",
        anchor=CENTER,
        font=font_def,
        width=20,
        background="black",
        foreground="white",
    )
    var_save_ts = tk.StringVar()
    var_save_ts.set(True)
    font_save_ts = f.Font(family="Times News", weight="bold", size=12)
    cb_save_ts = tk.Checkbutton(
        frame_save_ts,
        text="セーブ",
        onvalue=True,
        offvalue=False,
        width=10,
        font=font_save_ts,
        background="black",
        activebackground="black",
        foreground="white",
        activeforeground="white",
        selectcolor="black",
        indicatoron=True,
        variable=var_save_ts,
    )
    label_save_ts.grid(row=0, column=0, ipadx=5, ipady=15)
    cb_save_ts.grid(row=0, column=1, pady=10, padx=10, ipadx=50, ipady=10)

    frame_exec = tk.Frame(root, background="black")
    frame_exec.place(x=100, y=600)
    button_exec = tk.Button(
        frame_exec,
        width=8,
        font=font_def,
        relief=tk.RAISED,
        borderwidth=5,
        text="ろくおん",
        command=lambda: command.inverse(
            record_time=float(var_time.get()),
            tofile_origin=int(var_save.get()),
            tofile_chan=int(var_save_ts.get()),
            speed=float(var_speed.get()),
            inv=int(var_inv.get()),
        ),
    )
    button_exec.grid(row=0, column=1, padx=50, pady=10, ipadx=10, ipady=10)

    button_out = tk.Button(
        frame_exec,
        width=8,
        font=font_def,
        relief=tk.RAISED,
        border=5,
        text="さいせい",
        command=lambda: command.write(),
    )
    button_out.grid(row=0, column=2, padx=50, pady=10, ipadx=10, ipady=10)

    root.mainloop()

    if __name__ == "__main__":
        dibox_inv(Test())
