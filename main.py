# -*- coding: utf-8 -*-
import os
import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import clockform
import setting
import SetAlarm
import datetime
import subprocess
import Twipost
from pygame import mixer
import time
import threading

al = datetime.time(6, 00)
music = ''
with open('AlarmTime.ti', 'r') as ti:
    tim = ti.read().split(':')
    al = datetime.time(int(tim[0]),
                       int(tim[1]))
with open('musicpath.txt', 'r') as mu:
    music = mu.readline()


def musicPlay(musicpath):
    mixer.init()
    mixer.music.load(musicpath)
    mixer.music.play(-1)
    time.sleep(15)
    mixer.music.stop()
thread_1 = threading.Thread(target=lambda: musicPlay(music))


class MainWindow(QDialog):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.flag = 0
        self.timer = pyqtSignal()
        self.createForm()
        self.buttonSignal()
        self.timerSignal()

    def createForm(self):
        self.ui = clockform.Ui_Form()
        self.ui.setupUi(self)

    def buttonSignal(self):
        self.ui.pushButton.clicked.connect(self.makeWindow)
        self.ui.pushButton_2.clicked.connect(app.quit)

    def timerSignal(self):
        self.timer = QTimer(self)
        self.timer.timeout.connect(lambda: self.ui.lineEdit.setText(
                                   datetime.datetime.now()
                                   .strftime('%H:%M:%S')))
        self.timer.timeout.connect(lambda:
                                   self.alarm())
        self.timer.start(200)  # ミリ秒単位

    def alarm(self):
        self.ti = datetime.datetime.now()
        if(self.ti.minute == al.minute):
            if self.flag == 0:
                self.flag = 1
                if(self.ti.hour == al.hour):
                    thread_1.start()
        elif(self.ti.minute == (al.minute+5) % 60):
            if self.flag == 0:
                self.flag = 1
                if ((self.ti.minute <= 4 and self.ti.hour-1 == al.hour) or
                   (self.ti.minute >= 5 and self.ti.hour == al.hour)):
                    Twipost.Twi_aupos('アラームから遅れてるっぽい')
        else:
            self.flag = 0

    def makeWindow(self):
        self.sub = SubWindow()
        self.sub.show()


class SubWindow(QDialog):
    def __init__(self, parent=None):
        super(SubWindow, self).__init__(parent)
        self.ui = setting.Ui_Form()
        self.ui.setupUi(self)
        self.closeWindow()
        self.buttonSignal()

    def closeWindow(self):
        self.ui.pushButton_3.clicked.connect(self.close)

    def buttonSignal(self):
        self.ui.pushButton.clicked.connect(self.makeAlarm)
        self.ui.pushButton_2.clicked.connect(self.musicDialog)

    def makeAlarm(self):
        self.alarm = AlarmSetting()
        self.alarm.show()

    def musicDialog(self):
        self.music = SelectFile()


class AlarmSetting(QDialog):
    def __init__(self, parent=None):
        super(AlarmSetting, self).__init__(parent)
        self.ui = SetAlarm.Ui_Form()
        self.ui.setupUi(self)
        self.closeWindow()
        self.buttonSignal()
        self.SH = 0
        self.SM = 0

    def closeWindow(self):
        self.ui.pushButton_5.clicked.connect(self.saveTime)
        self.ui.pushButton_5.clicked.connect(self.close)

    def buttonSignal(self):
        self.ui.pushButton.clicked.connect(self.hourIncrement)
        self.ui.pushButton_2.clicked.connect(self.hourDecrement)
        self.ui.pushButton_3.clicked.connect(self.minuteIncrement)
        self.ui.pushButton_4.clicked.connect(self.minuteDecrement)

    def hourIncrement(self):
        self.SH = (self.SH+1) % 24
        self.ui.label.setText(str(self.SH))

    def hourDecrement(self):
        self.SH = (self.SH+23) % 24
        self.ui.label.setText(str(self.SH))

    def minuteIncrement(self):
        self.SM = (self.SM+1) % 60
        self.ui.label_2.setText(str(self.SM))

    def minuteDecrement(self):
        self.SM = (self.SM+59) % 60
        self.ui.label_2.setText(str(self.SM))

    def saveTime(self):
        global al
        al = datetime.time(self.SH, self.SM)
        with open('AlarmTime.ti', 'w') as f:
            self.state = str(self.SH)+':'+str(self.SM)
            f.write(self.state)


class SelectFile(QMainWindow):
    def __init__(self, parent=None):
        super(SelectFile, self).__init__(parent)
        self.initUI()

    def initUI(self):
        fname = QFileDialog.getOpenFileName(self, 'Select mp3', '/home/wister')
        if fname[0]:
            music = fname[0]


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
