#!/usr/bin/python3
# -*- coding: utf-8 -*-

import main


import sys
from PyQt5.QtWidgets import (QWidget, QToolTip,
    QPushButton, QApplication)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import pyqtSlot


class Drivers(QWidget):

    def __init__(self):
        super().__init__()
        self.w = None
        self.initUI()


    def initUI(self):
        self.setFixedSize(1000, 800)

        btn = QPushButton(f'Меню', self)
        btn.setGeometry(30, self.height()-100, 100, 50)
        btn.clicked.connect(self.to_menu)

        btn = QPushButton(f'Добавить', self)
        btn.setGeometry(self.width()-130, self.height() - 100, 100, 50)
        btn.clicked.connect(self.to_menu)


        self.setGeometry(500, 200, int(self.width()/2), int(self.height()/1.5))
        self.setWindowTitle('Drivers')
        self.show()

    @pyqtSlot()
    def to_menu(self):
        self.window().close()
        if self.w is None:
            self.w = main.Menu()
            self.w.show()

        else:
            self.w.close()  # Close window.
            self.w = None  # Discard reference.

    @pyqtSlot()
    def on_click_drivers(self):
        print('drivers')

    @pyqtSlot()
    def on_click_raice(self):
        print('raice')