#!/usr/bin/python3
# -*- coding: utf-8 -*-

import cars, contracts, drivers, clients, garage, free_drivers,cars_drivers
import navbar
from datetime import datetime



import psycopg2
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


class Cars(QMainWindow):



    def __init__(self):
        super().__init__()
        self.con()
        self.w = None
        navbar.createToolBars(self)
        # подключить базу данных
        self.con()
        # параметры окна
        self.resize(1300, 800)
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


        self.setWindowTitle('Машины')
        self.tb = Tb(self)
        # кнопка "обновить"
        self.btn = QPushButton('Обновить', self)
        self.btn.resize(150, 40)
        self.btn.move(1130, 40)
        self.btn.clicked.connect(self.upd)

        # кнопка добавить запись
        self.btn = QPushButton('Добавить', self)
        self.btn.resize(150, 40)
        self.btn.move(1130, 90)
        self.btn.clicked.connect(self.ins)
        # кнопка удалить запись
        self.btn = QPushButton('Удалить', self)
        self.btn.resize(150, 40)
        self.btn.move(1130, 140)
        self.btn.clicked.connect(self.dels)



        # здесь идентификатор
        self.idp = QLineEdit(self)
        self.idp.setPlaceholderText('Id')
        self.idp.resize(150, 40)
        self.idp.move(1130, 90)
        self.idp.hide()
        # здесь тип машины
        self.type = QComboBox(self)
        self.type.resize(150, 40)
        self.type.move(40, 560)

        self.cur.execute("SELECT cars_type_id, type_name FROM cars_type")
        data = self.cur.fetchall()
        for item_name in data:
            self.type.addItem(item_name[1])

        # здесь номер машины
        self.num = QLineEdit(self)
        self.num.setPlaceholderText('Номер машины')
        self.num.resize(150, 40)
        self.num.move(40, 610)

        self.mark = QLineEdit(self)
        self.mark.setPlaceholderText('Марка')
        self.mark.resize(150, 40)
        self.mark.move(40, 660)

        # здесь изображение
        self.img = QLineEdit(self)
        self.img.setPlaceholderText('Путь к изображению')
        self.img.resize(150, 40)
        self.img.move(40, 710)

        self.length = QLineEdit(self)
        self.length.setPlaceholderText('Длина')
        self.length.resize(150, 40)
        self.length.move(230, 560)

        self.width = QLineEdit(self)
        self.width.setPlaceholderText('Ширина')
        self.width.resize(150, 40)
        self.width.move(230, 610)

        self.height = QLineEdit(self)
        self.height.setPlaceholderText('Высота')
        self.height.resize(150, 40)
        self.height.move(230, 660)

        # self.length = QLineEdit(self)
        # self.length.setPlaceholderText('Объём')
        # self.length.resize(150, 40)
        # self.length.move(230, 710)

        self.year_of_release = QLineEdit(self)
        self.year_of_release.setPlaceholderText('Дата выпуска')
        self.year_of_release.resize(150, 40)
        self.year_of_release.move(410, 560)

        self.load_capacity = QLineEdit(self)
        self.load_capacity.setPlaceholderText('Грузоподъёмность')
        self.load_capacity.resize(150, 40)
        self.load_capacity.move(410, 610)

        self.number_of_seats = QLineEdit(self)
        self.number_of_seats.setPlaceholderText('Количество мест')
        self.number_of_seats.resize(150, 40)
        self.number_of_seats.move(410, 660)

        self.mileage = QLineEdit(self)
        self.mileage.setPlaceholderText('Пробег')
        self.mileage.resize(150, 40)
        self.mileage.move(410, 710)

        self.ctc = QLineEdit(self)
        self.ctc.setPlaceholderText('СТС')
        self.ctc.resize(150, 40)
        self.ctc.move(580, 560)

        self.under_repair = QCheckBox(self)
        self.under_repair.setText('На ремонте')
        self.under_repair.resize(150, 40)
        self.under_repair.move(580, 610)



    # соединение с базой данных


    # обновить таблицу и поля
    def upd(self):
        self.conn.commit()
        self.tb.updt()
        self.idp.setText('')
        self.img.setText('')
        self.mark.setText('')
        self.num.setText('')
        self.length.setText('')
        self.width.setText('')
        self.height.setText('')
        self.year_of_release.setText('')
        self.load_capacity.setText('')
        self.number_of_seats.setText('')
        self.mileage.setText('')
        self.ctc.setText('')






    # добавить таблицу новую строку
    def ins(self):
        try:
            type_index = self.type.currentIndex() + 1
            img = self.img.text()
            mark = self.mark.text()
            car_number = self.num.text()
            length = float(self.length.text())
            width = float(self.width.text())
            height = float(self.height.text())
            year_of_release = datetime.strptime(self.year_of_release.text(), '%Y-%m-%d')
            load_capacity = float(self.load_capacity.text())
            number_of_seats = int(self.number_of_seats.text())
            ctc = self.ctc.text()
            under_repair = bool(self.under_repair.checkState())
            mileage = int(self.mileage.text())
            # print(type_index, img, mark, car_number, length, width, height, year_of_release, load_capacity, number_of_seats, ctc, under_repair, mileage)

            self.cur.execute("insert into cars (cars_type_id, img, mark, car_number, length, width, height, year_of_release, load_capacity, number_of_seats, ctc, under_repair, mileage) \
                          values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s, %s)", (type_index, img, mark, car_number, length, width, height, year_of_release, load_capacity, number_of_seats, ctc, under_repair, mileage))
        except:
            print('error')
        self.upd()

    # удалить из таблицы строку
    def dels(self):
        try:
            ids = int(self.idp.text())  # идентификатор строки
            self.cur.execute("delete from cars where car_id=%s", (ids,))
            self.conn.commit()
        except:
            return
        self.upd()


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
        self.setGeometry(10, 40, 1100, 500)
        self.setColumnCount(14)
        self.verticalHeader().hide();
        self.updt() # обновить таблицу
        self.setEditTriggers(QTableWidget.NoEditTriggers) # запретить изменять поля
        self.cellClicked.connect(self.cellClick)  # установить обработчик щелча мыши в таблице

# обновление таблицы
    def updt(self):
        self.clear()
        self.setRowCount(0);
        self.setHorizontalHeaderLabels(['ID','Тип', 'Изображение', 'Марка', 'Номер', 'Длина', 'Ширина', 'Высота', 'Дата произвобства', 'Грузоподъёмность', 'Количество мест', 'СТС', 'В ремонте', 'Пробег']) # заголовки столцов
        self.wg.cur.execute("select c.car_id, ct.type_name, c.img, c.mark, c.car_number, c.length, c.width, c.height, c.year_of_release, c.load_capacity, c.number_of_seats, c.ctc, c.under_repair, c.mileage  from cars c \
	                         left join cars_type ct on c.cars_type_id = ct.cars_type_id ")
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
        self.wg.type.setCurrentText(self.item(row, 1).text().strip())
        self.wg.img.setText(self.item(row, 2).text().strip())
        self.wg.mark.setText(self.item(row, 3).text())
        self.wg.num.setText(self.item(row, 4).text().strip())
        self.wg.length.setText(self.item(row, 5).text())
        self.wg.width.setText(self.item(row, 6).text())
        self.wg.height.setText(self.item(row, 7).text())
        self.wg.year_of_release.setText(self.item(row, 8).text())
        self.wg.load_capacity.setText(self.item(row, 9).text())
        self.wg.number_of_seats.setText(self.item(row, 10).text())
        self.wg.ctc.setText(self.item(row, 11).text())
        self.wg.under_repair.setChecked(bool(self.item(row, 12).text() == 'True'))