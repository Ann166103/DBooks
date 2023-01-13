import sys
import sqlite3
from PyQt5 import QtCore
import wath_book, new_book, new_buy_books, dbooksqt
from PyQt5.QtWidgets import (QApplication, QMainWindow, QGridLayout, QTableWidgetItem, QMessageBox,
                             QInputDialog, QWidget, QLabel, QFormLayout, QLineEdit, QComboBox, QAbstractScrollArea)


class WatchWindow(QMainWindow, wath_book.Ui_MainWindow):  # Окно для просмотра информации о книге (почитанной)
    def __init__(self):
        super().__init__()
        self.setupUi(self)


    def watch(self, res):
        self.setWindowTitle(res[1])
        self.label_9.setText(str(res[1]))
        self.label_10.setText(str(res[2]))
        self.label_11.setText(str(res[3]))
        self.label_12.setText(str(res[4]))
        self.label_13.setText(str(res[5]))
        self.label_14.setText(str(res[6]))
        self.label_15.setText(str(res[7]))
        self.label_16.setText(str(res[8]) + ' / 10')
        self.label_19.setText(str(res[9]))
        self.label_20.setText(str(res[10]))


class EditWindow(QMainWindow, new_book.Ui_MainWindow):  # Окно для изменения данных прочитанной книги
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.edit)
        self.connection = sqlite3.connect("books.sqlite")

    def watch(self, res):
        self.id = res[0]
        self.label_9.setText('')
        self.setWindowTitle(res[1])
        self.lineEdit.setText(str(res[1]))
        self.lineEdit_2.setText(str(res[2]))
        query2 = f"SELECT title FROM genres"
        res2 = [i[0] for i in list(self.connection.cursor().execute(query2).fetchall())]
        self.comboBox.addItems(res2)
        self.comboBox.setCurrentIndex(res[3] - 1)
        query3 = f"SELECT title FROM types"
        res3 = [i[0] for i in list(self.connection.cursor().execute(query3).fetchall())]
        self.comboBox_2.addItems(res3)
        self.comboBox_2.setCurrentIndex(res[4] - 1)
        self.lineEdit_5.setText(str(res[5]))
        self.lineEdit_6.setText(str(res[6]))
        self.lineEdit_7.setText(str(res[7]))
        self.lineEdit_8.setText(str(res[8]))
        self.dateEdit.setDate(QtCore.QDate(*res[9]))
        self.dateEdit_2.setDate(QtCore.QDate(*res[10]))
        self.dateEdit.setCalendarPopup(True)
        self.dateEdit_2.setCalendarPopup(True)

    def edit(self):
        self.label_9.setText('')
        if (self.lineEdit.text() and self.lineEdit_2.text() and self.lineEdit_5.text()
                and self.lineEdit_6.text() and self.lineEdit_7.text() and self.lineEdit_8.text()):
            cur = self.connection.cursor()
            if (self.lineEdit_5.text().isdigit() and self.lineEdit_6.text().isdigit()
                    and self.lineEdit_7.text().isdigit() and self.lineEdit_8.text().isdigit()):
                if 0 <= int(self.lineEdit_8.text()) <= 10:
                    cur.execute(f'UPDATE books SET title = "{self.lineEdit.text()}",'
                                f' author = "{self.lineEdit_2.text()}",'
                                f' genre = "{self.comboBox.currentIndex() + 1}",'
                                f' type = "{self.comboBox_2.currentIndex() + 1}",'
                                f' page_count = "{int(self.lineEdit_5.text())}",'
                                f' price = "{int(self.lineEdit_6.text())}", time = "{int(self.lineEdit_7.text())}",'
                                f' rating = "{int(self.lineEdit_8.text())}",'
                                f' date1 = "{str(self.dateEdit.date().toString("yyyy-MM-dd"))}",'
                                f' date2 = "{str(self.dateEdit_2.date().toString("yyyy-MM-dd"))}" WHERE id = {self.id}')
                    self.connection.commit()
                    self.window().close()
                else:
                    self.label_9.setText('В строке рейтинг должно находится числo от 0 до 10')
            else:
                self.label_9.setText('В строках кол-во страниц, цена, время чтения и рейтинг должно находится число')
        else:
            self.label_9.setText('Пожалуйста, заполните все строчки')


class AddWindow(QMainWindow, new_book.Ui_MainWindow):  # Окно для добавления прочитанной книги
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.save)
        self.label_9.setText('')
        self.connection = sqlite3.connect("books.sqlite")
        query2 = f"SELECT title FROM genres"
        res2 = [i[0] for i in list(self.connection.cursor().execute(query2).fetchall())]
        self.comboBox.addItems(res2)
        query3 = f"SELECT title FROM types"
        res3 = [i[0] for i in list(self.connection.cursor().execute(query3).fetchall())]
        self.comboBox_2.addItems(res3)
        self.dateEdit.setCalendarPopup(True)
        self.dateEdit_2.setCalendarPopup(True)

    def save(self):
        self.label_9.setText('')
        if (self.lineEdit.text() and self.lineEdit_2.text() and self.lineEdit_5.text()
                and self.lineEdit_6.text() and self.lineEdit_7.text() and self.lineEdit_8.text()):
            cur = self.connection.cursor()
            if (self.lineEdit_5.text().isdigit() and self.lineEdit_6.text().isdigit()
                    and self.lineEdit_7.text().isdigit() and self.lineEdit_8.text().isdigit()):
                if 0 <= int(self.lineEdit_8.text()) <= 10:
                    cur.execute(
                        f'INSERT INTO books(title, author, genre, type, page_count, price, time, rating, date1, date2)'
                        f' VALUES("{self.lineEdit.text()}", "{self.lineEdit_2.text()}",'
                        f' "{self.comboBox.currentIndex() + 1}", "{self.comboBox_2.currentIndex() + 1}",'
                        f' "{int(self.lineEdit_5.text())}", "{int(self.lineEdit_6.text())}", '
                        f'"{int(self.lineEdit_7.text())}", "{int(self.lineEdit_8.text())}",'
                        f' "{str(self.dateEdit.date().toString("yyyy-MM-dd"))}",'
                        f' "{str(self.dateEdit_2.date().toString("yyyy-MM-dd"))}")')
                    self.connection.commit()
                    self.window().close()
                else:
                    self.label_9.setText('В строке рейтинг должно находится числo от 0 до 10')
            else:
                self.label_9.setText('В строках кол-во страниц, цена, время чтения и рейтинг должно находится число')
        else:
            self.label_9.setText('Пожалуйста, заполните все строчки')


class EditBuyWindow(QMainWindow, new_buy_books.Ui_MainWindow):  # Окно для изменения данных купленной книги
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.edit)
        self.label.setText('')
        self.connection = sqlite3.connect("books.sqlite")

    def watch(self, res):
        self.id = res[0]
        self.setWindowTitle(res[1])
        self.lineEdit_1.setText(str(res[1]))
        self.lineEdit_2.setText(str(res[2]))
        self.lineEdit_3.setText(str(res[3]))

    def edit(self):
        self.label.setText('')
        if self.lineEdit_1.text() and self.lineEdit_2.text() and self.lineEdit_3.text():
            cur = self.connection.cursor()
            if self.lineEdit_3.text().isdigit():
                cur.execute(f'UPDATE buybooks SET title = "{self.lineEdit_1.text()}",'
                            f' author = "{self.lineEdit_2.text()}",'
                            f' price = "{int(self.lineEdit_3.text())}" WHERE id = {self.id}')
                self.connection.commit()
                self.window().close()
            else:
                self.label.setText('В строкe цена должно находится число')
        else:
            self.label.setText('Пожалуйста, заполните все строчки')


class AddBuyWindow(QMainWindow, new_buy_books.Ui_MainWindow):  # Окно для добавления данных купленной книги
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.save)
        self.label.setText('')
        self.connection = sqlite3.connect("books.sqlite")

    def save(self):
        self.label.setText('')
        if self.lineEdit_1.text() and self.lineEdit_2.text() and self.lineEdit_3.text():
            cur = self.connection.cursor()
            if self.lineEdit_3.text().isdigit():
                cur.execute(f'INSERT INTO buybooks(title, author, price) VALUES("{self.lineEdit_1.text()}",'
                            f' "{self.lineEdit_2.text()}", "{int(self.lineEdit_3.text())}")')
                self.connection.commit()
                self.window().close()
            else:
                self.label.setText('В строкe цена должно находится число')
        else:
            self.label.setText('Пожалуйста, заполните все строчки')


class EditPlansWindow(QMainWindow, new_buy_books.Ui_MainWindow):  # Окно для изменения данных книги в планах
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.edit)
        self.label.setText('')
        self.connection = sqlite3.connect("books.sqlite")

    def watch(self, res):
        self.id = res[0]
        self.setWindowTitle(res[1])
        self.lineEdit_1.setText(str(res[1]))
        self.lineEdit_2.setText(str(res[2]))
        self.lineEdit_3.setParent(None)
        self.label_3.setParent(None)

    def edit(self):
        self.label.setText('')
        if self.lineEdit_1.text() and self.lineEdit_2.text():
            cur = self.connection.cursor()
            cur.execute(f'UPDATE plansbooks SET title = "{self.lineEdit_1.text()}",'
                        f' author = "{self.lineEdit_2.text()}" WHERE id = {self.id}')
            self.connection.commit()
            self.window().close()
        else:
            self.label.setText('Пожалуйста, заполните все строчки')


class AddPlansWindow(QMainWindow, new_buy_books.Ui_MainWindow):  # Окно для добавления данных книги в планах
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.save)
        self.label.setText('')
        self.connection = sqlite3.connect("books.sqlite")
        self.lineEdit_3.setParent(None)
        self.label_3.setParent(None)

    def save(self):
        self.label.setText('')
        if self.lineEdit_1.text() and self.lineEdit_2.text():
            cur = self.connection.cursor()
            cur.execute(f'INSERT INTO plansbooks(title, author) VALUES("{self.lineEdit_1.text()}",'
                        f' "{self.lineEdit_2.text()}")')
            self.connection.commit()
            self.window().close()
        else:
            self.label.setText('Пожалуйста, заполните все строчки')


class MyWidget(QMainWindow, dbooksqt.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.connection = sqlite3.connect("books.sqlite")
        self.select_data(self.tableWidget, 'books')
        self.select_data(self.tableWidget_2, 'buybooks')
        self.select_data(self.tableWidget_3, 'plansbooks')
        self.comboBox.currentIndexChanged.connect(self.static)
        self.static()

        self.pushButton_1.clicked.connect(self.watch_book)
        self.pushButton_2.clicked.connect(self.add_book)
        self.pushButton_3.clicked.connect(self.edit_book)
        self.pushButton_44.clicked.connect(lambda: self.delite(self.tableWidget, 'books'))

        self.pushButton_4.clicked.connect(self.add_buybook)
        self.pushButton_5.clicked.connect(self.edit_buybook)
        self.pushButton_6.clicked.connect(lambda: self.delite(self.tableWidget_2, 'buybooks'))

        self.pushButton_7.clicked.connect(self.add_plansbook)
        self.pushButton_8.clicked.connect(self.edit_plansbook)
        self.pushButton_9.clicked.connect(lambda: self.delite(self.tableWidget_3, 'plansbooks'))

        self.pushButton.clicked.connect(lambda: self.select_data(self.tableWidget, 'books'))
        self.pushButton_10.clicked.connect(lambda: self.select_data(self.tableWidget_2, 'buybooks'))
        self.pushButton_11.clicked.connect(lambda: self.select_data(self.tableWidget_3, 'plansbooks'))

        self.pushButton.clicked.connect(self.static)
        self.pushButton_10.clicked.connect(self.static)
        self.pushButton_11.clicked.connect(self.static)
        self.label.setText('')

    def select_data(self, tab, bd):
        tab.setColumnWidth(1, 175)
        query = f"SELECT * FROM {bd}"
        if bd == 'books':
            query = f"SELECT id, title, author, price, rating FROM {bd}"
        res = self.connection.cursor().execute(query).fetchall()
        tab.setRowCount(len(res))
        # Заполняем таблицу элементами
        for i, elem in enumerate(res):
            for j, val in enumerate(elem):
                if j == len(elem) - 1 and bd == 'books':
                    tab.setItem(i, j, QTableWidgetItem(str(val) + ' / 10'))
                else:
                    tab.setItem(i, j, QTableWidgetItem(str(val)))

    def static(self):  # реализация вкладки статистика в зависимости от периода
        self.label.setText('')
        if self.comboBox.currentIndex() == 0:
            s = ''
        elif self.comboBox.currentIndex() == 1:
            s = ' WHERE julianday()-julianday("date2") < 8'
        elif self.comboBox.currentIndex() == 2:
            s = ' WHERE julianday()-julianday("date2") < 31'
        elif self.comboBox.currentIndex() == 3:
            s = ' WHERE julianday()-julianday("date2") < 92'
        elif self.comboBox.currentIndex() == 4:
            s = ' WHERE julianday()-julianday("date2") < 185'
        else:
            s = ' WHERE julianday()-julianday("date2") < 365'
        query = f"SELECT id FROM books" + s
        res = self.connection.cursor().execute(query).fetchall()
        self.label_3.setText(str(len(res)))
        query = f"SELECT id FROM buybooks" + s
        res = self.connection.cursor().execute(query).fetchall()
        self.label_5.setText(str(len(res)))
        query = f"SELECT id FROM plansbooks" + s
        res = self.connection.cursor().execute(query).fetchall()
        self.label_7.setText(str(len(res)))
        query = f"SELECT genre FROM books" + s
        res = self.connection.cursor().execute(query).fetchall()
        res = sorted(list(map(lambda a: a[0], res)))
        if res:
            res = res[-1]
            query = f'SELECT title FROM genres WHERE id={res}'
            self.label_8.setText(self.connection.cursor().execute(query).fetchall()[0][0])
        else:
            self.label_8.setText('—')
        query = f'SELECT rating FROM books' + s
        res = self.connection.cursor().execute(query).fetchall()
        res = list(map(lambda a: a[0], res))
        if res:
            self.label_11.setText(str(sum(res) / len(res))[:4])
        else:
            self.label_11.setText('0')
        query = f'SELECT price FROM buybooks' + s
        res = self.connection.cursor().execute(query).fetchall()
        res = list(map(lambda a: a[0], res))
        self.label_13.setText(str(sum(res)))
        query = f'SELECT time FROM books' + s
        res = self.connection.cursor().execute(query).fetchall()
        res = list(map(lambda a: a[0], res))
        self.label_15.setText(str(sum(res)))

    def watch_book(self):
        if self.tableWidget.selectedItems():
            self.label.setText('')
            self.w = WatchWindow()
            self.w.show()
            # записываем данные таблицы в список
            rows = list(set([i.row() for i in self.tableWidget.selectedItems()]))
            ids = [self.tableWidget.item(i, 0).text() for i in rows]
            query = f"SELECT * FROM books WHERE id={ids[0]}"
            res = list(self.connection.cursor().execute(query).fetchall()[0])
            res[3] = self.connection.cursor().execute(f'''SELECT title FROM genres WHERE id={res[3]}''').fetchone()[0]
            res[4] = self.connection.cursor().execute(f'''SELECT title FROM types WHERE id={res[4]}''').fetchone()[0]
            self.w.watch(res)
        else:
            self.label.setText('Пожалуйста, выберите книгу')

    def edit_book(self):
        if self.tableWidget.selectedItems():
            self.label.setText('')
            self.w = EditWindow()
            self.w.show()

            rows = list(set([i.row() for i in self.tableWidget.selectedItems()]))
            ids = [self.tableWidget.item(i, 0).text() for i in rows]
            query = f"SELECT * FROM books WHERE id={ids[0]}"
            res = list(self.connection.cursor().execute(query).fetchall()[0])
            res[9] = map(int, res[9].split('-'))
            res[10] = map(int, res[10].split('-'))
            self.w.watch(res)
        else:
            self.label.setText('Пожалуйста, выберите книгу')

    def add_book(self):
        self.label.setText('')
        self.w = AddWindow()
        self.w.show()

    def delite(self, tab, bd):
        if tab.selectedItems():
            self.label.setText('')
            # Получаем список элементов без повторов и их id
            rows = list(set([i.row() for i in tab.selectedItems()]))
            ids = [tab.item(i, 0).text() for i in rows]
            # Спрашиваем у пользователя подтверждение на удаление элементов
            valid = QMessageBox.question(
                self, '', "Действительно удалить элемент(ы) " + ",".join(ids),
                QMessageBox.Yes, QMessageBox.No)
            # Если пользователь ответил утвердительно, удаляем элементы.
            # Не забываем зафиксировать изменения
            if valid == QMessageBox.Yes:
                cur = self.connection.cursor()
                cur.execute(f"DELETE FROM {bd} WHERE id IN (" + ", ".join(
                    '?' * len(ids)) + ")", ids)
                self.connection.commit()
        else:
            self.label.setText('Пожалуйста, выберите книгу')

    def edit_buybook(self):
        if self.tableWidget_2.selectedItems():
            self.label.setText('')
            self.w = EditBuyWindow()
            self.w.show()

            # Получаем список элементов без повторов и их id
            rows = list(set([i.row() for i in self.tableWidget_2.selectedItems()]))
            ids = [self.tableWidget_2.item(i, 0).text() for i in rows]
            query = f"SELECT * FROM buybooks WHERE id={ids[0]}"
            res = list(self.connection.cursor().execute(query).fetchall()[0])

            self.w.watch(res)
        else:
            self.label.setText('Пожалуйста, выберите книгу')

    def edit_plansbook(self):
        if self.tableWidget_3.selectedItems():
            self.label.setText('')
            self.w = EditPlansWindow()
            self.w.show()

            # Получаем список элементов без повторов и их id
            rows = list(set([i.row() for i in self.tableWidget_3.selectedItems()]))
            ids = [self.tableWidget_3.item(i, 0).text() for i in rows]
            query = f"SELECT * FROM plansbooks WHERE id={ids[0]}"
            res = list(self.connection.cursor().execute(query).fetchall()[0])

            self.w.watch(res)
        else:
            self.label.setText('Пожалуйста, выберите книгу')

    def add_buybook(self):
        self.label.setText('')
        self.w = AddBuyWindow()
        self.w.show()

    def add_plansbook(self):
        self.label.setText('')
        self.w = AddPlansWindow()
        self.w.show()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec_())
