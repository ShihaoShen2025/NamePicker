import os.path
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
from PIL import Image,ImageTk
import pystray
import threading
import logging
import traceback

if os.path.exists("DEBUG"):
    logging.basicConfig(filename='log.log',encoding="UTF-8",level=logging.DEBUG,filemode='w')
elif os.path.exists("IDE"):
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(filename='log.log', encoding="UTF-8", level=logging.INFO, filemode='w')
temp_dir = tempfile.gettempdir()
VERSION = "1.1.1dev"
VER_NO = 6
CODENAME = "Sonetto"
img = Image.open("NamePicker.png")
img.resize((100,100))

logging.info("⌈晴朗和静谧统治着一切⌋")
class App(tkinter.Toplevel):
    def __init__(self):
        global allowRepeat,alwaysOnTop,showName,SupportCW,pref,pickNames,pns
        allowRepeat = False
        alwaysOnTop = True
        showName = True
        SupportCW = False
        pickNames = 1
        super().__init__()
        w = self.winfo_screenwidth()
        h = self.winfo_screenheight()
        self.geometry("450x200+%d+%d"%(w*0.6,h*0.6))
        self.iconbitmap("favicon.ico")
        self.loadcfg()
        self.attributes('-topmost',alwaysOnTop)
        self.title("NamePicker - 随机抽选")
        sv_ttk.set_theme(darkdetect.theme())
        pref = [tkinter.StringVar(), tkinter.StringVar()]
        pns = tkinter.IntVar()
        pns.set(1)
        self.loadname()
        self.createWidget()
        self.report_callback_exception = self.handle_exception
    names = []
    chosen = []
    length = 0
    sexlen = [0,0,0]
    sexl = [[],[],[]]
    numlen = [0,0]
    numl = [[],[]]

    def pick(self):
        global allowRepeat,showName
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
                logging.debug(self.chosen)
            logging.info("抽选完成")
            return [tar[chs],self.names[2][self.names[0].index(tar[chs])]]
        else:
            showwarning("警告","没有符合筛选条件的学生")
            logging.warning("没有符合筛选条件的学生")
            return ["尚未抽选","尚未抽选"]

    def pickcb(self):
        global SupportCW,temp_dir,pickNames
        self.loadcfg()
        name.delete(*name.get_children())
        if pickNames == 1:
            res = self.pick()
            if SupportCW:
                with open("%s\\unread"%temp_dir,"w",encoding="utf-8") as f:
                    f.write("111")
                with open("%s\\res.txt"%temp_dir,"w",encoding="utf-8") as f:
                    f.write("%s（%s）"%(res[0],res[1]))
                logging.info("写入名单完成")
            else:
                name.insert("","end", values=res)
                logging.info("写入名单完成")
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
                logging.info("写入名单完成")
            else:
                for i in res:
                    name.insert("", "end", values=i)
                logging.info("写入名单完成")


    def opencfg(self):
        cfg = configgui.cfgpage()
        cfg.mainloop()
        logging.info("打开配置菜单")

    def updatenames(self):
        global pickNames,pns
        pickNames = pns.get()
        logging.debug("updatenames被调用")

    def createWidget(self):
        global name
        scroll_v = ttk.Scrollbar(self)
        scroll_v.pack(side="right",fill="y")
        name = ttk.Treeview(self, height=8,columns=["姓名","学号"],show='headings',yscrollcommand=scroll_v.set)
        name.heading('姓名', text='姓名')
        name.heading('学号', text='学号')
        name.column("姓名",width=75)
        name.column("学号", width=75)
        name.place(relx=0,rely=0,anchor="nw",relheight=1)
        scroll_v.config(command=name.yview)
        button = ttk.Button(self, text="点击以抽选", command=self.pickcb)
        button.place(relx=0.53, rely=0.25, anchor="center")
        pn = ttk.Spinbox(self,textvariable=pns,from_=1,to=len(self.names[2]),width=3,command=self.updatenames)
        pn.place(relx=0.8, rely=0.25, anchor="center")
        confb = ttk.Button(self, text="点击打开配置菜单", command=self.opencfg)
        confb.place(relx=0.65, rely=0.8, anchor="center")
        sexpref = ttk.OptionMenu(self,pref[0],"男女都抽","只抽男","只抽女","只抽非二元","男女都抽")
        sexpref.place(relx=0.53,rely=0.5,anchor="center")
        numpref = ttk.OptionMenu(self, pref[1], "单双都抽", "只抽单数", "只抽双数", "单双都抽")
        numpref.place(relx=0.8, rely=0.5, anchor="center")
        logging.info("组件设置完成")

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
            logging.info("名单导入完成")
        except FileNotFoundError:
            with open("names.csv","w",encoding="utf-8") as f:
                st  = ["name,sex,no\n","example,0,1"]
                f.writelines(st)
            r = showwarning("警告","检测到names.csv不存在，已为您创建样板文件，请修改")
            logging.warning("names.csv不存在")
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
                logging.warning("当前配置文件版本较低")
            elif config["VER_NO"] > VER_NO:
                r = showwarning("警告","当前配置文件版本较高，可能会出现一些玄学问题")
                logging.warning("当前配置文件版本较高")
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
            logging.warning("没有找到config.json")

    def handle_exception(sel,exception, value, trace):
        logging.error(traceback.format_exc())

class Shortcut(tkinter.Tk):
    def __init__(self):
        super().__init__()
        w = self.winfo_screenwidth()
        h = self.winfo_screenheight()
        self.geometry("100x100+%d+%d"%(w*0.7,h*0.7))
        self.overrideredirect(True)
        self.attributes('-topmost', True)
        sv_ttk.set_theme(darkdetect.theme())
        self.photo = None
        self.dragging = False
        self.pack_widgets()
        self.report_callback_exception = self.handle_exception
        logging.info("浮窗初始化完成")

    def handle_exception(sel,exception, value, trace):
        logging.error(traceback.format_exc())

    def pack_widgets(self):
        global img
        self.photo = ImageTk.PhotoImage(img)
        frame = ttk.Frame(self,width=100,height=100)
        frame.pack(anchor="center")
        can = tkinter.Canvas(frame,width=100,height=100)
        can.create_image(50,50,image=self.photo)
        can.pack()
        can.bind("<B1-Motion>", self.move_window)
        can.bind("<ButtonRelease-1>", self.calls)
        logging.info("浮窗组件绑定事件完成")
        menu = (pystray.MenuItem(text='打开软件窗口', action=self.calls),
                pystray.MenuItem(text='退出', action=self.quit_window)
                )
        icon = pystray.Icon("name", img, "NamePicker", menu)
        threading.Thread(target=icon.run, daemon=True).start()
        logging.info("浮窗组件设置完成")

    def move_window(self,event):
        self.dragging = True
        self.geometry("+{0}+{1}".format(event.x_root-50, event.y_root-50))

    def calls(self,event):
        if self.dragging:
            self.dragging = False
            logging.debug("结束拖拽")
        else:
            logging.debug("点击回调函数")
            app = App()
            app.mainloop()

    def quit_window(self):
        self.destroy()

if __name__ == "__main__":
    sh = Shortcut()
    sh.mainloop()