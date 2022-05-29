#!/usr/bin/python3
# -*- coding: utf-8 -*-

import main


import psycopg2
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *



class Free_drivers(QWidget):



    def __init__(self):
        super().__init__()
        self.con()
        self.w = None
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


        self.btn = QPushButton(f'Меню', self)
        self.btn.setGeometry(30, self.height() - 100, 100, 50)
        self.btn.clicked.connect(self.to_menu)




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
    def to_menu(self):
        self.window().close()
        if self.w is None:
            self.w = main.Menu()
            self.w.show()

        else:
            self.w.close()  # Close window.
            self.w = None  # Discard reference.



class Tb(QTableWidget):
    def __init__(self, wg):
        self.wg = wg  # запомнить окно, в котором эта таблица показывается
        super().__init__(wg)
        self.setGeometry(10, 10, 280, 500)
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
                             where c.dayto < current_date  \
                             or c.dayfrom > current_date \
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