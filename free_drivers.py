#!/usr/bin/python3
# -*- coding: utf-8 -*-

import cars, contracts, drivers, clients, garage, free_drivers, cars_drivers
import navbar


import psycopg2
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *



class Free_drivers(QMainWindow):



    def __init__(self):
        super().__init__()
        self.con()
        self.w = None
        navbar.createToolBars(self)
        # подключить базу данных
        self.con()
        # параметры окна
        self.resize(1000, 800)
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        self.setWindowTitle('Свободные водители')
        self.tb = Tb(self)





    # соединение с базой данных


    # обновить таблицу и поля
    def upd(self):
        self.conn.commit()
        self.tb.updt()
        self.img.setText('')
        self.num.setText('')


    def con(self):
        self.conn = psycopg2.connect(user="postgres",
                                     password="123",
                                     host="127.0.0.1",
                                     port="5432",
                                     database="postgres")
        self.cur = self.conn.cursor()

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
    def on_click_contracts(self):
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

    @pyqtSlot()
    def on_click_cars_drivers(self):
        self.window().close()
        if self.w is None:
            self.w = cars_drivers.Cars_Drivers()
            self.w.show()

        else:
            self.w.close()  # Close window.
            self.w = None  # Discard reference.



class Tb(QTableWidget):
    def __init__(self, wg):
        self.wg = wg  # запомнить окно, в котором эта таблица показывается
        super().__init__(wg)
        self.setGeometry(10, 40, 280, 500)
        self.setColumnCount(3)
        self.verticalHeader().hide();
        self.updt() # обновить таблицу
        self.setEditTriggers(QTableWidget.NoEditTriggers) # запретить изменять поля

# обновление таблицы
    def updt(self):
        self.clear()
        self.setRowCount(0);
        self.setHorizontalHeaderLabels(['ID','ФИО', 'Категория']) # заголовки столцов
        self.wg.cur.execute("select drivers.driver_id, drivers.name_driver, drivers.categorie_id from drivers \
	                         left join cars_drivers cd on cd.driver_id  = drivers.driver_id \
		                     left join contracts c on c.cars_drivers_id = cd.cars_drivers_id \
                             where (c.dayto < current_date  \
                             or c.dayfrom > current_date) \
                             or c.dayfrom is null")
        rows = self.wg.cur.fetchall()
        print(rows)
        i = 0
        for elem in rows:
            self.setRowCount(self.rowCount() + 1)
            j = 0
            for t in elem: # заполняем внутри строки
                self.setItem(i, j, QTableWidgetItem(str(t).strip()))
                j += 1
            i += 1
        self.resizeColumnsToContents()
