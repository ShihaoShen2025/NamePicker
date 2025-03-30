import tkinter
from tkinter import ttk
import sv_ttk
import darkdetect
import json
from tkinter.messagebox import *

VERSION = "1.1.2dev"
VER_NO = 7
CODENAME = "Sonetto"
class cfgpage(tkinter.Toplevel):
    def __init__(self):
        global cfgvar
        super().__init__()
        self.geometry("450x320")
        self.title("NamePicker - 配置菜单")
        sv_ttk.set_theme(darkdetect.theme())
        cfgvar = [tkinter.IntVar(), tkinter.IntVar(),tkinter.IntVar(),tkinter.StringVar(),tkinter.IntVar()]
        self.loadcfg()
        self.createWidget()

    def savecfg(self):
        cfg = {"VERSION":VERSION,
               "VER_NO":VER_NO,
               "CODENAME": CODENAME,
                "allowRepeat":self.getcfg(cfgvar[0]),
               "alwaysOnTop":self.getcfg(cfgvar[1]),
               "SupportCW":self.getcfg(cfgvar[2]),
               "logLevel":cfgvar[3].get(),
               "consoleOutput":self.getcfg(cfgvar[4])}
        conf = json.dumps(cfg)
        with open("config.json","w",encoding="utf-8") as f:
            f.write(conf)
        res = showinfo("完成","更改已保存，进行一次抽选以应用更改\n某些设置可能需要重启应用来应用")

    def createWidget(self):
        pages = ttk.Notebook(self)
        general = ttk.Frame(pages)
        pages.add(general,text="常规")
        debg = ttk.Frame(pages)
        pages.add(debg,text="调试")
        about = ttk.Frame(pages)
        pages.add(about,text="关于")

        cfg = [ttk.Checkbutton(general, text="允许重复点名", variable=cfgvar[0]),
               ttk.Checkbutton(general, text="始终置顶", variable=cfgvar[1]),
               ttk.Checkbutton(general, text="课表软件支持\n启用后不会在主页显示抽选结果，需要安装CW/CI侧插件", variable=cfgvar[2])
               ]
        for i in range(len(cfg)):
            cfg[i].place(relx=0.1, rely=0.1+0.2*i)

        inf = ttk.Label(debg,text="此界面所有选项仅供调试\n如果您不知道您在做什么，请不要随意操作")
        inf.place(relx=0.1,rely=0.1)
        levlab = ttk.Label(debg,text="日志等级")
        levlab.place(relx=0.1, rely=0.3)
        lev = ttk.OptionMenu(debg, cfgvar[3], "Warning", "Error", "Warning", "Info", "Debug")
        lev.place(relx=0.5,rely=0.3)
        console = ttk.Checkbutton(debg, text="在控制台（而非日志文件）中输出日志", variable=cfgvar[4])
        console.place(relx=0.1,rely=0.5)


        prod = ttk.Label(about,text="NamePicker - 一款简洁的点名器")
        prod.place(relx=0.1,rely=0.1)
        ver = ttk.Label(about, text="当前版本：%s - Codename %s" % (VERSION, CODENAME))
        ver.place(relx=0.1,rely=0.3)
        aut = ttk.Label(about, text="作者：灵魂歌手er（GitHub @LHGS-github\n本软件完全开源免费，并遵循MIT协议")
        aut.place(relx=0.1, rely=0.5)

        save = ttk.Button(self, text="保存配置", command=self.savecfg)
        save.place(relx=0.4,rely=0.8)

        pages.pack(expand=True, fill="both")

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
        cfgvar[3].set(config["logLevel"])
        self.setcfg(cfgvar[4], config["consoleOutput"])

if __name__ == "__main__":
    app = cfgpage()
    app.mainloop()
