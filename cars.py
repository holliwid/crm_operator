#!/usr/bin/python3
# -*- coding: utf-8 -*-

import main


import sys
import psycopg2
from PyQt5.QtWidgets import QTableWidget, QApplication, QMainWindow, QTableWidget
from PyQt5.QtWidgets import QTableWidgetItem, QWidget, QPushButton, QLineEdit
from PyQt5 import QtGui
from PyQt5.QtCore import pyqtSlot


class Cars(QWidget):



    def __init__(self):
        super().__init__()
        self.con()
        self.w = None
        # self.initUI()
        # подключить базу данных
        self.con()
        # параметры окна
        self.setGeometry(100, 100, 500, 600)
        self.setWindowTitle('Журнал оценок')
        self.tb = Tb(self)
        # кнопка "обновить"
        self.btn = QPushButton('Обновить', self)
        self.btn.resize(150, 40)
        self.btn.move(300, 10)
        self.btn.clicked.connect(self.upd)
        # здесь идентификатор
        self.idp = QLineEdit(self)
        self.idp.resize(150, 40)
        self.idp.move(300, 60)
        self.idp.setReadOnly(True)
        # здесь фио
        self.fio = QLineEdit(self)
        self.fio.resize(150, 40)
        self.fio.move(300, 110)
        # здесь оценка
        self.oce = QLineEdit(self)
        self.oce.resize(150, 40)
        self.oce.move(300, 160)
        # кнопка добавить запись
        self.btn = QPushButton('Добавить', self)
        self.btn.resize(150, 40)
        self.btn.move(300, 210)
        self.btn.clicked.connect(self.ins)
        # кнопка удалить запись
        self.btn = QPushButton('Удалить', self)
        self.btn.resize(150, 40)
        self.btn.move(300, 260)
        self.btn.clicked.connect(self.dels)

    # соединение с базой данных
    def con(self):
        self.conn = psycopg2.connect(user="postgres",
                                     password="123",
                                     database="postgres")
        self.cur = self.conn.cursor()

    # обновить таблицу и поля
    def upd(self):
        self.conn.commit()
        self.tb.updt()
        self.idp.setText('')
        self.fio.setText('')
        self.oce.setText('')

    # добавить таблицу новую строку
    def ins(self):
        fio, oce = self.fio.text(), self.oce.text()
        try:
            self.cur.execute("insert into student (name, ocenka) values (%s,%s)", (fio, oce))
        except:
            pass
        self.upd()

    # удалить из таблицы строку
    def dels(self):
        try:
            ids = int(self.idp.text())  # идентификатор строки
        except:
            return
        self.cur.execute("delete from student where id=%s", (ids,))


    def initUI(self):
        self.setFixedSize(1000, 800)

        btn = QPushButton(f'Меню', self)
        btn.setGeometry(30, self.height()-100, 100, 50)
        btn.clicked.connect(self.to_menu)

        btn = QPushButton(f'Добавить', self)
        btn.setGeometry(self.width() - 130, self.height() - 100, 100, 50)
        btn.clicked.connect(self.to_menu)


        self.setGeometry(500, 200, int(self.width()/2), int(self.height()/1.5))
        self.setWindowTitle('Cars')
        self.show()

    def con(self):
        self.conn = psycopg2.connect(user="postgres",
                                     password="123",
                                     host="192.168.0.67",
                                     port="5432",
                                     database="students")
        self.cur = self.conn.cursor()


    def updt(self):
        self.clear()
        self.setRowCount(0);
        self.setHorizontalHeaderLabels(['id', 'ФИО', 'Оценка'])  # заголовки столцов
        self.wg.cur.execute("select * from student order by name")
        rows = self.wg.cur.fetchall()
        i = 0
        for elem in rows:
            self.setRowCount(self.rowCount() + 1)
            j = 0
            for t in elem:  # заполняем внутри строки
                self.setItem(i, j, QTableWidgetItem(str(t).strip()))
                j += 1
            i += 1
        self.resizeColumnsToContents()


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
        self.setHorizontalHeaderLabels(['id', 'ФИО', 'Оценка']) # заголовки столцов
        self.wg.cur.execute("select * from student order by name")
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

# обработка щелчка мыши по таблице
    def cellClick(self, row, col): # row - номер строки, col - номер столбца
        self.wg.idp.setText(self.item(row, 0).text())
        self.wg.fio.setText(self.item(row, 1).text().strip())
        self.wg.oce.setText(self.item(row, 2).text().strip())