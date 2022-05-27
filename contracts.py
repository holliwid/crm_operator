#!/usr/bin/python3
# -*- coding: utf-8 -*-
from datetime import datetime
import main


import sys
import psycopg2
from PyQt5.QtWidgets import QTableWidget, QApplication, QMainWindow, QTableWidget
from PyQt5.QtWidgets import QTableWidgetItem, QWidget, QPushButton, QLineEdit
from PyQt5 import QtGui
from PyQt5.QtCore import pyqtSlot


class Contracts(QWidget):

    def __init__(self):
        super().__init__()
        self.con()
        self.w = None
        # подключить базу данных
        self.con()
        # параметры окна
        self.setGeometry(100, 100, 1000, 800)
        self.setWindowTitle('Рейсы')
        self.tb = Tb(self)
        # кнопка "обновить"
        self.btn = QPushButton('Обновить', self)
        self.btn.resize(150, 40)
        self.btn.move(300, 10)
        self.btn.clicked.connect(self.upd)
        # здесь идентификатор
        self.contracts_id = QLineEdit(self)
        self.contracts_id.setPlaceholderText('Contracts id')
        self.contracts_id.resize(150, 40)
        self.contracts_id.move(300, 60)
        # здесь тип машины
        self.client_id = QLineEdit(self)
        self.client_id.setPlaceholderText('Client id')
        self.client_id.resize(150, 40)
        self.client_id.move(300, 110)
        # здесь изображение
        self.rate_id = QLineEdit(self)
        self.rate_id.setPlaceholderText('Rate id')
        self.rate_id.resize(150, 40)
        self.rate_id.move(300, 160)
        # здесь номер машины и водителя
        self.cars_drivers = QLineEdit(self)

        self.cars_drivers.setPlaceholderText('Сars drivers')
        self.cars_drivers.resize(150, 40)
        self.cars_drivers.move(300, 210)
        #
        self.dayFrom = QLineEdit(self)
        self.dayFrom.setPlaceholderText('Day From')
        self.dayFrom.resize(150, 40)
        self.dayFrom.move(300, 260)
        #
        self.dayTo = QLineEdit(self)
        self.dayTo.setPlaceholderText('Day To')
        self.dayTo.resize(150, 40)
        self.dayTo.move(300, 310)
        #
        self.loading_add = QLineEdit(self)
        self.loading_add.setPlaceholderText('Loading address')
        self.loading_add.resize(150, 40)
        self.loading_add.move(300, 360)
        #
        self.unloading_add = QLineEdit(self)
        self.unloading_add.setPlaceholderText('Unloading address')
        self.unloading_add.resize(150, 40)
        self.unloading_add.move(300, 410)
        #
        self.cargo_weights = QLineEdit(self)
        self.cargo_weights.setPlaceholderText('Cargo weights')
        self.cargo_weights.resize(150, 40)
        self.cargo_weights.move(300, 460)
        #
        self.distance = QLineEdit(self)
        self.distance.setPlaceholderText('Distance')
        self.distance.resize(150, 40)
        self.distance.move(300, 510)
        #Стоимость
        self.contracts_cost = QLineEdit(self)
        self.contracts_cost.setPlaceholderText('Стоимость')
        self.contracts_cost.resize(150, 40)
        self.contracts_cost.move(300, 560)
        #Рассчитать
        self.btn = QPushButton('Рассчитать стоимость', self)
        self.btn.resize(150, 40)
        self.btn.move(300, 610)
        self.btn.clicked.connect(self.calculate_cost)
        # кнопка добавить запись
        self.btn = QPushButton('Добавить', self)
        self.btn.resize(150, 40)
        self.btn.move(300, 660)
        self.btn.clicked.connect(self.ins)
        # кнопка удалить запись
        self.btn = QPushButton('Удалить', self)
        self.btn.resize(150, 40)
        self.btn.move(300, 710)
        self.btn.clicked.connect(self.dels)

        self.btn = QPushButton(f'Меню', self)
        self.btn.setGeometry(30, self.height() - 100, 100, 50)
        self.btn.clicked.connect(self.to_menu)




    # соединение с базой данных


    # обновить таблицу и поля
    def upd(self):
        self.conn.commit()
        self.tb.updt()
        self.contracts_id.setText('')
        self.client_id.setText('')
        self.rate_id.setText('')
        self.cars_drivers.setText('')
        self.dayFrom.setText('')
        self.dayTo.setText('')
        self.loading_add.setText('')
        self.unloading_add.setText('')
        self.cargo_weights.setText('')
        self.distance.setText('')



    # добавить таблицу новую строку
    def ins(self):
        contracts_id, client_id, rate_id, cars_drivers, dayFrom, dayTo, loading_add, unloading_add, cargo_weights, distance = (self.contracts_id.text(), self.client_id.text(), self.rate_id.text(), self.cars_drivers.text(),
                              self.dayFrom.text(), self.dayTo.text(), self.loading_add.text(), self.unloading_add.text(),
                               self.cargo_weights.text(), self.distance.text())
        # print(datetime.strptime(dayFrom, '%d.%m.%y'))

        #TODO time
        try:
            self.cur.execute("insert into contracts (contracts_id, client_id, rate_id, cars_drivers_id, dayFrom, dayTo, loading_address, unloading_address, cargo_weight, distance) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", (int(contracts_id), int(client_id), int(rate_id), int(cars_drivers),
                                                                                                                         datetime.strptime('01/01/10', '%d/%m/%y'), datetime.strptime('02/02/20', '%d/%m/%y'),
                                                                                                                         loading_add, unloading_add, int(cargo_weights), int(distance)))
        except:
            print('error')
        self.upd()

    # удалить из таблицы строку
    def dels(self):
        try:
            contracts_id = int(self.contracts_id.text())  # идентификатор строки
        except:
            return
        self.cur.execute("delete from contracts where contracts_id=%s", (contracts_id,))
        self.conn.commit()
        self.upd()

    def calculate_cost(self):
        try:
            contractss_id = int(self.contracts_id.text())
        except:
            return

        self.cur.execute(f"select contracts.distance * cost_rates sums from  contracts left join rates ON contracts.rate_id = rates.rate_id  where contracts_id = {contractss_id}")

        self.contracts_cost.setText(str(self.cur.fetchall()[0][0]))
        print(self.cur.fetchall())


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

    @pyqtSlot()
    def on_click_drivers(self):
        print('drivers')

    @pyqtSlot()
    def on_click_raice(self):
        print('raice')



class Tb(QTableWidget):
    def __init__(self, wg):
        self.wg = wg  # запомнить окно, в котором эта таблица показывается
        super().__init__(wg)
        self.setGeometry(10, 10, 280, 500)
        self.setColumnCount(10)
        self.verticalHeader().hide();
        self.updt() # обновить таблицу
        self.setEditTriggers(QTableWidget.NoEditTriggers) # запретить изменять поля
        self.cellClicked.connect(self.cellClick)  # установить обработчик щелча мыши в таблице

# обновление таблицы
    def updt(self):
        self.clear()
        self.setRowCount(0);
        self.setHorizontalHeaderLabels(['contracts_id', 'client_id', 'rate_id', 'cars_drivers', 'dayfrom', 'dayto', 'loading_address', 'unloading_address', 'cargo_weight', 'distance']) # заголовки столцов
        self.wg.cur.execute("select * from contracts")
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
        self.wg.contracts_id.setText(self.item(row, 0).text())
        self.wg.client_id.setText(self.item(row, 1).text().strip())
        self.wg.rate_id.setText(self.item(row, 2).text().strip())
        self.wg.cars_drivers.setText(self.item(row, 3).text().strip())
        self.wg.dayFrom.setText(self.item(row, 4).text().strip())
        self.wg.dayTo.setText(self.item(row, 5).text().strip())
        self.wg.loading_add.setText(self.item(row, 6).text().strip())
        self.wg.unloading_add.setText(self.item(row, 7).text().strip())
        self.wg.cargo_weights.setText(self.item(row, 8).text().strip())
        self.wg.distance.setText(self.item(row, 9).text().strip())