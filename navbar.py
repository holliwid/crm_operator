from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import cars, contracts, drivers, clients, garage, free_drivers



def createToolBars(self):
    toolbar = QToolBar("Меню")
    self.addToolBar(toolbar)
    button_action = QAction("Контракты", self)
    button_action.triggered.connect(self.on_click_contracts)
    toolbar.addAction(button_action)

    button_action = QAction("Гараж", self)
    button_action.triggered.connect(self.on_click_garage)
    toolbar.addAction(button_action)

    button_action = QAction("Свободные водители", self)
    button_action.triggered.connect(self.on_click_free_drivers)
    toolbar.addAction(button_action)

    button_action = QAction("Машины", self)
    button_action.triggered.connect(self.on_click_cars)
    toolbar.addAction(button_action)

    button_action = QAction("Водители", self)
    button_action.triggered.connect(self.on_click_drivers)
    toolbar.addAction(button_action)

    button_action = QAction("Клиенты", self)
    button_action.triggered.connect(self.on_click_clients)
    toolbar.addAction(button_action)

    button_action = QAction("Машины_Водители", self)
    button_action.triggered.connect(self.on_click_cars_drivers)
    toolbar.addAction(button_action)
