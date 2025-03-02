import tkinter
from tkinter import ttk
import sv_ttk
import darkdetect
import random
import json

names = []
chosen = []
with open("names.txt","r",encoding="utf-8") as f:
    for i in f.readlines():
        names.append(i.strip("\n"))

with open("config.json","r",encoding="utf-8") as f:
    conf = f.read()
config = json.loads(conf)
allowRepeat = config["allowRepeat"]
alwaysOnTop = config["alwaysOnTop"]

def pick():
    global name,names,allowRepeat,chosen
    ch = random.choice(names)
    if not allowRepeat:
        if len(names) == len(chosen):
            chosen = []
        while ch in chosen:
            ch = random.choice(names)
        chosen.append(ch)
    name.config(text=ch)

root = tkinter.Tk()
root.geometry("200x200")
root.attributes('-topmost',alwaysOnTop)
root.title("随机抽选")

name = ttk.Label(root,text="尚未抽选")
name.place(x=100,y=50,anchor="center")
button = ttk.Button(root, text="点击以抽选",command=pick)
button.place(x=100,y=100,anchor="center")

sv_ttk.set_theme(darkdetect.theme())
root.mainloop()