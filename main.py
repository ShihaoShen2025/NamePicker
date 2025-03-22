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
import tempfile

temp_dir = tempfile.gettempdir()
VERSION = "1.0.3dev"
VER_NO = 4
CODENAME = "Firefly"
photo = None

class App(tkinter.Toplevel):
    def __init__(self):
        global allowRepeat,alwaysOnTop,showName,SupportCW,pref,pickNames,pns
        allowRepeat = False
        alwaysOnTop = True
        showName = True
        SupportCW = False
        pickNames = 1
        super().__init__()
        self.geometry("450x200")
        self.loadcfg()
        self.attributes('-topmost',alwaysOnTop)
        self.title("NamePicker - 随机抽选")
        self.resizable(False, False)
        sv_ttk.set_theme(darkdetect.theme())
        pref = [tkinter.StringVar(), tkinter.StringVar()]
        pns = tkinter.IntVar()
        pns.set(1)
        self.loadname()
        self.createWidget()
    names = []
    chosen = []
    length = 0
    sexlen = [0,0,0]
    sexl = [[],[],[]]
    numlen = [0,0]
    numl = [[],[]]

    def pick(self):
        global allowRepeat,showName
        self.loadcfg()
        if pref[0].get() != "男女都抽":
            if pref[0].get() == "只抽男":
                le = self.sexlen[0]
                tar = self.sexl[0]
            elif pref[0].get() == "只抽女":
                le = self.sexlen[1]
                tar = self.sexl[1]
            else:
                le = self.sexlen[2]
                tar = self.sexl[2]
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
        if le != 0:
            chs = random.randint(0, le - 1)
            if not allowRepeat:
                if len(self.chosen)>=le:
                    self.chosen=[]
                    chs = random.randint(0, le-1)
                else:
                    while chs in self.chosen:
                        chs = random.randint(0, le-1)
                self.chosen.append(chs)

            return [tar[chs],self.names[2][self.names[0].index(tar[chs])]]
        else:
            showwarning("警告","没有符合筛选条件的学生")
            return ["尚未抽选","尚未抽选"]

    def pickcb(self):
        global SupportCW,temp_dir,pickNames
        name.delete(*name.get_children())
        if pickNames == 1:
            res = self.pick()
            if SupportCW:
                with open("%s\\unread"%temp_dir,"w",encoding="utf-8") as f:
                    f.write("111")
                with open("%s\\res.txt"%temp_dir,"w",encoding="utf-8") as f:
                    f.write("%s（%s）"%(res[0],res[1]))

            else:
                name.insert("","end", values=res)
        else:
            res = []
            for i in range(pickNames):
                res.append(self.pick())
            if SupportCW:
                rese = []
                for i in res:
                    rese.append("%s（%s）" % (i[0], i[1]))
                with open("%s\\unread"%temp_dir,"w",encoding="utf-8") as f:
                    f.write("111")
                with open("%s\\res.txt"%temp_dir,"w",encoding="utf-8") as f:
                    f.write("，".join(rese))
            else:
                for i in res:
                    name.insert("", "end", values=i)


    def opencfg(self):
        cfg = configgui.cfgpage(darkdetect.theme())
        cfg.mainloop()

    def updatenames(self):
        global pickNames,pns
        pickNames = pns.get()

    def createWidget(self):
        global name
        scroll_v = ttk.Scrollbar(self)
        scroll_v.pack(side="right",fill="y")
        name = ttk.Treeview(self, height=10,columns=["姓名","学号"],show='headings',yscrollcommand=scroll_v.set)
        name.heading('姓名', text='姓名')
        name.heading('学号', text='学号')
        name.column("姓名",width=75)
        name.column("学号", width=75)
        name.place(relx=0,rely=0,anchor="nw")
        scroll_v.config(command=name.yview)
        button = ttk.Button(self, text="点击以抽选", command=self.pickcb)
        button.place(x=250, y=50, anchor="center")
        pn = ttk.Spinbox(self,textvariable=pns,from_=1,to=len(self.names[2]),width=3,command=self.updatenames)
        pn.place(x=370, y=50, anchor="center")
        confb = ttk.Button(self, text="点击打开配置菜单", command=self.opencfg)
        confb.place(x=300, y=150, anchor="center")
        sexpref = ttk.OptionMenu(self,pref[0],"男女都抽","只抽男","只抽女","只抽非二元","男女都抽")
        sexpref.place(x=250,y=100,anchor="center")
        numpref = ttk.OptionMenu(self, pref[1], "单双都抽", "只抽单数", "只抽双数", "单双都抽")
        numpref.place(x=370, y=100, anchor="center")

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
            self.sexlen[2] = self.names[1].count(2)
            for i in self.names[0]:
                if self.names[1][self.names[0].index(i)] == 0:
                    self.sexl[0].append(i)
                elif self.names[1][self.names[0].index(i)] == 1:
                    self.sexl[1].append(i)
                else:
                    self.sexl[2].append(i)

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
            global allowRepeat,alwaysOnTop,showName,SupportCW,pickNames
            with open("config.json","r",encoding="utf-8") as f:
                conf = f.read()
            config = json.loads(conf)
            allowRepeat = config["allowRepeat"]
            alwaysOnTop = config["alwaysOnTop"]
            SupportCW = config["SupportCW"]
            if config["VER_NO"] < VER_NO:
                r = showwarning("警告","当前配置文件版本较低，可能会出现一些玄学问题")
            elif config["VER_NO"] > VER_NO:
                r = showwarning("警告","当前配置文件版本较高，可能会出现一些玄学问题")
            self.attributes('-topmost',alwaysOnTop)
        except FileNotFoundError:
            cfg = {"VERSION": VERSION,
                   "VER_NO": VER_NO,
                   "CODENAME": CODENAME,
                   "allowRepeat": False,
                   "alwaysOnTop": True,
                   "SupportCW":False}
            conf = json.dumps(cfg)
            with open("config.json", "w", encoding="utf-8") as f:
                f.write(conf)

class Shortcut(tkinter.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("100x100")
        self.overrideredirect(True)
        self.attributes('-topmost', True)
        sv_ttk.set_theme(darkdetect.theme())
        self.pack_widgets()

    def pack_widgets(self):
        frame = ttk.Frame(self,width=100,height=100)
        frame.pack(anchor="center")
        frame.bind("<B1-Motion>", self.move_window)
        frame.bind("<ButtonRelease-1>", self.calls)

    def move_window(self,event):
        self.geometry("+{0}+{1}".format(event.x_root-50, event.y_root-50))

    def calls(self,event):
        app = App()
        app.mainloop()


if __name__ == "__main__":
    # app = App()
    # app.mainloop()
    sh = Shortcut()
    sh.mainloop()