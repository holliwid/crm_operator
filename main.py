#!/usr/bin/python3
# -*- coding: utf-8 -*-
import cars, raice, drivers

import sys
from PyQt5.QtWidgets import (QWidget, QToolTip,
    QPushButton, QApplication)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QMainWindow, QLabel
from PyQt5.QtWidgets import QGridLayout, QWidget, QDesktopWidget
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget


class Menu(QWidget):

    def __init__(self):
        super().__init__()
        self.w = None

        self.initUI()


    def initUI(self):
        QToolTip.setFont(QFont('SansSerif', 10))

        self.setFixedSize(1000, 800)
        qtRectangle = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())


        btn = QPushButton(f'Машины', self)
        btn.setGeometry(int(self.width()/2) - 100, 50, 200, 100)
        btn.clicked.connect(self.on_click_cars)

        btn = QPushButton(f'Водители', self)
        btn.setGeometry(int(self.width() / 2) - 100, 200, 200, 100)
        btn.clicked.connect(self.on_click_drivers)

        btn = QPushButton(f'Рейсы', self)
        btn.setGeometry(int(self.width() / 2) - 100, 350, 200, 100)
        btn.clicked.connect(self.on_click_raice)


        self.setWindowTitle('Menu')
        self.show()

    @pyqtSlot()
    def on_click_cars(self):
        self.window().close()
        if self.w is None:
            self.w = cars.Cars()
            self.w.show()

        else:
            self.w.close()  # Close window.
            self.w = None  # Discard reference.


    @pyqtSlot()
    def on_click_drivers(self):
        self.window().close()
        if self.w is None:
            self.w = drivers.Drivers()
            self.w.show()

        else:
            self.w.close()  # Close window.
            self.w = None  # Discard reference.

    @pyqtSlot()
    def on_click_raice(self):
        self.window().close()
        if self.w is None:
            self.w = raice.Raice()
            self.w.show()

        else:
            self.w.close()  # Close window.
            self.w = None  # Discard reference.


if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = Menu()
    sys.exit(app.exec_())