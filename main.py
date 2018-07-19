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

al = datetime.time(6, 00)
with open('AlarmTime.ti', 'r') as ti:
        tim = ti.read().split(':')
        al = datetime.time(int(tim[0]),
                           int(tim[1]))


class mainwin(QDialog):

    def __init__(self, parent=None):
        super(mainwin, self).__init__(parent)
        self.flag = 0
        self.timer = pyqtSignal()
        self.CFrom()
        self.ButSig()
        self.TimeSig()

    def CFrom(self):
        self.ui = clockform.Ui_Form()
        self.ui.setupUi(self)

    def ButSig(self):
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
                                   self.Alarm())
        self.timer.start(200)  # ミリ秒単位

    def Alarm(self):
        self.ti = datetime.datetime.now()
        if(self.ti.minute == al.minute):
            if(self.flag == 0):
                self.flag = 1
                if(self.ti.hour == al.hour):
                    subprocess.call('aplay Test.wav', shell=True)
                    subprocess.call('aplay Test.wav', shell=True)
        elif(self.ti.minute == (al.minute+5) % 60):
            if(self.flag == 0):
                self.flag = 1
                if(self.ti.hour == al.hour or
                   (self.ti.minute >= 55 and self.ti.hour-1 == al.hour)):
                    subprocess.call('aplay Test.wav', shell=True)
                    subprocess.call('aplay Test.wav', shell=True)
                    Twipost.Twi_aupos('アラームから遅れてるっぽい')
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
        self.ButSig()
        self.SH = 0
        self.SM = 0

    def clbutton(self):
        self.ui.pushButton_5.clicked.connect(self.Savetime)
        self.ui.pushButton_5.clicked.connect(self.close)

    def ButSig(self):
        self.ui.pushButton.clicked.connect(self.Hinc)
        self.ui.pushButton_2.clicked.connect(self.Hdec)
        self.ui.pushButton_3.clicked.connect(self.Minc)
        self.ui.pushButton_4.clicked.connect(self.Mdec)

    def Hinc(self):
        self.SH = (self.SH+1) % 24
        self.ui.label.setText(str(self.SH))

    def Hdec(self):
        self.SH = (self.SH+23) % 24
        self.ui.label.setText(str(self.SH))

    def Minc(self):
        self.SM = (self.SM+1) % 60
        self.ui.label_2.setText(str(self.SM))

    def Mdec(self):
        self.SM = (self.SM+59) % 60
        self.ui.label_2.setText(str(self.SM))

    def Savetime(self):
        global al
        al = datetime.time(self.SH, self.SM)
        with open('AlarmTime.ti', 'w') as f:
            self.state = str(self.SH)+':'+str(self.SM)
            f.write(self.state)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = mainwin()
    window.show()
    sys.exit(app.exec_())
