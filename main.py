import tkinter
from tkinter import ttk
from tkinter.messagebox import *
import sv_ttk
import darkdetect
import random
import json

from numpy.ma.core import count

import configgui
import pandas as pd

VERSION = "1.0.0dev"
VER_NO = 1
class App(tkinter.Tk):
    def __init__(self):
        global allowRepeat,alwaysOnTop,showName,pref
        allowRepeat = False
        alwaysOnTop = True
        showName = True
        super().__init__()
        self.geometry("400x200")
        self.attributes('-topmost',alwaysOnTop)
        self.title("NamePicker - 随机抽选")
        self.resizable(False, False)
        self.loadcfg()
        sv_ttk.set_theme(darkdetect.theme())
        pref = [tkinter.StringVar(), tkinter.IntVar()]
        self.loadname()
        self.createWidget()
    names = []
    chosen = []
    length = 0
    sexlen = [0,0]
    sexl = [[],[]]
    def pick(self):
        global allowRepeat,showName
        if pref[0].get() != "男女都抽":
            if pref[0].get() == "只抽男":
                le = self.sexlen[0]
                tar = self.sexl[0]
            else:
                le = self.sexlen[1]
                tar = self.sexl[1]
        else:
            le = self.length
            tar = self.names[0]

        chs = random.randint(0, le - 1)
        if not allowRepeat:
            if len(self.chosen)>=le:
                self.chosen=[]
                chs = random.randint(0, le-1)
            else:
                while chs in self.chosen:
                    chs = random.randint(0, le-1)
            self.chosen.append(chs)

        if showName:
            ch = tar[chs]
        else:
            ch = self.names[2][self.names[0].index(tar[chs])]
        name.config(text=ch)

    def opencfg(self):
        cfg = configgui.cfgpage()
        cfg.mainloop()

    def createWidget(self):
        global name
        name = ttk.Label(self, text="尚未抽选",font=('微软雅黑', 20))
        name.place(x=100, y=100, anchor="center")
        button = ttk.Button(self, text="点击以抽选", command=self.pick)
        button.place(x=300, y=50, anchor="center")
        confb = ttk.Button(self, text="点击打开配置菜单", command=self.opencfg)
        confb.place(x=300, y=150, anchor="center")
        sexpref = ttk.OptionMenu(self,pref[0],"男女都抽","只抽男","只抽女","男女都抽")
        sexpref.place(x=300,y=100,anchor="center")

    def loadname(self):
        name = pd.read_csv("names.csv",sep=",",header=0,dtype={'name': str, 'sex': int, "no":int})
        name = name.to_dict()
        self.names.append(list(name["name"].values()))
        self.names.append(list(name["sex"].values()))
        self.names.append(list(name["no"].values()))
        self.length =len(name["name"])
        self.sexlen[0] = self.names[1].count(0)
        self.sexlen[1] = self.names[1].count(1)
        for i in self.names[0]:
            if self.names[1][self.names[0].index(i)] == 0:
                self.sexl[0].append(i)
            else:
                self.sexl[1].append(i)

    def loadcfg(self):
        try:
            global allowRepeat,alwaysOnTop,showName
            with open("config.json","r",encoding="utf-8") as f:
                conf = f.read()
            config = json.loads(conf)
            allowRepeat = config["allowRepeat"]
            alwaysOnTop = config["alwaysOnTop"]
            showName = config["showName"]
            if config["VER_NO"] < VER_NO:
                r = showwarning("警告","当前配置文件版本较低，可能会出现一些玄学问题")
            elif config["VER_NO"] > VER_NO:
                r = showwarning("警告","当前配置文件版本较高，可能会出现一些玄学问题")
        except FileNotFoundError:
            cfg = {"VERSION": VERSION,
                   "VER_NO": VER_NO,
                   "allowRepeat": False,
                   "alwaysOnTop": True,
                   "showName": True}
            conf = json.dumps(cfg)
            with open("config.json", "w", encoding="utf-8") as f:
                f.write(conf)
            r = showinfo("完成","没有检测到配置文件，已创建默认配置文件")


if __name__ == "__main__":
    app = App()
    app.mainloop()