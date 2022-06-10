#!/usr/bin/python3
# -*- coding: utf-8 -*-

import cars, contracts, drivers, clients, garage, free_drivers, cars_drivers
import navbar

import psycopg2
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


class Clients(QMainWindow):



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
        self.setWindowTitle('Клиенты')
        self.tb = Tb(self)
        self.tb_contact = Tb_contacts(self)
        # кнопка "обновить"
        self.btn = QPushButton('Обновить', self)
        self.btn.resize(150, 40)
        self.btn.move(300, 40)
        self.btn.clicked.connect(self.upd)
        # здесь идентификатор
        self.idp = QLineEdit(self)
        self.idp.setPlaceholderText('Id')
        self.idp.resize(150, 40)
        self.idp.move(400, 50)
        self.idp.hide()
        # имя
        self.name = QLineEdit(self)
        self.name.setPlaceholderText('ФИО')
        self.name.resize(150, 40)
        self.name.move(300, 90)
        # кнопка добавить запись
        self.btn = QPushButton('Добавить', self)
        self.btn.resize(150, 40)
        self.btn.move(300, 260)
        self.btn.clicked.connect(self.ins)
        # кнопка удалить запись
        self.btn = QPushButton('Удалить', self)
        self.btn.resize(150, 40)
        self.btn.move(300, 310)
        self.btn.clicked.connect(self.dels)





        self.type_contact = QLineEdit(self)
        self.type_contact.setPlaceholderText('Тип контакта')
        self.type_contact.resize(150, 40)
        self.type_contact.move(800, 50)
        # здесь тип машины
        self.content_contact = QLineEdit(self)
        self.content_contact.setPlaceholderText('Контент')
        self.content_contact.resize(150, 40)
        self.content_contact.move(800, 110)

        self.btn = QPushButton('Добавить контакт', self)
        self.btn.resize(150, 40)
        self.btn.move(800, 260)
        self.btn.clicked.connect(self.ins_contact)
        # кнопка удалить запись
        self.btn = QPushButton('Удалить контакт', self)
        self.btn.resize(150, 40)
        self.btn.move(800, 310)
        self.btn.clicked.connect(self.dels_contact)





    # соединение с базой данных


    # обновить таблицу и поля
    def upd(self, id):

        self.conn.commit()
        self.tb.updt()
        self.tb_contact.updt(id)
        self.idp.setText('')
        self.name.setText('')

    def upd_contact(self, id):

        self.conn.commit()
        self.tb_contact.updt(id)



    # добавить таблицу новую строку
    def ins(self):
        name = self.name.text()
        try:
            self.cur.execute(f"insert into clients (name) values (%s)", (str(name),))
        except:
            return
        id = self.idp.text()
        self.upd(id)

    # удалить из таблицы строку
    def dels(self):
        try:
            ids = int(self.idp.text())  # идентификатор строки
        except:
            return
        try:
            self.cur.execute("delete from clients where client_id=%s", (ids,))
            self.conn.commit()
        except:
            return
        id = self.idp.text()
        self.upd(id)

    def ins_contact(self):
        idp = self.idp.text()
        type = self.type_contact.text()
        content = self.content_contact.text()
        try:
            self.cur.execute(f"insert into clients_contacts (client_id, type, contact) values (%s,%s,%s)", (int(idp), type, content))
        except:
            return
        id = self.idp.text()
        self.upd_contact(id)

    def dels_contact(self):
        try:
            ids = int(self.idp.text())  # идентификатор строки
            type = self.type_contact.text()
            content = self.content_contact.text()
        except:
            return
        try:
            self.cur.execute(f"delete from clients_contacts where client_id={ids} and type like '{type}' and contact like '{content}'")
            self.conn.commit()
        except:
            return
        id = self.idp.text()
        self.upd_contact(id)


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
        self.setColumnCount(2)
        self.verticalHeader().hide();
        self.updt() # обновить таблицу
        self.setEditTriggers(QTableWidget.NoEditTriggers) # запретить изменять поля
        self.cellClicked.connect(self.cellClick)  # установить обработчик щелча мыши в таблице

# обновление таблицы
    def updt(self):
        self.clear()
        self.setRowCount(0);
        self.setHorizontalHeaderLabels(['ID','ФИО']) # заголовки столцов
        self.wg.cur.execute("select * from clients")
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
        self.wg.name.setText(self.item(row, 1).text().strip())
        self.wg.tb_contact.updt(self.item(row, 0).text())
        self.wg.upd_contact(self.item(row, 0).text())



class Tb_contacts(QTableWidget):
    def __init__(self, wg):
        self.wg = wg  # запомнить окно, в котором эта таблица показывается
        super().__init__(wg)
        self.setGeometry(500, 40, 280, 500)
        self.setColumnCount(3)
        self.verticalHeader().hide();
        self.updt('-1') # обновить таблицу
        self.setEditTriggers(QTableWidget.NoEditTriggers) # запретить изменять поля
        self.cellClicked.connect(self.cellClick)  # установить обработчик щелча мыши в таблице

# обновление таблицы
    def updt(self, client_id):
        try:
            self.clear()
            self.setRowCount(0);
            self.setHorizontalHeaderLabels(['ID клиента','Тип', "Контакт"]) # заголовки столцов
            self.wg.cur.execute(f"select * from clients_contacts where client_id = {int(client_id)}")
            rows = self.wg.cur.fetchall()

            i = 0
            for elem in rows:
                self.setRowCount(self.rowCount() + 1)
                j = 0
                for t in elem: # заполняем внутри строки
                    self.setItem(i, j, QTableWidgetItem(str(t).strip()))
                    j += 1
                i += 1
            self.resizeColumnsToContents()
        except:
            pass

    def cellClick(self, row, col): # row - номер строки, col - номер столбца
        self.wg.type_contact.setText(self.item(row, 1).text())
        self.wg.content_contact.setText(self.item(row, 2).text().strip())
        pass