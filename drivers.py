#!/usr/bin/python3
# -*- coding: utf-8 -*-

import main


import sys
import psycopg2
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


class Drivers(QWidget):



    def __init__(self):
        super().__init__()
        self.w = None
        # подключить базу данных
        self.con()
        # параметры окна
        self.resize(1000, 800)
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        self.setWindowTitle('Водители')


        self.tb = Tb(self)
        # кнопка "обновить"
        self.btn = QPushButton('Обновить', self)
        self.btn.resize(150, 40)
        self.btn.move(300, 10)
        self.btn.clicked.connect(self.upd)
        # здесь идентификатор
        self.idp = QLineEdit(self)
        self.idp.setPlaceholderText('Id')
        self.idp.resize(150, 40)
        self.idp.move(300, 60)
        self.idp.hide()
        # здесь тип название
        self.name = QLineEdit(self)
        self.name.setPlaceholderText('ФИО')
        self.name.resize(150, 40)
        self.name.move(300, 110)
        # здесь категории
        self.categories = QComboBox(self)
        self.categories.resize(150, 40)
        self.categories.move(300, 160)

        self.cur.execute("SELECT categorie_name FROM categories")
        data = self.cur.fetchall()
        for item_name in data:
            self.categories.addItem(item_name[0])


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

        self.btn = QPushButton(f'Меню', self)
        self.btn.setGeometry(30, self.height() - 100, 100, 50)
        self.btn.clicked.connect(self.to_menu)




    # соединение с базой данных


    # обновить таблицу и поля
    def upd(self):
        self.conn.commit()
        self.tb.updt()
        self.idp.setText('')
        self.name.setText('')


    # добавить таблицу новую строку
    def ins(self):
        categories = self.categories.currentIndex() + 1
        idp, name = self.idp.text(), self.name.text()
        try:
            self.cur.execute("insert into drivers (name_driver, categorie_id) values (%s,%s)", (name, categories))
        except:
            print('error')
        self.upd()

    # удалить из таблицы строку
    def dels(self):
        try:
            ids = int(self.idp.text())  # идентификатор строки
        except:
            return
        self.cur.execute("delete from drivers where driver_id=%s", (ids,))
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
        self.setColumnCount(3)
        self.verticalHeader().hide();
        self.updt() # обновить таблицу
        self.setEditTriggers(QTableWidget.NoEditTriggers) # запретить изменять поля
        self.cellClicked.connect(self.cellClick)  # установить обработчик щелча мыши в таблице

# обновление таблицы
    def updt(self):
        self.clear()
        self.setRowCount(0);
        self.setHorizontalHeaderLabels(['ID', 'ФИО', 'Категория прав']) # заголовки столцов
        self.wg.cur.execute("select d.driver_id, d.name_driver, c.categorie_name  from drivers d \
	                         left join categories c on c.categorie_id = d.categorie_id ")
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
        self.wg.categories.setCurrentText(self.item(row, 2).text().strip())
