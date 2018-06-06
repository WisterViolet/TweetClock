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
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(lambda:
                                           Twipost.Twi_aupos('Pushed'))
        self.ui.pushButton_2.clicked.connect(app.quit)
        self.timer = QTimer(self)
        self.timer.timeout.connect(lambda:
                                   self.ui.lineEdit.
                                   setText(datetime.
                                           datetime.now().
                                           strftime('%H:%M:%S')))
        self
        self.timer.start(1000)  # ミリ秒単位


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Win()
    window.show()
    sys.exit(app.exec_())
