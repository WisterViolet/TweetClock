# -*- coding: utf-8 -*-
import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from clockform import Ui_Form
import datetime
import subprocess
import Twipost


class Win(QDialog):
    timer = pyqtSignal()

    def __init__(self, parent=None):
        super(Win, self).__init__(parent)
        self.flag = 0
        self.al = datetime.time(19, 1)
        self.CFrom()
        self.ButSig('Pushed')
        self.TimeSig()

    def CFrom(self):
        self.ui = Ui_Form()
        self.ui.setupUi(self)

    def ButSig(self, state):
        self.ui.pushButton.clicked.connect(lambda:
                                           Twipost.Twi_aupos(state))
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
        self.timer.start(1000)  # ミリ秒単位

    def Alarm(self, state):
        self.ti = datetime.datetime.now()
        if(self.ti.minute == self.al.minute):
            if(self.flag == 0):
                self.flag = 1
                if(self.ti.hour == self.al.hour):
                    Twipost.Twi_aupos(state)
        else:
            self.flag = 0

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Win()
    window.show()
    sys.exit(app.exec_())
