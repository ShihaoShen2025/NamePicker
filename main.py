import tkinter
from tkinter import ttk
from tkinter.messagebox import *
import sv_ttk
import darkdetect
import random
import json
import sys

class App(tkinter.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("200x200")
        self.attributes('-topmost',self.alwaysOnTop)
        self.title("随机抽选")
        self.resizable(False, False)
        sv_ttk.set_theme(darkdetect.theme())
        self.loadcfg()
        self.loadname()
        self.createWidget()
    names = []
    chosen = []
    def pick(self):
        ch = random.choice(self.names)
        if not allowRepeat:
            if len(self.names) == len(self.chosen):
                self.chosen = []
            while ch in self.chosen:
                ch = random.choice(self.names)
            self.chosen.append(ch)
        name.config(text=ch)

    def opencfg(self):
        pass

    def createWidget(self):
        global name
        name = ttk.Label(self, text="尚未抽选")
        name.place(x=100, y=50, anchor="center")
        button = ttk.Button(self, text="点击以抽选", command=self.pick)
        button.place(x=100, y=100, anchor="center")
        confb = ttk.Button(self, text="点击打开配置菜单", command=self.opencfg)
        confb.place(x=100, y=150, anchor="center")

    def loadname(self):
        try:
            with open("names.txt","r",encoding="utf-8") as f:
                for i in f.readlines():
                    self.names.append(i.strip("\n"))
        except FileNotFoundError:
            r = showerror("错误","没有找到names.txt，请参照README进行处理")
            sys.exit(114514)

    allowRepeat = False
    alwaysOnTop =True
    def loadcfg(self):
        global alwaysOnTop,allowRepeat
        with open("config.json","r",encoding="utf-8") as f:
            conf = f.read()
        config = json.loads(conf)
        allowRepeat = config["allowRepeat"]
        alwaysOnTop = config["alwaysOnTop"]


if __name__ == "__main__":
    app = App()
    app.mainloop()