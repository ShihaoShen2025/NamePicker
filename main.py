import os
import sys
import pandas as pd
import tempfile
import random
import traceback
from loguru import logger
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon,QPainter,QPixmap
from qfluentwidgets import *
if os.name == 'nt':
    from win32com.client import Dispatch

temp_dir = tempfile.gettempdir()
VERSION = "v2.0.1dev"
CODENAME = "Robin"

QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

class Config(QConfig):
    allowRepeat = ConfigItem("General","allowRepeat",False,BoolValidator())
    supportCS = ConfigItem("General", "supportCS", False, BoolValidator())
    chooseKey = ConfigItem("General","chooseKey","ctrl+w")
    autoStartup = ConfigItem("General","autoStartup",False,BoolValidator())
    eco = ConfigItem("Huanyu", "ecoMode", False, BoolValidator())
    justice = ConfigItem("Huanyu", "justice", False, BoolValidator())
    logLevel = OptionsConfigItem("Debug", "logLevel", "INFO", OptionsValidator(["DEBUG", "INFO", "WARNING","ERROR"]), restart=True)

cfg = Config()
qconfig.load('config.json', cfg)

if os.path.exists("out.log"):
    os.remove("out.log")
logger.remove(0)
logger.add("out.log")
logger.add(sys.stderr, level=cfg.get(cfg.logLevel))

logger.info("「她将自己的生活形容为一首歌，而那首歌的开始阴沉而苦涩。⌋")

def hookExceptions(exc_type, exc_value, exc_tb):
    error_details = ''.join(traceback.format_exception(exc_type, exc_value, exc_tb))
    logger.error(error_details)
sys.excepthook = hookExceptions

class Choose(QFrame):

    def __init__(self, text: str, parent=None):
        super().__init__(parent=parent)
        self.names = []
        self.sexlen = [0,0,0]
        self.sexl = [[],[],[]]
        self.numlen = [0,0,0]
        self.numl = [[],[],[]]
        self.chosen = []
        self.loadname()

        self.hBoxLayout = QHBoxLayout(self)
        self.options = QVBoxLayout(self)

        if cfg.get(cfg.justice):
            self.just = StrongBodyLabel("NamePicker绝对没有暗改概率功能")
            self.options.addWidget(self.just)

        self.pickbn = PrimaryPushButton("点击抽选")
        self.pickbn.clicked.connect(self.pickcb)
        self.pickbn.setShortcut(cfg.get(cfg.chooseKey))
        self.pickbn.adjustSize()
        self.options.addWidget(self.pickbn,5)

        self.table = TableWidget(self)
        self.table.setBorderVisible(True)
        self.table.setBorderRadius(8)
        self.table.setWordWrap(False)
        self.table.setRowCount(10)
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["姓名","学号"])

        self.pn = QWidget()
        self.pnl = QHBoxLayout(self)
        self.pnLabel = SubtitleLabel("抽选数量", self)
        self.pickNum = SpinBox()
        self.pickNum.setRange(1, len(self.names[0]))
        self.pnl.addWidget(self.pnLabel, 10)
        self.pnl.addWidget(self.pickNum, 5)
        self.pn.setLayout(self.pnl)
        self.options.addWidget(self.pn,5)

        self.sep = QWidget()
        self.sepl = QHBoxLayout(self)
        self.seLabel = SubtitleLabel("性别偏好", self)
        self.sexCombo = ComboBox()
        self.sexCombo.addItems(["都抽","只抽男","只抽女","只抽特殊性别"])
        self.sepl.addWidget(self.seLabel, 10)
        self.sepl.addWidget(self.sexCombo, 5)
        self.sep.setLayout(self.sepl)
        self.options.addWidget(self.sep, 5)

        self.nup = QWidget()
        self.nul = QHBoxLayout(self)
        self.nuLabel = SubtitleLabel("学号偏好", self)
        self.numCombo = ComboBox()
        self.numCombo.addItems(["都抽", "只抽单数", "只抽双数"])
        self.nul.addWidget(self.nuLabel, 10)
        self.nul.addWidget(self.numCombo, 5)
        self.nup.setLayout(self.nul)
        self.options.addWidget(self.nup, 5)

        self.opt = QWidget()
        self.opt.setLayout(self.options)

        self.hBoxLayout.addWidget(self.table,2)
        self.hBoxLayout.addWidget(self.opt,3,Qt.AlignCenter)
        self.setObjectName(text.replace(' ', 'Choose'))
        logger.info("主界面初始化完成")

        if cfg.get(cfg.eco):
            InfoBar.success(
                title='环保模式已启用',
                content="NamePicker低碳模式将大幅降低碳排放，同时大幅增加设备寿命",
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=3000,
                parent=self
            )
            logger.info("NamePicker低碳模式将大幅降低碳排放，同时大幅增加设备寿命")

    def pick(self):
        global cfg
        if self.sexCombo.currentText() != "都抽":
            if self.sexCombo.currentText() == "只抽男":
                le = self.sexlen[0]
                tar = self.sexl[0]
            elif self.sexCombo.currentText() == "只抽女":
                le = self.sexlen[1]
                tar = self.sexl[1]
            else:
                le = self.sexlen[2]
                tar = self.sexl[2]
        else:
            le = self.length
            tar = self.names[0]

        if self.numCombo.currentText() != "都抽":
            if self.numCombo.currentText() == "只抽双数":
                tar = list(set(tar) & set(self.numl[0]))
                le = len(tar)
            else:
                tar = list(set(tar) & set(self.numl[1]))
                le = len(tar)
        if le != 0:
            chs = random.randint(0, le - 1)
            if not cfg.get(cfg.allowRepeat):
                if len(self.chosen) >= le:
                    self.chosen = []
                    chs = random.randint(0, le - 1)
                else:
                    while chs in self.chosen:
                        chs = random.randint(0, le - 1)
                self.chosen.append(chs)
                logger.debug(self.chosen)
            return [tar[chs], self.names[2][self.names[0].index(tar[chs])]]
        else:
            return ["尚未抽选", "尚未抽选"]

    def pickcb(self):
        logger.debug("pickcb被调用")
        self.table.setRowCount(self.pickNum.value())
        namet = []
        namel = []
        for i in range(self.pickNum.value()):
            namet.append(self.pick())
        if cfg.get(cfg.supportCS):
            with open("%s\\unread" % temp_dir, "w", encoding="utf-8") as f:
                f.write("111")
            with open("%s\\res.txt" % temp_dir, "w", encoding="utf-8") as f:
                for i in namet:
                    namel.append("%s（%s）" % (i[0], i[1]))
                f.writelines(namel)
            logger.info("文件存储完成")
        else:
            for i, t in enumerate(namet):
                for j in range(2):
                    self.table.setItem(i, j, QTableWidgetItem(t[j]))
            logger.debug("表格设置完成")

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
            logger.info("名单加载完成")
        except FileNotFoundError:
            logger.warning("没有找到名单文件")
            with open("names.csv","w",encoding="utf-8") as f:
                st  = ["name,sex,no\n","example,0,1"]
                f.writelines(st)
            w = Dialog("没有找到名单文件", "没有找到名单文件，已为您创建默认名单，请自行编辑", self)
            w.exec()
            self.loadname()

class NameEdit(QFrame):
    def __init__(self, text: str, parent=None):
        super().__init__(parent=parent)
        self.names = []
        self.nametable = []
        self.loadname()
        self.editing = 0

        self.vbox = QVBoxLayout(self)
        self.title = TitleLabel("名单编辑")
        self.vbox.addWidget(self.title)

        self.expl = BodyLabel("所有更改都将自动保存至文件，可以直接编辑表格内容")
        self.vbox.addWidget(self.expl)

        self.table = TableWidget(self)
        self.table.setBorderVisible(True)
        self.table.setBorderRadius(8)
        self.table.setWordWrap(False)
        self.table.setRowCount(len(self.nametable))
        self.table.setColumnCount(3)
        self.table.adjustSize()
        self.table.setHorizontalHeaderLabels(["姓名", "性别", "学号"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.opv = QWidget()
        self.option = QHBoxLayout(self.opv)
        self.add = PushButton(FluentIcon.ADD,"添加一行")
        self.rem = PushButton(FluentIcon.DELETE,"删除选中行")
        self.add.clicked.connect(self.addrow)
        self.rem.clicked.connect(self.delrow)
        self.option.addWidget(self.add)
        self.option.addWidget(self.rem)
        self.vbox.addWidget(self.opv)

        self.refresh()
        self.vbox.addWidget(self.table)
        self.table.clicked.connect(self.select)
        self.table.itemChanged.connect(self.savename)
        self.selected_items = self.table.selectedItems()
        self.selected_data = [item.text() for item in self.selected_items]

        self.setObjectName(text.replace(' ', 'NameEdit'))

    def refresh(self):
        self.table.setRowCount(len(self.nametable))
        for i, t in enumerate(self.nametable):
            for j in range(3):
                self.table.setItem(i, j, QTableWidgetItem(t[j]))

    def addrow(self):
        self.nametable.append(["example","男","0"])
        self.refresh()

    def delrow(self):
        del self.nametable[self.editing]
        self.editing = 0
        self.refresh()

    def select(self):
        self.selected_items = self.table.selectedItems()
        self.selected_data = [item.text() for item in self.selected_items]
        self.editing = self.nametable.index(self.selected_data)
        logger.debug(self.selected_data)
        logger.debug(self.editing)

    def savename(self):
        self.selected_items = self.table.selectedItems()
        self.selected_data = [item.text() for item in self.selected_items]
        self.nametable[self.editing] = self.selected_data
        logger.debug(self.nametable)
        with open("names.csv","w",encoding="utf-8") as f:
            namewrite = ["name,sex,no\n"]
            t = 0
            for i in range(len(self.nametable)):
                logger.debug(self.nametable[i])
                if self.nametable[i][1] == "男" or self.nametable[i][1] == "0":
                    t = 0
                elif self.nametable[i][1] == "女" or self.nametable[i][1] == "1":
                    t = 1
                else:
                    t = 2
                namewrite.append(",".join([self.nametable[i][0],str(t),str(self.nametable[i][2])])+"\n")
            f.writelines(namewrite)

    def loadname(self):
        name = pd.read_csv("names.csv",sep=",",header=0,dtype={'name': str, 'sex': int, "no":int})
        name = name.to_dict()
        self.names.append(list(name["name"].values()))
        self.names.append(list(name["sex"].values()))
        self.names.append(list(name["no"].values()))
        for i in range(len(self.names[0])):
            if self.names[1][i] == 0:
                t = "男"
            elif self.names[1][i] == 1:
                t = "女"
            else:
                t = "其他"
            self.nametable.append([self.names[0][i],t,str(self.names[2][i])])
        logger.debug(self.nametable)
        logger.info("名单加载完成")

class Settings(QFrame):
    def __init__(self, text: str, parent=None):
        global cfg
        super().__init__(parent=parent)
        self.setObjectName(text.replace(' ', 'Settings'))
        self.df = QVBoxLayout(self)
        self.scrollArea = ScrollArea()
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.optv =QWidget()
        self.opts = QVBoxLayout(self.optv)
        self.tlog = PushButton(FluentIcon.DOCUMENT,"测试日志输出")
        self.tcrash = PushButton(FluentIcon.CLOSE,"测试引发崩溃")
        self.tlog.clicked.connect(self.testLog)
        self.tcrash.clicked.connect(self.testCrash)
        self.cKey=SettingCard(
            icon=FluentIcon.FONT,
            title="抽选快捷键",
            content="设置抽选的快捷键（不区分大小写，使用英文加号(+)串联多个按键），重启生效"
        )
        self.cKeyInput = LineEdit()
        self.cKeyInput.setPlaceholderText("输入快捷键")
        self.cKeyInput.setText(cfg.get(cfg.chooseKey))
        self.cKey.hBoxLayout.addStretch(20)
        self.cKey.hBoxLayout.addWidget(self.cKeyInput)
        self.cKey.hBoxLayout.addStretch(1)
        self.cKeyInput.textChanged.connect(lambda :cfg.set(cfg.chooseKey,self.cKeyInput.text()))
        self.sets = [SubtitleLabel("常规"),
        SwitchSettingCard(
            configItem=cfg.allowRepeat,
            icon=FluentIcon.LIBRARY,
            title="允许重复点名",
            content="允许点到重复名字"
        ),
        SwitchSettingCard(
            configItem=cfg.supportCS,
            icon=FluentIcon.LINK,
            title="课表软件联动",
            content="启用后将在ClassIsland/Class Widgets上（而非主界面）显示抽选结果，需要安装对应插件"
        ),
        SwitchSettingCard(
            configItem=cfg.autoStartup,
            icon=FluentIcon.POWER_BUTTON,
            title="开机自启",
            content="开机时自动启动（对于非Windows系统无效）"
        ),
        self.cKey,
        SubtitleLabel("调试"),
        ComboBoxSettingCard(
            configItem=cfg.logLevel,
            icon=FluentIcon.DEVELOPER_TOOLS,
            title="日志记录级别",
            content="日志的详细程度（重启以应用更改）",
            texts=["DEBUG", "INFO", "WARNING","ERROR"]
        ),self.tlog,
        self.tcrash,
        SubtitleLabel("欢愉（太有乐子了）"),
        SwitchSettingCard(
            configItem=cfg.eco,
            icon=FluentIcon.LEAF,
            title="环保模式",
            content="NamePicker致力于减少碳排放"
        ),SwitchSettingCard(
            configItem=cfg.justice,
            icon=FluentIcon.SPEED_MEDIUM,
            title="绝对公平模式",
            content="启用后，将在主页显示一条提示"
        )]
        for i in self.sets:
            self.opts.addWidget(i)
        self.scrollArea.setStyleSheet("QScrollArea{background: transparent; border: none}")
        self.scrollArea.setWidget(self.optv)
        self.optv.setStyleSheet("QWidget{background: transparent}")
        self.df.addWidget(TitleLabel("设置"))
        self.df.addWidget(self.scrollArea)
        QScroller.grabGesture(self.scrollArea.viewport(), QScroller.LeftMouseButtonGesture)
        cfg.autoStartup.valueChanged.connect(self.startupChange)
        logger.info("设置界面初始化完成")

    def startupChange(self):
        if cfg.get(cfg.autoStartup):
            self.setStartup()
        else:
            self.removeStartup()

    def setStartup(self):
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

    def removeStartup(self):
        file_path = '%s/main.exe' % os.path.dirname(os.path.abspath(__file__))
        name = os.path.splitext(os.path.basename(file_path))[0]
        startup_folder = os.path.join(os.getenv('APPDATA'), 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup')
        shortcut_path = os.path.join(startup_folder, f'{name}.lnk')
        if os.path.exists(shortcut_path):
            os.remove(shortcut_path)

    def testLog(self):
        logger.debug("这是Debug日志")
        logger.info("这是Info日志")
        logger.warning("这是Warning日志")
        logger.error("这是Error日志")

    def testCrash(self):
        raise Exception("NamePicker实际上没有任何问题，是你自己手贱引发的崩溃")

class About(QFrame):
    def __init__(self, text: str, parent=None):
        global cfg
        super().__init__(parent=parent)
        self.setObjectName(text.replace(' ', 'About'))
        self.df = QVBoxLayout(self)
        self.about = TitleLabel("关于")
        self.image = ImageLabel("assets/NamePicker.png")
        self.ver = SubtitleLabel("NamePicker %s - Codename %s"%(VERSION,CODENAME))
        self.author = BodyLabel("By 灵魂歌手er（Github @LHGS-github）")
        self.cpleft = BodyLabel("本软件基于GNU GPLv3获得授权")

        self.linkv = QWidget()
        self.links = QHBoxLayout(self.linkv)
        self.ghrepo = HyperlinkButton(FluentIcon.GITHUB, "https://github.com/NamePickerOrg/NamePicker", 'GitHub Repo')
        self.docsite = HyperlinkButton(FluentIcon.DOCUMENT,"https://namepicker-docs.netlify.app/","官方文档")
        self.links.addWidget(self.ghrepo)
        self.links.addWidget(self.docsite)

        self.df.addWidget(self.about)
        self.df.addWidget(self.image)
        self.df.addWidget(self.ver)
        self.df.addWidget(self.author)
        self.df.addWidget(self.cpleft)
        self.df.addWidget(self.linkv)
        logger.info("关于界面初始化")

class App(FluentWindow):
    def __init__(self):
        super().__init__()
        qconfig.theme = Theme.AUTO
        setTheme(Theme.AUTO)
        self.Choose = Choose("随机抽选",self)
        self.NameEdit = NameEdit("名单编辑", self)
        self.Settings = Settings("设置",self)
        self.About = About("关于", self)
        self.initNavigation()
        self.initWindow()
        logger.info("主界面初始化")

    def initNavigation(self):
        self.addSubInterface(self.Choose, FluentIcon.HOME, "随机抽选")
        self.addSubInterface(self.NameEdit, FluentIcon.EDIT, "名单编辑")
        self.addSubInterface(self.Settings, FluentIcon.SETTING, '设置', NavigationItemPosition.BOTTOM)
        self.addSubInterface(self.About, FluentIcon.INFO, '关于', NavigationItemPosition.BOTTOM)

    def initWindow(self):
        self.resize(700, 500)
        self.setWindowIcon(QIcon('assets/NamePicker.png'))
        self.setWindowTitle('NamePicker')

    def closeEvent(self, event):
        self.hide()
        event.ignore()

class SystemTrayIcon(QSystemTrayIcon):
    def __init__(self, parent):
        super().__init__(parent=parent)
        self.setIcon(parent.windowIcon())

        self.menu = SystemTrayMenu(parent=parent)
        self.menu.addActions([
            Action("打开主界面",triggered=parent.show_main_window),
            Action("重启",triggered=lambda:os.execl(sys.executable, sys.executable, *sys.argv)),
            Action('退出', triggered=lambda:sys.exit(0))
        ])
        self.setContextMenu(self.menu)


class TrayWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setFixedSize(100, 100)
        self.setWindowIcon(QIcon('assets/NamePickerCircle.png'))
        screen = QDesktopWidget().screenGeometry()
        self.move(int(screen.width()*0.7), int(screen.height()*0.7))
        self.systemTrayIcon = SystemTrayIcon(self)
        self.systemTrayIcon.show()

        self.drag_start_pos = None
        self.main_window = App()
        self.main_window.hide()
        self.drag = False

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_start_pos = event.globalPos()
            event.accept()

    def mouseMoveEvent(self, event):
        if self.drag_start_pos is not None and event.buttons() == Qt.LeftButton:
            self.drag = True
            delta = event.globalPos() - self.drag_start_pos
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.drag_start_pos = event.globalPos()
            event.accept()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton and self.drag_start_pos:
            if not self.drag:
                if not cfg.get(cfg.supportCS):
                    self.show_main_window()
                else:
                    self.main_window.Choose.pickcb()
            else:
                self.drag = False
            self.drag_start_pos = None
            event.accept()

    def show_main_window(self):
        self.main_window.show()
        self.main_window.activateWindow()

    def paintEvent(self, event):
        painter = QPainter(self)
        pixmap = QPixmap('assets/NamePickerCircle.png')
        painter.drawPixmap(self.rect(), pixmap)
        painter.setCompositionMode(QPainter.CompositionMode_SourceIn)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    tray = TrayWindow()
    tray.show()
    sys.exit(app.exec_())