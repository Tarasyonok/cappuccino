import sys
import sqlite3

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QInputDialog, QWidget


class Coffee(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("main.ui", self)
        self.con = sqlite3.connect("coffee.sqlite")
        self.createBtn.clicked.connect(self.create_coffee)
        self.changeBtn.clicked.connect(self.change_coffee)

        self.show_info()

    def show_info(self):
        cur = self.con.cursor()
        result = cur.execute(f"""SELECT * FROM info""").fetchall()
        self.curr_id = len(result) - 1

        title = ["ID", "название сорта", "степень обжарки", "молотый/в зернах", "описание вкуса", "цена",
                 "объем упаковки"]
        self.tableWidget.setColumnCount(len(title))
        self.tableWidget.setHorizontalHeaderLabels(title)
        self.tableWidget.setRowCount(0)
        for i, row in enumerate(result):
            self.tableWidget.setRowCount(
                self.tableWidget.rowCount() + 1)
            for j, elem in enumerate(row):
                self.tableWidget.setItem(
                    i, j, QTableWidgetItem(str(elem)))

    def create_coffee(self):
        self.opp = 'create'
        self.AECF = QWidget()
        uic.loadUi("addEditCoffeeForm.ui", self.AECF)
        self.AECF.show()

        self.AECF.cancelBtn.clicked.connect(self.cancel)
        self.AECF.okBtn.clicked.connect(self.comfirm)
        self.curr_id += 1
        self.id = self.curr_id

    def change_coffee(self):
        self.opp = 'change'
        cur = self.con.cursor()
        result = cur.execute(f"""SELECT id FROM info""").fetchall()
        coffee_list = []
        for item in result:
            coffee_list.append(str(item[0]))

        n, ok_pressed = QInputDialog.getItem(self, "Выберете кофе", "Выберете id кофе для изменения", coffee_list, 0,
                                             False)

        if not ok_pressed:
            return
        self.id = n

        print(n)

        self.AECF = QWidget()
        uic.loadUi("addEditCoffeeForm.ui", self.AECF)
        self.AECF.show()

        self.AECF.cancelBtn.clicked.connect(self.cancel)
        self.AECF.okBtn.clicked.connect(self.comfirm)

        cur = self.con.cursor()
        result = cur.execute(f"""SELECT * FROM info WHERE id = ?""", (n)).fetchone()

        self.AECF.sortInput.setText(result[1])
        self.AECF.roastInput.setValue(result[2])
        self.AECF.BOGInput.setCurrentIndex(result[3])
        self.AECF.tasteInput.setText(result[4])
        self.AECF.priceInput.setValue(result[5])
        self.AECF.sizeInput.setValue(result[6])

    def cancel(self):
        self.AECF.hide()

    def comfirm(self):
        sort = self.AECF.sortInput.text()
        roast = self.AECF.roastInput.value()
        BOG = self.AECF.BOGInput.currentIndex()
        taste = self.AECF.tasteInput.text()
        price = self.AECF.priceInput.value()
        size = self.AECF.sizeInput.value()

        print(self.opp)

        # print(self.id, sort, roast, BOG, taste, price, size)

        # cur = self.con.cursor()

        print("I'm before!")
        if self.opp == 'create':
            print("I'm if!")
        else:
            print("I'm else!")
            result = cur.execute(f"""SELECT * FROM info WHERE id = {self.id}""").fetchone()
            print(result)
            cur.execute(f"""
            UPDATE info SET
            sort = '{sort}', roast = {roast}, beansOrGround = {BOG},
            taste = '{taste}', price = {price}, size = {size}
            WHERE id = {self.id}
            """)
            # con = sqlite3.connect("coffee.sqlite")
            # cur = con.cursor()
            # cur.execute(f"""
            # UPDATE info SET
            # sort='asd', roast=1, beansOrGround=1,
            # taste='asd', price=1, size=1
            # WHERE id = 0
            # """)
        con.commit()

        # self.show_info()


# con = sqlite3.connect("coffee.sqlite")
# cur = con.cursor()
# cur.execute(f"""
# UPDATE info SET
# sort='fgh', roast=3, beansOrGround=1,
# taste='fgh', price=40, size=1
# WHERE id = 0
# """)
# con.commit()
if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Coffee()
    w.show()
    sys.exit(app.exec())
