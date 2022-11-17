#!/usr/bin/python3
# -*- coding: utf-8 -*-

import navbar
import cars, contracts, drivers, clients, garage, free_drivers, cars_drivers



import sys
import psycopg2
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *




class Drivers(QMainWindow):



    def __init__(self):
        super(Drivers, self).__init__()
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
        self.setWindowTitle('Водители')


        self.tb = Tb(self)
        # кнопка "обновить"
        self.btn = QPushButton('Обновить', self)
        self.btn.resize(150, 40)
        self.btn.move(350, 40)
        self.btn.clicked.connect(self.upd)
        # здесь идентификатор
        self.idp = QLineEdit(self)
        self.idp.setPlaceholderText('Id')
        self.idp.resize(150, 40)
        self.idp.move(350, 60)
        self.idp.hide()
        # здесь тип название
        self.name = QLineEdit(self)
        self.name.setPlaceholderText('ФИО')
        self.name.resize(150, 40)
        self.name.move(350, 110)
        # здесь категории
        self.categories = QComboBox(self)
        self.categories.resize(150, 40)
        self.categories.move(350, 160)
        # стаж
        self.experience = QLineEdit(self)
        self.experience.setPlaceholderText('Стаж')
        self.experience.resize(150, 40)
        self.experience.move(350, 210)

        self.cur.execute("SELECT categorie_name FROM categories")
        data = self.cur.fetchall()
        for item_name in data:
            self.categories.addItem(item_name[0])


        # кнопка добавить запись
        self.btn = QPushButton('Добавить', self)
        self.btn.resize(150, 40)
        self.btn.move(350, 260)
        self.btn.clicked.connect(self.ins)
        # кнопка удалить запись
        self.btn = QPushButton('Удалить', self)
        self.btn.resize(150, 40)
        self.btn.move(350, 310)
        self.btn.clicked.connect(self.dels)


    # соединение с базой данных


    # обновить таблицу и поля
    def upd(self):
        self.conn.commit()
        self.tb.updt()
        self.idp.setText('')
        self.name.setText('')


    # добавить таблицу новую строку
    def ins(self):
        try:
            categories = self.categories.currentIndex() + 1
            idp, name = self.idp.text(), self.name.text()
            experience = int(self.experience.text())
            self.cur.execute("insert into drivers (name_driver, categorie_id, experience) values (%s,%s,%s)", (name, categories, experience))
        except:
            print('error')
        self.upd()

    # удалить из таблицы строку
    def dels(self):
        try:
            ids = int(self.idp.text())  # идентификатор строки

            self.cur.execute("delete from drivers where driver_id=%s", (ids,))
            self.conn.commit()
            self.upd()
        except:
            return


    def con(self):
        self.conn = psycopg2.connect(user="postgres",
                                     password="postgres",
                                     host="127.0.0.1",
                                     port="5432",
                                     database="crm_car")
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
        self.setGeometry(10, 40, 320, 500)
        self.setColumnCount(4)
        self.verticalHeader().hide();
        self.updt() # обновить таблицу
        self.setEditTriggers(QTableWidget.NoEditTriggers) # запретить изменять поля
        self.cellClicked.connect(self.cellClick)  # установить обработчик щелча мыши в таблице

# обновление таблицы
    def updt(self):
        self.clear()
        self.setRowCount(0);
        self.setHorizontalHeaderLabels(['ID', 'ФИО', 'Категория прав', 'Стаж']) # заголовки столцов
        self.wg.cur.execute("select d.driver_id, d.name_driver, c.categorie_name, d.experience  from drivers d \
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
        self.wg.experience.setText(self.item(row, 3).text().strip())


