#!/usr/bin/python3
# -*- coding: utf-8 -*-
import cars, contracts, drivers, clients, garage, free_drivers

import sys
import psycopg2
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class Menu(QWidget):

    def __init__(self):
        super().__init__()
        self.w = None

        self.initUI()


    def initUI(self):
        QToolTip.setFont(QFont('SansSerif', 10))

        self.resize(1000, 800)
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


        btn = QPushButton(f'Машины', self)
        btn.setGeometry(int(self.width()/2) - 100, 50, 200, 100)
        btn.clicked.connect(self.on_click_cars)

        btn = QPushButton(f'Водители', self)
        btn.setGeometry(int(self.width() / 2) - 100, 200, 200, 100)
        btn.clicked.connect(self.on_click_drivers)

        btn = QPushButton(f'Рейсы', self)
        btn.setGeometry(int(self.width() / 2) - 100, 350, 200, 100)
        btn.clicked.connect(self.on_click_raice)

        btn = QPushButton(f'Клиенты', self)
        btn.setGeometry(int(self.width() / 2) - 100, 500, 200, 100)
        btn.clicked.connect(self.on_click_clients)

        btn = QPushButton(f'Гараж', self)
        btn.setGeometry(int(self.width() / 2) - 100, 650, 200, 100)
        btn.clicked.connect(self.on_click_garage)

        btn = QPushButton(f'Свободные водители', self)
        btn.setGeometry(int(self.width() / 2) + 150, 650, 200, 100)
        btn.clicked.connect(self.on_click_free_drivers)

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
            self.w = contracts.Contracts()
            self.w.show()

        else:
            self.w.close()  # Close window.
            self.w = None  # Discard reference.

    @pyqtSlot()
    def on_click_clients(self):
        self.window().close()
        if self.w is None:
            self.w = clients.Clients()
            self.w.show()

        else:
            self.w.close()  # Close window.
            self.w = None  # Discard reference.

    @pyqtSlot()
    def on_click_garage(self):
        self.window().close()
        if self.w is None:
            self.w = garage.Garage()
            self.w.show()

        else:
            self.w.close()  # Close window.
            self.w = None  # Discard reference.

    @pyqtSlot()
    def on_click_free_drivers(self):
        self.window().close()
        if self.w is None:
            self.w = free_drivers.Free_drivers()
            self.w.show()

        else:
            self.w.close()  # Close window.
            self.w = None  # Discard reference.


if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = Menu()
    sys.exit(app.exec_())