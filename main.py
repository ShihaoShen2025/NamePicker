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

class Choose(QFrame):

    def __init__(self, text: str, parent=None):
        super().__init__(parent=parent)
        self.names = []
        self.sexlen = [0,0,0]
        self.sexl = [[],[],[]]
        self.numlen = [0,0,0]
        self.numl = [[],[],[]]
        self.loadname()

        self.label = SubtitleLabel(text, self)
        self.hBoxLayout = QHBoxLayout(self)
        self.options = QVBoxLayout(self)

        self.pickbn = PrimaryPushButton("点击抽选")
        self.pickbn.clicked.connect(self.pickcb)
        self.pickbn.adjustSize()
        self.options.addWidget(self.pickbn,5)
        self.pickNum = SpinBox()
        self.pickNum.setRange(1, len(self.names))
        self.options.addWidget(self.pickNum, 5)

        self.opt = QWidget()
        self.opt.setLayout(self.options)

        setFont(self.label, 24)
        self.label.setAlignment(Qt.AlignCenter)
        self.hBoxLayout.addWidget(self.label, 1, Qt.AlignCenter)
        self.hBoxLayout.addWidget(self.opt,1,Qt.AlignCenter)
        self.setObjectName(text.replace(' ', 'Choose'))

    def pick(self):
        pass

    def pickcb(self):
        pass

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

class App(SplitFluentWindow):
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
        self.resize(900, 700)
        self.setWindowIcon(QIcon('assets/NamePicker.png'))
        self.setWindowTitle('NamePicker')


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = App()
    w.show()
    app.exec()