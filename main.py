import sys
import tkinter
from tkinter import ttk
from tkinter.messagebox import *
import sv_ttk
import darkdetect
import random
import json

import configgui
import pandas as pd

VERSION = "1.0.0rel"
VER_NO = 1
class App(tkinter.Tk):
    def __init__(self):
        global allowRepeat,alwaysOnTop,showName,pref
        allowRepeat = False
        alwaysOnTop = True
        showName = True
        super().__init__()
        self.geometry("450x200")
        self.attributes('-topmost',alwaysOnTop)
        self.title("NamePicker - 随机抽选")
        self.resizable(False, False)
        self.loadcfg()
        sv_ttk.set_theme(darkdetect.theme())
        pref = [tkinter.StringVar(), tkinter.StringVar()]
        self.loadname()
        self.createWidget()
    names = []
    chosen = []
    length = 0
    sexlen = [0,0]
    sexl = [[],[]]
    numlen = [0,0]
    numl = [[],[]]
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

        if pref[1].get() != "单双都抽":
            if pref[1].get() == "只抽双数":
                tar = list(set(tar)&set(self.numl[0]))
                le = len(tar)
            else:
                tar = list(set(tar) & set(self.numl[1]))
                le = len(tar)
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
        cfg = configgui.cfgpage(darkdetect.theme())
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
        sexpref.place(x=250,y=100,anchor="center")
        numpref = ttk.OptionMenu(self, pref[1], "单双都抽", "只抽单数", "只抽双数", "单双都抽")
        numpref.place(x=350, y=100, anchor="center")

    def loadname(self):
        try:
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

            for i in self.names[0]:
                if self.names[2][self.names[0].index(i)]%2==0:
                    self.numl[0].append(i)
                else:
                    self.numl[1].append(i)
            self.numlen[0] = len(self.numl[0])
            self.numlen[1] = len(self.numl[1])
        except FileNotFoundError:
            with open("names.csv","w",encoding="utf-8") as f:
                st  = ["name,sex,no\n","example,0,1"]
                f.writelines(st)
            r = showwarning("警告","检测到names.csv不存在，已为您创建样板文件，请修改")
            sys.exit(114514)

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