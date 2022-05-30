#!/usr/bin/python3
# -*- coding: utf-8 -*-

import cars, contracts, drivers, clients, garage, free_drivers, cars_drivers
import navbar


import psycopg2
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


class Garage(QMainWindow):



    def __init__(self):
        super().__init__()
        self.con()
        self.w = None
        navbar.createToolBars(self)
        # подключить базу данных
        self.con()
        # параметры окна
        self.resize(1200, 800)
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        self.setWindowTitle('Гараж')
        self.tb = Tb(self)


        self.id = QLineEdit(self)
        self.id.setPlaceholderText('ID машины')
        self.id.resize(150, 40)
        self.id.move(600, 560)


        self.under_repair = QCheckBox(self)
        self.under_repair.setText('На ремонте')
        self.under_repair.resize(150, 40)
        self.under_repair.move(600, 610)


        self.btn = QPushButton('Обновить', self)
        self.btn.resize(150, 40)
        self.btn.move(600, 650)
        self.btn.clicked.connect(self.change_under_repair)




    def change_under_repair(self):
        id = int(self.id.text())
        under_repair = self.under_repair.isChecked()

        self.cur.execute(f"update cars set under_repair={under_repair} where car_id={id}")
        self.upd()


    # обновить таблицу и поля
    def upd(self):
        self.conn.commit()
        self.tb.updt()
        self.under_repair.setChecked(False)
        self.id.setText('')


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
        self.setGeometry(10, 40, 1100, 500)
        self.setColumnCount(13)
        self.verticalHeader().hide();
        self.updt() # обновить таблицу
        self.setEditTriggers(QTableWidget.NoEditTriggers) # запретить изменять поля
        self.cellClicked.connect(self.cellClick)  # установить обработчик щелча мыши в таблице


# обновление таблицы
    def updt(self):
        self.clear()
        self.setRowCount(0);
        self.setHorizontalHeaderLabels(['ID','Тип', 'Изображение', 'Марка', 'Номер', 'Длина', 'Ширина', 'Высота', 'Дата произвобства', 'Грузоподъёмность', 'Количество мест', 'СТС', 'В ремонте']) # заголовки столцов
        self.wg.cur.execute("select cars.car_id, ct.type_name, cars.img, cars.mark, cars.car_number, cars.length, cars.width, cars.height, cars.year_of_release, cars.load_capacity, cars.number_of_seats, cars.ctc, cars.under_repair from cars \
	                         left join cars_drivers cd on cd.car_id = cars.car_id \
		                     left join contracts c on c.cars_drivers_id = cd.cars_drivers_id \
                             left join cars_type ct on cars.cars_type_id = ct.cars_type_id \
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


    def cellClick(self, row, col): # row - номер строки, col - номер столбца
        self.wg.id.setText(self.item(row, 0).text())
        self.wg.under_repair.setChecked(bool(self.item(row, 12).text() == 'True'))
