#!/usr/bin/python3
# -*- coding: utf-8 -*-

import navbar
import cars, contracts, drivers, clients, garage, free_drivers



import sys
import psycopg2
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


class Cars_Drivers(QMainWindow):



    def __init__(self):
        super(Cars_Drivers, self).__init__()
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
        self.setWindowTitle('Машины и Водители')


        self.tb = Tb(self)
        # кнопка "обновить"
        self.btn = QPushButton('Обновить', self)
        self.btn.resize(150, 40)
        self.btn.move(650, 40)
        self.btn.clicked.connect(self.upd)
        # здесь идентификатор
        self.idp = QLineEdit(self)
        self.idp.setPlaceholderText('Id')
        self.idp.resize(150, 40)
        self.idp.move(650, 110)
        # здесь категории
        self.drivers = QComboBox(self)
        self.drivers.resize(150, 40)
        self.drivers.move(650, 160)

        self.cur.execute("SELECT driver_id FROM drivers")
        data = self.cur.fetchall()
        for item_name in data:
            self.drivers.addItem(str(item_name[0]))

        self.cars = QComboBox(self)
        self.cars.resize(150, 40)
        self.cars.move(650, 210)

        self.cur.execute("SELECT car_id FROM cars")
        data = self.cur.fetchall()
        for item_name in data:
            self.cars.addItem(str(item_name[0]))


        # кнопка добавить запись
        self.btn = QPushButton('Добавить', self)
        self.btn.resize(150, 40)
        self.btn.move(650, 260)
        self.btn.clicked.connect(self.ins)
        # кнопка удалить запись
        self.btn = QPushButton('Удалить', self)
        self.btn.resize(150, 40)
        self.btn.move(650, 310)
        self.btn.clicked.connect(self.dels)


    # соединение с базой данных


    # обновить таблицу и поля
    def upd(self):
        self.conn.commit()
        self.tb.updt()
        self.idp.setText('')


    # добавить таблицу новую строку
    def ins(self):
        try:
            id = int(self.idp.text())
            car = int(self.cars.currentText())
            driver = int(self.drivers.currentText())
        except:
            pass
        try:
            self.cur.execute("insert into cars_drivers (cars_drivers_id, car_id, driver_id) values (%s,%s,%s)", (id, car, driver))
        except:
            print('error')
        self.upd()

    # удалить из таблицы строку
    def dels(self):
        try:
            ids = int(self.idp.text())  # идентификатор строки
        except:
            return
        self.cur.execute("delete from cars_drivers where cars_drivers_id=%s", (ids,))
        self.conn.commit()
        self.upd()


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
            self.w = Cars_Drivers()
            self.w.show()

        else:
            self.w.close()  # Close window.
            self.w = None  # Discard reference.



class Tb(QTableWidget):
    def __init__(self, wg):
        self.wg = wg  # запомнить окно, в котором эта таблица показывается
        super().__init__(wg)
        self.setGeometry(10, 40, 550, 500)
        self.setColumnCount(7)
        self.verticalHeader().hide();
        self.updt() # обновить таблицу
        self.setEditTriggers(QTableWidget.NoEditTriggers) # запретить изменять поля
        self.cellClicked.connect(self.cellClick)  # установить обработчик щелча мыши в таблице

# обновление таблицы
    def updt(self):
        self.clear()
        self.setRowCount(0);
        self.setHorizontalHeaderLabels(['ID', 'ID машины', 'Марка', 'ID водителя', 'ФИО', 'Категория прав', 'Стаж']) # заголовки столцов
        self.wg.cur.execute("select cd.cars_drivers_id, c.car_id, c.mark, d.driver_id, d.name_driver, d.categorie_id, d.experience  from cars_drivers cd\
                             left join cars c on c.car_id =cd.car_id \
 	                         left join drivers d on d.driver_id = cd.driver_id ")
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

# обработка щелчка мыши по таблице
    def cellClick(self, row, col): # row - номер строки, col - номер столбца
        self.wg.idp.setText(self.item(row, 0).text())
        self.wg.cars.setCurrentText(self.item(row, 1).text().strip())
        self.wg.drivers.setCurrentText(self.item(row, 3).text().strip())



