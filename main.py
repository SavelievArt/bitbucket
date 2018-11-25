import sys
from PyQt5.QtWidgets import QTableWidgetItem
from crud_ui import *
from PyQt5 import QtCore, QtGui, QtWidgets
import mysql.connector
import datetime


class MyWin(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        self.conn = None
        QtWidgets.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.conn = self.getConnection()
        # connect to database and check connection
        self.updateTable()

        # buttons function
        self.ui.pushButtonUpdate.clicked.connect(self.UpdateFunction)
        self.ui.pushButtonClear.clicked.connect(self.ClearFunction)
        self.ui.pushButtonAdd.clicked.connect(self.AddFunction)
        self.ui.pushButtonDelete.clicked.connect(self.DeleteFunction)
        self.ui.tableWidget.cellClicked.connect(self.CellFunction)

    # function to fill lines if clicked on cells
    def CellFunction(self):
        index = self.ui.tableWidget.currentRow()
        self.ui.lineEdit.setText(self.ui.tableWidget.item(index, 1).text())
        self.ui.lineEdit_2.setText(self.ui.tableWidget.item(index, 3).text())
        self.ui.lineEdit_3.setText(self.ui.tableWidget.item(index, 4).text())
        self.ui.plainTextEdit.setPlainText(self.ui.tableWidget.item(index, 2).text())
        self.ui.labelID.setText(str(self.ui.tableWidget.item(index, 0).text()))


    def UpdateFunction(self):
        cursor = self.conn.cursor()
        request = "UPDATE nodes SET name = " + str("\'" + self.ui.lineEdit.text() + "\'") + \
                    ", descipt = " + str("\'" + self.ui.plainTextEdit.toPlainText() + "\'") + \
                    ", price = " + str(self.ui.lineEdit_2.text()) + \
                    ", link = " + str("\'" + self.ui.lineEdit_3.text() + "\'") + \
                    " WHERE id = " + str(self.ui.labelID.text()) + ";"
        try:
            cursor.execute(request)
            cursor.fetchone()
        except:
            print("ERROR IN REQUEST")
        self.updateTable()

    def DeleteFunction(self):

        cursor = self.conn.cursor()
        index = self.ui.tableWidget.currentRow()
        if self.ui.tableWidget.item(index, 0) is not None:
            request = "DELETE FROM nodes WHERE id = " + str(self.ui.tableWidget.item(index, 0).text()) + ";"
            try:
                cursor.execute(request)
                cursor.fetchone()
            except:
                print("ERROR IN REQUEST")
            self.ui.tableWidget.removeRow(index)
        self.updateTable()

    def AddFunction(self):

        if self.ui.lineEdit.text() is None and self.ui.plainTextEdit.toPlainText() is None \
                and self.ui.lineEdit_2.text() is None and self.ui.lineEdit_3.text() is None:
            return

        cursor = self.conn.cursor()
        request = "INSERT INTO nodes (name, descipt, price, link, date) " \
                  "VALUES (" + "\'" + self.ui.lineEdit.text() + "\'" + ", " + \
                  "\'" + self.ui.plainTextEdit.toPlainText() + "\'" + ", " + \
                  self.ui.lineEdit_2.text() + ", " + \
                  "\'" + self.ui.lineEdit_3.text() + "\'" + ", " + \
                  str(datetime.date.today().strftime("20%y%m%d")) + ");"
        try:
            cursor.execute(request)
            cursor.fetchone()
        except:
            print("ERROR IN REQUEST")
        self.updateTable()

    def getConnection(self):
        self.conn = None
        try:
            # create database and table if it not exists
            conn = mysql.connector.Connect(host='localhost', user='admin', password='1234')
            cursor = conn.cursor()
            cursor.execute("CREATE DATABASE IF NOT EXISTS crud;")
            cursor.fetchone()
            cursor.execute("USE crud;")
            cursor.fetchone()
            conn = mysql.connector.Connect(host='localhost', user='admin', password='1234', database = 'crud')
            cursor = conn.cursor()
            cursor.execute("CREATE TABLE IF NOT EXISTS `nodes` ( "
                           "`id` int NOT NULL AUTO_INCREMENT,"
                           "`name` varchar(255) NOT NULL,"
                           "`descipt` varchar(255) NOT NULL,"
                           "`price` int NOT NULL,"
                           "`link` varchar(255) NOT NULL,"
                           "`date` date NOT NULL,"
                           "PRIMARY KEY (`id`)) "
                           "DEFAULT CHARSET=utf8")
            cursor.fetchone()
            # trying to connect to database and check tables
            try:
                cursor.execute("show tables;")
                cursor.fetchall()
            except:
                print("no database")
        except:
            print("ERROR CONNECTION TO DATABASE")
        return conn

    def updateTable(self):

        """ 0 - ID
            1 - Name
            2 - Discription
            3 - Price
            4 - link
            5 - date
        """

        self.ui.tableWidget.clear()
        cursor = self.conn.cursor()

        cursor.execute("SHOW COLUMNS FROM nodes")

        res = cursor.fetchall()
        for col in range(len(res)):
            self.ui.tableWidget.setHorizontalHeaderItem(col, QTableWidgetItem(str(res[col][0])))

        cursor.execute("SELECT * FROM nodes")
        res = cursor.fetchall()

        # fill table
        for i in range(len(res)):
            if len(res) > self.ui.tableWidget.rowCount():  # check to skip empty rows
                self.ui.tableWidget.insertRow(self.ui.tableWidget.rowCount())
            for j in range(len(res[i])):
                self.ui.tableWidget.setItem(i, j, QTableWidgetItem(str(res[i][j])))

    def ClearFunction(self):
        self.ui.lineEdit.setText("")
        self.ui.lineEdit_2.setText("")
        self.ui.lineEdit_3.setText("")
        self.ui.plainTextEdit.setPlainText("")
        self.updateTable()

    def __del__(self):
        self.conn.commit()
        self.conn.close()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    myapp = MyWin()
    myapp.show()
    sys.exit(app.exec_())
