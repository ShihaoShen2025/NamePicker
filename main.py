import json
import importlib
import os
import sys
import pandas as pd
import tempfile
import random
import traceback
from loguru import logger
from PySide6.QtCore import QObject, Slot,Property,Signal
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QDesktopServices,QIcon,QGuiApplication
from RinUI import RinUIWindow
if os.name == 'nt':
    from win32com.client import Dispatch

temp_dir = tempfile.gettempdir()
VERSION = "v2.0.3dev"
CODENAME = "Robin"
APIVER = 1
# error_dialog = None
# tray = None
# unlocked = [False,False]
# plugin = {}
# plugin_info = {}
# plugin_settings = {}
# plugin_customkey = []
# plugin_customkey_title = []
# plugin_filters = []
# plugin_filters_name = []
# plugin_icon = {}
# plugin_path = {}
# def load_plugins():
#     for i in os.listdir("plugins"):
#         if not (os.path.exists("plugins/%s/info.json"%i) and os.path.exists("plugins/%s/icon.png"%i) and os.path.exists("plugins/%s/main.py"%i)):
#             logger.warning("目录%s没有有效插件"%i)
#             continue
#         elif os.path.exists("plugins/%s/DEL"%i):
#             os.remove("plugins/%s"%i)
#             logger.info("插件被成功移除")
#             continue
#         else:
#             with open("plugins/%s/info.json"%i,"r",encoding="utf-8") as f:
#                 ct = f.read()
#                 js = json.loads(ct)
#                 if js["api"] > cfg.get(cfg.apiver):
#                     logger.warning("当前插件API版本过高，拒绝加载")
#                     continue
#                 plugin_info[js["id"]] = js
#             pgin = importlib.import_module("plugins.%s.main"%i)
#             plugin_icon[js["id"]] = "plugins/%s/icon.png"%i
#             plugin_path[js["id"]] = "plugins/%s" % i
#             if hasattr(pgin,"Settings") and not os.path.exists("plugins/%s/DISABLED"%i):
#                 plugin_settings[js["id"]] = pgin.Settings()
#             if hasattr(pgin,"Plugin"):
#                 if not os.path.exists("plugins/%s/DISABLED"%i):
#                     plugin[js["id"]] = pgin.Plugin()
#                     for i in plugin[js["id"]].customKey:
#                         plugin_customkey.append(i)
#                     for i in plugin[js["id"]].customKeyTitle:
#                         plugin_customkey_title.append(i)
#                     for i in plugin[js["id"]].filters:
#                         plugin_filters.append(i)
#                     for i in plugin[js["id"]].filtersName:
#                         plugin_filters_name.append(i)
#                 else:
#                     logger.warning("插件%s已被禁用" % js["id"])
#                     continue
#             logger.info("加载插件：%s成功"%js["id"])

# def apply_customkey():
#     with open("names.csv", "r", encoding="utf-8") as f:
#         namesread = f.readlines()
#         for i in range(len(namesread)):
#             namesread[i] = namesread[i].strip("\n")
#         for i in range(len(plugin_customkey)):
#             if plugin_customkey[i] not in namesread[0]:
#                 namesread[0] += ",%s"%plugin_customkey[i]
#                 for j in range(len(namesread)):
#                     if j == 0:
#                         continue
#                     namesread[j] += ",Nope"

#     with open("names.csv","w",encoding="utf-8") as f:
#         namewrite = []
#         for i in range(len(namesread)):
#             namewrite.append(namesread[i]+"\n")
#         f.writelines(namewrite)


# def hookExceptions(exc_type, exc_value, exc_tb):
#     error_details = ''.join(traceback.format_exception(exc_type, exc_value, exc_tb))
#     if "TypeError: disconnect() of all signals failed" in error_details:
#         return
#     logger.error(error_details)
#     if not error_dialog:
#         # w = ErrorDialog(error_details)
#         # w.exec()
#         pass
# sys.excepthook = hookExceptions

class Choose:
    def __init__(self,sexFavor:str,numFavor:str):
        self.names = {}
        self.sexlen = [0,0,0]
        self.sexl = [[],[],[]]
        self.numlen = [0,0,0]
        self.numl = [[],[],[]]
        self.chosen = []
        self.sexFavor = sexFavor
        self.numFavor = numFavor
        self.loadname()

    def pick(self):
        global cfg
        if self.sexFavor != "都抽":
            if self.sexFavor == "只抽男":
                le = self.sexlen[0]
                tar = self.sexl[0]
            elif self.sexFavor == "只抽女":
                le = self.sexlen[1]
                tar = self.sexl[1]
            else:
                le = self.sexlen[2]
                tar = self.sexl[2]
        else:
            le = self.length
            tar = self.names["name"]

        if self.numFavor != "都抽":
            if self.numFavor == "只抽双数":
                tar = list(set(tar) & set(self.numl[0]))
                le = len(tar)
            else:
                tar = list(set(tar) & set(self.numl[1]))
                le = len(tar)
        # if plugin_filters:
        #     for i in range(len(tar)):
        #         for j in range(len(plugin_filters_name)):
        #             if self.filswitch[j].isChecked() and not plugin_filters[j](tar[i]):
        #                 tar.remove(tar[i])
        le = len(tar)
        if le != 0:
            chs = random.randint(0, le - 1)
            if not cfg.get("General","allowRepeat"):
                if len(self.chosen) >= le:
                    self.chosen = []
                    chs = random.randint(0, le - 1)
                else:
                    while chs in self.chosen:
                        chs = random.randint(0, le - 1)
                self.chosen.append(chs)
                logger.debug(self.chosen)
            tmp = {"name":tar[chs],"no":str(self.names["no"][self.names["name"].index(tar[chs])])}
            for i in self.names.keys():
                if i == "name" or i == "no":
                    continue
                tmp[i] = str(self.names[i][self.names["name"].index(tar[chs])])
            return tmp
        else:
            return "尚未抽选"

    def pickcb(self,nb:int):
        logger.debug("pickcb被调用")
        # for i in plugin.keys():
        #     plugin[i].beforePick()
        namet = []
        namel = []
        for i in range(nb):
            n = self.pick()
            if n != "尚未抽选":
                namet.append(n)
            else:
                return ["bydcnm","没有符合条件的学生"]

        if cfg.get("General","supportCS"):
            with open("%s\\unread" % temp_dir, "w", encoding="utf-8") as f:
                f.write("111")
            with open("%s\\res.txt" % temp_dir, "w", encoding="utf-8") as f:
                for i in namet:
                    namel.append("%s（%s）" % (i["name"], i["no"]))
                f.writelines(namel)
            logger.info("文件存储完成")
        else:
            for i in namet:
                    namel.append("%s（%s）" % (i["name"], i["no"]))
            return namel
        # for i in plugin.keys():
        #     plugin[i].afterPick(namet)

    def loadname(self):
        try:
            name = pd.read_csv("names.csv", sep=",", header=0)
            name = name.to_dict()
            self.names["name"] = list(name["name"].values())
            self.names["sex"] = list(name["sex"].values())
            self.names["no"] = list(name["no"].values())
            # for i in plugin_customkey:
            #     self.names[i] = list(name[i].values())
            for k in self.names.keys():
                for i in range(len(self.names[k])):
                    self.names[k][i] = str(self.names[k][i])
            self.length =len(name["name"])
            self.sexlen[0] = self.names["sex"].count("0")
            self.sexlen[1] = self.names["sex"].count("1")
            self.sexlen[2] = self.names["sex"].count("2")
            for i in self.names["name"]:
                if int(self.names["sex"][self.names["name"].index(i)]) == 0:
                    self.sexl[0].append(i)
                elif int(self.names["sex"][self.names["name"].index(i)]) == 1:
                    self.sexl[1].append(i)
                else:
                    self.sexl[2].append(i)

            for i in self.names["name"]:
                if int(self.names["no"][self.names["name"].index(i)])%2==0:
                    self.numl[0].append(i)
                else:
                    self.numl[1].append(i)
            self.numlen[0] = len(self.numl[0])
            self.numlen[1] = len(self.numl[1])
            logger.info("名单加载完成")
        except FileNotFoundError:
            logger.warning("没有找到名单文件")
            with open("names.csv","w",encoding="utf-8") as f:
                st  = ["name,sex,no\n","example,0,1"]
                f.writelines(st)
            self.loadname()

def setStartup():
    if os.name != 'nt':
        return
    file_path='%s/main.exe'%os.path.dirname(os.path.abspath(__file__))
    icon_path = 'assets/favicon.ico'
    startup_folder = os.path.join(os.getenv('APPDATA'), 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup')
    name = os.path.splitext(os.path.basename(file_path))[0]  # 使用文件名作为快捷方式名称
    shortcut_path = os.path.join(startup_folder, f'{name}.lnk')
    shell = Dispatch('WScript.Shell')
    shortcut = shell.CreateShortCut(shortcut_path)
    shortcut.Targetpath = file_path
    shortcut.WorkingDirectory = os.path.dirname(file_path)
    shortcut.IconLocation = icon_path  # 设置图标路径
    shortcut.save()

def removeStartup():
    file_path = '%s/main.exe' % os.path.dirname(os.path.abspath(__file__))
    name = os.path.splitext(os.path.basename(file_path))[0]
    startup_folder = os.path.join(os.getenv('APPDATA'), 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup')
    shortcut_path = os.path.join(startup_folder, f'{name}.lnk')
    if os.path.exists(shortcut_path):
        os.remove(shortcut_path)

class Config:
    def __init__(self,filename:str,rules:dict,default:dict):
        self.filename = filename
        with open(filename,"r",encoding="utf-8") as f:
            self.cfgf = f.read()
            self.cfg = json.loads(self.cfgf)
        for i in list(rules.keys()):
            if i not in self.cfg.keys():
                self.cfg[i] = {}
            for j in list(rules[i].keys()):
                if j not in rules[i].keys():
                    self.cfg[i][j] = default[i][j]
                elif not self.val(i,j,self.cfg[i][j],rules):
                        self.cfg[i][j] = default[i][j]

    def val(self,i:str,j:str,chk,rules:dict):
        if type(rules[i][j]) == list:
            if ((rules[i][j][0] == "range" and (rules[i][j][1] > chk or rules[i][j][2] < chk)) 
                or (rules[i][j][0] == "option" and chk not in rules[i][j]) 
                or (rules[i][j][0] == "list" and type(chk) != list)):
                return False
        elif type(chk) != rules[i][j]:
            return False
        else:
            return True

    def get(self,cls:str,key:str):
        return self.cfg[cls][key]
    
    def set(self,cls:str,key:str,val):
        self.cfg[cls][key] = val
        with open(self.filename,"w",encoding="utf-8") as f:
            f.write(json.dumps(self.cfg))

CFGRULE = {
    "General": {"allowRepeat": bool,"autoStartup": bool,"chooseKey": str,"supportCS": bool},
    "Version": {"apiver": ["range",2,2]},
    "Huanyu": {"ecoMode": bool,"justice": bool},
    "Debug": {"logLevel": ["option","DEBUG","INFO","WARNING","ERROR"]}
}

CFGDEFAULT = {
    "General": {"allowRepeat": False,"autoStartup": False,"chooseKey": "ctrl+w","supportCS": False},
    "Version": {"apiver": 2},
    "Huanyu": {"ecoMode": False,"justice": False},
    "Debug": {"logLevel": "INFO"}
}

cfg = Config("config.json",CFGRULE,CFGDEFAULT)

if os.path.exists("out.log"):
    os.remove("out.log")
logger.remove(0)
logger.add("out.log")
logger.add(sys.stderr, level=cfg.get("Debug","logLevel"))
logger.info("「她将自己的生活形容为一首歌，而那首歌的开始阴沉而苦涩。⌋")
core = Choose("都抽","都抽")

class UI(RinUIWindow):
    def __init__(self):
        super().__init__("pages/main.qml")
        self.bridge = Bridge()
        self.engine.rootContext().setContextProperty("Bridge", self.bridge)

class Bridge(QObject):
    @Slot(str,str,str,result=list)
    def Pick(self,num,sexf,numf):
        core.sexFavor = sexf
        core.numFavor = numf
        try:
            return core.pickcb(int(num))
        except ValueError:
            return core.pickcb(int(1))
        
    @Slot(str,str,result=list)
    def GetCfg(self,cls,key):
        return [cfg.get(cls,key)]
    
    @Slot(str,str,list)
    def SetCfg(self,cls,key,val):
        if cfg.val(cls,key,val[0],CFGRULE):
            cfg.set(cls,key,val[0])

    @Slot(int,result=int)
    def GetDbg(self,cls):
        return ["DEBUG","INFO","WARNING","ERROR"].index(cfg.get("Debug","logLevel"))

    @Slot(bool)
    def Startup(self,stat):
        if stat:
            setStartup()
        else:
            removeStartup()

    @Property(str)
    def VerTxt(self):
        return "当前版本：%s - Codename %s"%(VERSION,CODENAME)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("../assets/favicon.ico"))
    main = UI()
    app.exec()