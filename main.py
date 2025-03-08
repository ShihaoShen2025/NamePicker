import tkinter
from tkinter import ttk
from tkinter.messagebox import *
import sv_ttk
import darkdetect
import random
import json
import sys
import configgui

VERSION = "1.0.0dev"
VER_NO = 1
class App(tkinter.Tk):
    def __init__(self):
        global allowRepeat,alwaysOnTop
        allowRepeat = False
        alwaysOnTop = True
        super().__init__()
        self.geometry("400x200")
        self.attributes('-topmost',alwaysOnTop)
        self.title("NamePicker - 随机抽选")
        self.resizable(False, False)
        self.loadcfg()
        sv_ttk.set_theme(darkdetect.theme())
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
        cfg = configgui.cfgpage()
        cfg.mainloop()

    def createWidget(self):
        global name
        name = ttk.Label(self, text="尚未抽选")
        name.place(x=100, y=50, anchor="center")
        button = ttk.Button(self, text="点击以抽选", command=self.pick)
        button.place(x=300, y=50, anchor="center")
        confb = ttk.Button(self, text="点击打开配置菜单", command=self.opencfg)
        confb.place(x=300, y=150, anchor="center")

    def loadname(self):
        try:
            with open("names.txt","r",encoding="utf-8") as f:
                for i in f.readlines():
                    self.names.append(i.strip("\n"))
        except FileNotFoundError:
            r = showerror("错误","没有找到names.txt，请参照README进行处理")
            sys.exit(114514)

    def loadcfg(self):
        try:
            global alwaysOnTop,allowRepeat
            with open("config.json","r",encoding="utf-8") as f:
                conf = f.read()
            config = json.loads(conf)
            allowRepeat = config["allowRepeat"]
            alwaysOnTop = config["alwaysOnTop"]
            if config["VER_NO"] < VER_NO:
                r = showwarning("警告","当前配置文件版本较低，可能会出现一些玄学问题")
            elif config["VER_NO"] > VER_NO:
                r = showwarning("警告","当前配置文件版本较高，可能会出现一些玄学问题")
        except FileNotFoundError:
            cfg = {"VERSION": VERSION,
                   "VER_NO": VER_NO,
                   "allowRepeat": False,
                    "alwaysOnTop": True}
            conf = json.dumps(cfg)
            with open("config.json", "w", encoding="utf-8") as f:
                f.write(conf)
            r = showinfo("完成","没有检测到配置文件，已创建默认配置文件")


if __name__ == "__main__":
    app = App()
    app.mainloop()