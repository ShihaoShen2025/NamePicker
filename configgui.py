import tkinter
from tkinter import ttk
import sv_ttk
import darkdetect
import json
from tkinter.messagebox import *

VERSION = "1.1.0rel"
VER_NO = 5
CODENAME = "Firefly"
class cfgpage(tkinter.Toplevel):
    def __init__(self,theme):
        global cfgvar
        super().__init__()
        self.geometry("450x320")
        self.title("NamePicker - 配置菜单")
        self.resizable(False, False)
        sv_ttk.set_theme(theme)
        cfgvar = [tkinter.IntVar(), tkinter.IntVar(),tkinter.IntVar(),tkinter.IntVar()]
        self.loadcfg()
        self.createWidget()

    def savecfg(self):
        cfg = {"VERSION":VERSION,
               "VER_NO":VER_NO,
               "CODENAME": CODENAME,
                "allowRepeat":self.getcfg(cfgvar[0]),
               "alwaysOnTop":self.getcfg(cfgvar[1]),
               "SupportCW":self.getcfg(cfgvar[2])}
        conf = json.dumps(cfg)
        with open("config.json","w",encoding="utf-8") as f:
            f.write(conf)
        res = showinfo("完成","更改已保存，进行一次抽选以应用更改")

    def createWidget(self):

        cfg = [ttk.Checkbutton(self, text="允许重复点名", variable=cfgvar[0]),
               ttk.Checkbutton(self, text="始终置顶", variable=cfgvar[1]),
               ttk.Checkbutton(self, text="课表软件支持\n启用后不会在主页显示抽选结果，需要安装CW/CI侧插件", variable=cfgvar[2]),
               ttk.Label(self,text="当前版本：%s - Codename %s"%(VERSION,CODENAME)),
               ttk.Button(self, text="保存配置", command=self.savecfg)]
        for i in range(len(cfg)):
            cfg[i].place(x=50, y=30 + 50 * i)

    def setcfg(self,t,param):
        if param:
            t.set(1)
        else:
            t.set(0)

    def getcfg(self,t):
        if t.get() == 1:
            return True
        else:
            return False

    def loadcfg(self):
        with open("config.json","r",encoding="utf-8") as f:
            conf = f.read()
        config = json.loads(conf)
        self.setcfg(cfgvar[0],config["allowRepeat"])
        self.setcfg(cfgvar[1],config["alwaysOnTop"])
        self.setcfg(cfgvar[2], config["SupportCW"])

if __name__ == "__main__":
    app = cfgpage(darkdetect.theme())
    app.mainloop()
