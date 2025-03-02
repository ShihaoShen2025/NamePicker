import tkinter
from tkinter import ttk
import sv_ttk
import darkdetect
import json
from tkinter.messagebox import *

root = tkinter.Tk()
root.geometry("250x200")
root.title("配置菜单")
sv_ttk.set_theme(darkdetect.theme())

def savecfg():
    global cfgvar
    cfg = {"allowRepeat":cfgvar[0].get(),
           "alwaysOnTop":cfgvar[1].get()}
    conf = json.dumps(cfg)
    with open("config.json","w",encoding="utf-8") as f:
        f.write(conf)
    res = showinfo("完成","更改已保存，请重启主程序以应用更改")

cfgvar = [tkinter.IntVar(),tkinter.IntVar()]
cfg = [ttk.Checkbutton(root,text="允许重复点名",variable=cfgvar[0]),
       ttk.Checkbutton(root,text="始终置顶",variable=cfgvar[1]),
       ttk.Button(root,text="保存配置",command=savecfg)]

def setcfg(t,param):
    if param:
        t.set(1)
    else:
        t.set(0)
def loadcfg():
    with open("config.json","r",encoding="utf-8") as f:
        conf = f.read()
    config = json.loads(conf)
    setcfg(cfgvar[0],config["allowRepeat"])
    setcfg(cfgvar[1],config["alwaysOnTop"])

loadcfg()

for i in range(len(cfg)):
    cfg[i].place(x=50,y=50+50*i)

