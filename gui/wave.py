from importlib.metadata import PathDistribution
from logging import root
from operator import inv
import tkinter as tk
from tkinter import CENTER, ttk
import tkinter.font as f

def dibox_graph(command):
    root = tk.Tk()
    root.configure(background="black")
    root.geometry("900x350")
    root.title('inverse sound')

    font_def = f.Font(family="Times News", weight="bold", size=15)
    frame_list = tk.Frame(root, background="black")
    frame_list.place(x=50, y=50)

    label_list = tk.Label(frame_list, text='type of graph ', anchor=CENTER,
                          width=15, background="black", foreground="white", font=font_def)
    font_list = f.Font(family="Times News", weight="bold", size=12)
    var_list = tk.StringVar(value=False)
    lb_one = tk.Radiobutton(frame_list, text='sound wave', value=False,
                            font=font_list, variable=var_list)
    lb_two = tk.Radiobutton(frame_list, text='sound wave and frequency',
                            value=True, font=font_list, variable=var_list)
    label_list.grid(row=0, column=0, ipadx=5, ipady=10)    
    lb_one.grid(row=0, column=1, padx=10, pady=10, ipadx=50, ipady=10)
    lb_two.grid(row=0, column=2, padx=10, pady=10, ipadx=50, ipady=10)
    
    frame_scale = tk.Frame(root, background="black")
    frame_scale.place(x=50, y=150)
    label_scale = tk.Label(frame_scale, text='x ticks scale', anchor=CENTER, font=font_def,
                           width=15, background="black", foreground="white")
    var_scale = tk.StringVar()
    entry_scale = tk.Entry(frame_scale, textvariable=var_scale, borderwidth=5, font=font_def)
    entry_scale.insert(0, 1)
    entry_scale.place(width=10, height=20)
    label_scale.grid(row=0, column=0, ipadx=5, ipady=15)
    entry_scale.grid(row=0, column=1, pady=10, padx=10, ipadx=0, ipady=10)

    frame_exec = tk.Frame(root, background="black")
    frame_exec.place(x=400, y=250)
    button_exec = tk.Button(frame_exec,
                            width=10,
                            font=font_def,
                            relief=tk.RAISED,
                            borderwidth=5, 
                            text='Record',
                            command=lambda: command.plot_graph(scale=int(var_scale.get()), freq=int(var_list.get())))
    button_exec.grid(row=0, column=1, ipadx=10, ipady=10)


    root.mainloop()

if __name__=='__main__':
    dibox_graph(1)
