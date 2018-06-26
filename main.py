# -*- coding: utf-8 -*-
import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import clockform
import setting
import SetAlarm
import datetime
import subprocess
import Twipost


class mainwin(QDialog):
    timer = pyqtSignal()

    def __init__(self, parent=None):
        super(mainwin, self).__init__(parent)
        self.flag = 0
        self.al = datetime.time(6, 00)
        self.CFrom()
        self.ButSig('Pushed')
        self.TimeSig()

    def CFrom(self):
        self.ui = clockform.Ui_Form()
        self.ui.setupUi(self)

    def ButSig(self, state):
        self.ui.pushButton.clicked.connect(self.MakeWin)
        self.ui.pushButton_2.clicked.connect(app.quit)

    def TimeSig(self):
        self.timer = QTimer(self)
        self.timer.timeout.connect(lambda:
                                   self.ui.lineEdit.
                                   setText(datetime.
                                           datetime.now().
                                           strftime('%H:%M:%S')))
        self.timer.timeout.connect(lambda:
                                   self.Alarm('TIME!!'))
        self.timer.start(200)  # ミリ秒単位

    def Alarm(self, state):
        self.ti = datetime.datetime.now()
        if(self.ti.minute == self.al.minute):
            if(self.flag == 0):
                self.flag = 1
                if(self.ti.hour == self.al.hour):
                    Twipost.Twi_aupos(state)
        else:
            self.flag = 0

    def MakeWin(self):
        self.sub = SubWin()
        self.sub.show()


class SubWin(QDialog):
    def __init__(self, parent=None):
        super(SubWin, self).__init__(parent)
        self.ui = setting.Ui_Form()
        self.ui.setupUi(self)
        self.clbutton()
        self.Butsig()

    def clbutton(self):
        self.ui.pushButton_3.clicked.connect(self.close)

    def Butsig(self):
        self.ui.pushButton.clicked.connect(self.makeAlarm)

    def makeAlarm(self):
        self.Alarm = AlarmSetting()
        self.Alarm.show()


class AlarmSetting(QDialog):
    def __init__(self, parent=None):
        super(AlarmSetting, self).__init__(parent)
        self.ui = SetAlarm.Ui_Form()
        self.ui.setupUi(self)
        self.clbutton()

    def clbutton(self):
        self.ui.pushButton_5.clicked.connect(self.close)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = mainwin()
    window.show()
    sys.exit(app.exec_())
