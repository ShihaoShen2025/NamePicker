import sys
import pandas as pd
import tempfile
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from qfluentwidgets import *

temp_dir = tempfile.gettempdir()
VERSION = "1.1.2dev"
VER_NO = 7
CODENAME = "Sonetto"

QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

class Choose(QFrame):

    def __init__(self, text: str, parent=None):
        super().__init__(parent=parent)
        self.names = []
        self.sexlen = [0,0,0]
        self.sexl = [[],[],[]]
        self.numlen = [0,0,0]
        self.numl = [[],[],[]]
        self.loadname()

        self.hBoxLayout = QHBoxLayout(self)
        self.options = QVBoxLayout(self)

        self.pickbn = PrimaryPushButton("点击抽选")
        self.pickbn.clicked.connect(self.pickcb)
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
        self.pickNum.setRange(1, len(self.names))
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

    def pick(self):
        pass

    def pickcb(self):
        self.table.setRowCount(self.pickNum.value())
        namet = []
        for i in range(self.pickNum.value()):
            pass
        for i, songInfo in enumerate(namet):
            for j in range(5):
                self.table.setItem(i, j, QTableWidgetItem(songInfo[j]))


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
            sys.exit(114514)

class App(FluentWindow):
    def __init__(self):
        super().__init__()
        qconfig.theme = Theme.AUTO
        setTheme(Theme.AUTO)
        self.Choose = Choose("随机抽选",self)

        self.initNavigation()
        self.initWindow()

    def initNavigation(self):
        self.addSubInterface(self.Choose, FluentIcon.HOME, "随机抽选")

    def initWindow(self):
        self.resize(700, 500)
        self.setWindowIcon(QIcon('assets/NamePicker.png'))
        self.setWindowTitle('NamePicker')


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = App()
    w.show()
    app.exec()