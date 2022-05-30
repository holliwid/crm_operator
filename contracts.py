#!/usr/bin/python3
# -*- coding: utf-8 -*-
from datetime import datetime
import cars, contracts, drivers, clients, garage, free_drivers,cars_drivers
import navbar



import sys
import psycopg2
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


class Contracts(QMainWindow):

    def __init__(self):
        super().__init__()
        self.con()
        self.w = None
        navbar.createToolBars(self)
        # подключить базу данных
        self.con()
        # параметры окна
        self.resize(1250, 800)
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        self.setWindowTitle('Рейсы')


        self.tb = Tb(self)


        # кнопки
        self.btn = QPushButton('Все рейсы', self)
        self.btn.resize(200, 50)
        self.btn.move(1000, 40)
        self.btn.clicked.connect(self.upd)

        self.btn = QPushButton(f'Действующие контракты', self)
        self.btn.setGeometry(1000, 100, 200, 50)
        self.btn.clicked.connect(self.tb.updt_current)

        # кнопка добавить запись
        self.btn = QPushButton('Добавить', self)
        self.btn.resize(200, 50)
        self.btn.move(1000, 440)
        self.btn.clicked.connect(self.ins)
        # кнопка удалить запись
        self.btn = QPushButton('Удалить', self)
        self.btn.resize(200, 50)
        self.btn.move(1000, 500)
        self.btn.clicked.connect(self.dels)

        self.btn = QPushButton(f'Распечатать контракт', self)
        self.btn.setGeometry(1000, 180, 200, 50)
        self.btn.clicked.connect(self.save_contract)

        # здесь идентификатор
        self.contracts_id = QLineEdit(self)
        self.contracts_id.setPlaceholderText('ID контракта')
        self.contracts_id.resize(150, 40)
        self.contracts_id.move(40, 600)
        self.contracts_id.hide()
        # здесь ид клиета
        self.client_id_label = QLabel(self)
        self.client_id_label.setText('ID клиента')
        self.client_id_label.setAlignment(Qt.AlignCenter)
        self.client_id_label.resize(150, 20)
        self.client_id_label.move(20, 550)

        self.client_id = QComboBox(self)
        self.client_id.resize(150, 40)
        self.client_id.move(20, 570)

        self.cur.execute("SELECT client_id FROM clients")
        data = self.cur.fetchall()
        for item_name in data:
            self.client_id.addItem(str(item_name[0]))

        self.client_id_name = QLineEdit(self)
        self.client_id_name.setPlaceholderText('ФИО клиента')
        self.client_id_name.resize(150, 40)
        self.client_id_name.move(180, 570)
        self.client_id_name.setReadOnly(True)

        # здесь тариф
        self.rate_id_label = QLabel(self)
        self.rate_id_label.setText('ID тарифа')
        self.rate_id_label.setAlignment(Qt.AlignCenter)
        self.rate_id_label.resize(150, 20)
        self.rate_id_label.move(20, 620)

        self.rate_id = QComboBox(self)
        self.rate_id.setPlaceholderText('ID тарифа')
        self.rate_id.resize(150, 40)
        self.rate_id.move(20, 650)
        self.rate_id.activated.connect(self.change_drivers_cars)

        self.cur.execute("SELECT rate_id FROM rates")
        data = self.cur.fetchall()
        for item_name in data:
            self.rate_id.addItem(str(item_name[0]))

        self.client_id_name = QLineEdit(self)
        self.client_id_name.setPlaceholderText('Навание тарифа')
        self.client_id_name.resize(150, 40)
        self.client_id_name.move(180, 650)
        self.client_id_name.setReadOnly(True)

        # здесь номер машины и водителя
        self.сars_drivers_id_label = QLabel(self)
        self.сars_drivers_id_label.setText('Водитель и машина')
        self.сars_drivers_id_label.setAlignment(Qt.AlignCenter)
        self.сars_drivers_id_label.resize(150, 20)
        self.сars_drivers_id_label.move(20, 710)

        self.cars_drivers = QComboBox(self)
        self.cars_drivers.setPlaceholderText('Сars drivers')
        self.cars_drivers.resize(150, 40)
        self.cars_drivers.move(20, 740)

        self.client_id_name = QLineEdit(self)
        self.client_id_name.setPlaceholderText('Водитель и машина')
        self.client_id_name.resize(150, 40)
        self.client_id_name.move(180, 740)
        self.client_id_name.setReadOnly(True)


        # Даты
        self.client_id_label = QLabel(self)
        self.client_id_label.setText('Даты')
        self.client_id_label.setAlignment(Qt.AlignCenter)
        self.client_id_label.resize(150, 20)
        self.client_id_label.move(370, 550)


        self.dayFrom = QLineEdit(self)
        self.dayFrom.setPlaceholderText('Дата начала')
        self.dayFrom.resize(150, 40)
        self.dayFrom.move(370, 570)
        #
        self.dayTo = QLineEdit(self)
        self.dayTo.setPlaceholderText('Дата конца')
        self.dayTo.resize(150, 40)
        self.dayTo.move(370, 620)


        #Ареса
        self.client_id_label = QLabel(self)
        self.client_id_label.setText('Адресы')
        self.client_id_label.setAlignment(Qt.AlignCenter)
        self.client_id_label.resize(150, 20)
        self.client_id_label.move(570, 550)


        self.loading_add = QLineEdit(self)
        self.loading_add.setPlaceholderText('Адрес загрузки')
        self.loading_add.resize(150, 40)
        self.loading_add.move(570, 570)
        #
        self.unloading_add = QLineEdit(self)
        self.unloading_add.setPlaceholderText('Адресс выгрузки')
        self.unloading_add.resize(150, 40)
        self.unloading_add.move(570, 620)



        #
        self.cargo_weights = QLineEdit(self)
        self.cargo_weights.setPlaceholderText('Вес груза')
        self.cargo_weights.resize(150, 40)
        self.cargo_weights.move(760, 570)
        #
        self.distance = QLineEdit(self)
        self.distance.setPlaceholderText('Дистанция')
        self.distance.resize(150, 40)
        self.distance.move(760, 620)


        #Стоимость
        self.contracts_cost = QLineEdit(self)
        self.contracts_cost.setPlaceholderText('Стоимость')
        self.contracts_cost.resize(170, 40)
        self.contracts_cost.move(650, 690)
        #Рассчитать
        self.btn = QPushButton('Рассчитать стоимость', self)
        self.btn.resize(170, 40)
        self.btn.move(650, 740)
        self.btn.clicked.connect(self.calculate_cost)

        # Время
        self.time = QLineEdit(self)
        self.time.setPlaceholderText('Время')
        self.time.resize(170, 40)
        self.time.move(830, 690)
        # Рассчитать
        self.btn = QPushButton('Рассчитать время', self)
        self.btn.resize(170, 40)
        self.btn.move(830, 740)
        self.btn.clicked.connect(self.calculate_time)

        self.show()










    def change_drivers_cars(self):
        self.cars_drivers.clear()
        rate_id = (self.rate_id.currentText())
        self.cur.execute(f"select cd.cars_drivers_id  from rates r \
	                     left join cars_type ct on ct.cars_type_id = r.cars_type_id \
		                 left join cars c on c.cars_type_id = ct.cars_type_id \
			             left join cars_drivers cd on cd.car_id = c.car_id \
				         left join contracts c2 on c2.cars_drivers_id = cd.cars_drivers_id \
                         where r.rate_id = {rate_id} \
                         and (c2.dayto < current_date or c2.dayfrom > current_date or c2.dayfrom is null)")
        data = self.cur.fetchall()
        for item_name in data:
            print(type(item_name[0]))
            if item_name[0] is not None:
                self.cars_drivers.addItem(str(item_name[0]))


    # обновить таблицу и поля
    def upd(self):
        self.conn.commit()
        self.tb.updt()
        self.contracts_id.setText('')
        self.dayFrom.setText('')
        self.dayTo.setText('')
        self.loading_add.setText('')
        self.unloading_add.setText('')
        self.cargo_weights.setText('')
        self.distance.setText('')



    # добавить таблицу новую строку
    def ins(self):
        contracts_id = self.contracts_id.text()
        client_id = self.client_id.currentText()
        rate_id = self.rate_id.currentText()
        cars_drivers = self.cars_drivers.currentText()
        dayFrom = self.dayFrom.text()
        dayTo = self.dayTo.text()
        loading_add = self.loading_add.text()
        unloading_add = self.unloading_add.text()
        cargo_weights = self.cargo_weights.text()
        distance = self.distance.text()
        # print(datetime.strptime(dayFrom, '%d.%m.%y'))


        # try:
        self.cur.execute("insert into contracts (client_id, rate_id, cars_drivers_id, dayFrom, dayTo, loading_address, unloading_address, cargo_weight, distance) values (%s,%s,%s,%s,%s,%s,%s,%s,%s)", (int(client_id), int(rate_id), int(cars_drivers),
                                                                                                                         datetime.strptime(dayFrom, '%Y-%m-%d'), datetime.strptime(dayTo, '%Y-%m-%d'),
                                                                                                                         loading_add, unloading_add, int(cargo_weights), int(distance)))
        # except:
        #     print('error')
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
            rate_id = self.rate_id.currentText()
            distance = int(self.distance.text())
        except:
            return

        self.cur.execute(f"select r.cost_rates * {distance} from rates r \
	                      where r.rate_id = {rate_id}")

        self.contracts_cost.setText(str(self.cur.fetchall()[0][0]))
        print(self.cur.fetchall())

    def calculate_time(self):
        try:
            distance = float(self.distance.text())
        except:
            return
        self.time.setText(str(int(distance / 1000) + 1))

    def con(self):
        self.conn = psycopg2.connect(user="postgres",
                                     password="123",
                                     host="127.0.0.1",
                                     port="5432",
                                     database="postgres")
        self.cur = self.conn.cursor()


    def save_contract(self):
        dlg = QFileDialog(self)
        dlg.setFileMode(QFileDialog.AnyFile)
        dlg.selectFile(".txt")
        dlg.setDefaultSuffix(".txt")
        dlg.setNameFilters(["Text files (*.txt)"])
        path = dlg.getSaveFileName(self, "Save file", ".txt", "Text files (*.txt)")
        if not path:
            return
        print(path)
        file = open(path[0], 'w')
        row = self.tb.currentRow()
        text = ""
        for x in range(1, 10):
            text += self.tb.horizontalHeaderItem(x).text() + ': ' + self.tb.item(row, x).text() + '\n'
        print(text)
        file.write(text)
        file.close()
        print("i print")


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
        self.setGeometry(10, 40, 975, 500)
        self.setColumnCount(10)
        self.verticalHeader().hide();
        self.updt() # обновить таблицу
        self.setEditTriggers(QTableWidget.NoEditTriggers) # запретить изменять поля
        self.cellClicked.connect(self.cellClick)  # установить обработчик щелча мыши в таблице

# обновление таблицы
    def updt(self):
        self.clear()
        self.setRowCount(0);
        self.setHorizontalHeaderLabels(['ID контракта', 'ID клиента', 'ID тарифа', 'cars_drivers', 'Дата начала', 'Дата конца', 'Адресс загрузки', 'Адресс выгрузки', 'Вес груза', 'Дистанция']) # заголовки столцов
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


    def updt_current(self):
        self.clear()
        self.setRowCount(0);
        self.setHorizontalHeaderLabels(['ID контракта', 'ID клиента', 'ID тарифа', 'cars_drivers', 'Дата начала', 'Дата конца', 'Адресс загрузки', 'Адресс выгрузки', 'Вес груза', 'Дистанция']) # заголовки столцов
        self.wg.cur.execute("select * from contracts where dayto > current_date")
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
        self.wg.client_id.setCurrentIndex(int(self.item(row, 1).text().strip())-1)
        self.wg.rate_id.setCurrentIndex(int(self.item(row, 2).text().strip())-1)
        self.wg.cars_drivers.setCurrentText(self.item(row, 3).text().strip())
        self.wg.dayFrom.setText(self.item(row, 4).text().strip())
        self.wg.dayTo.setText(self.item(row, 5).text().strip())
        self.wg.loading_add.setText(self.item(row, 6).text().strip())
        self.wg.unloading_add.setText(self.item(row, 7).text().strip())
        self.wg.cargo_weights.setText(self.item(row, 8).text().strip())
        self.wg.distance.setText(self.item(row, 9).text().strip())

if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = Contracts()
    sys.exit(app.exec_())