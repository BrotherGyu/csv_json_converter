from fileinput import filename
import sys
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import *
import csv

#module.py file import


#UI file connect : main.ui
form_class = uic.loadUiType("main.ui")[0]

class WindowClass(QMainWindow, form_class) :
    def __init__(self) :
        super().__init__()
        self.setupUi(self)
        self.initUI()

    def initUI(self):
        self.load_btn.clicked.connect(self.fileopen)
    
    ## open file & return-> filename
    def fileopen(self):
        global filename
        filename=QtWidgets.QFileDialog.getOpenFileName(self, 'Select File',"","CSV files(*.csv);;JSON files(*.json)")[0]
        self.input_name.setPlainText(filename)
        print(filename)
        self.csv_open()


    ## csv
    def csv_open(self):
        row_li=[]
        with open(filename, "r") as fp:
            for row in csv.reader(fp):    
                row_li.append(row)
        self.tableWidget_input.setColumnCount(len(row_li[0]))
        self.tableWidget_input.setHorizontalHeaderLabels(row_li[0])
        
        row_count=0
        for row_value in row_li[1:]: #start row_li[1]~ -> row_li[0]: column line 
            widget_row=self.tableWidget_input.rowCount()
            self.tableWidget_input.insertRow(widget_row)
            col_count=0
            for value in row_value:
                self.tableWidget_input.setItem(row_count,col_count,QTableWidgetItem(value))
                col_count+=1
            row_count+=1

        #self.tableWidget_input.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)

    ## json

if __name__ == "__main__" :
    app = QApplication(sys.argv) 
    myWindow = WindowClass() 
    myWindow.show()
    app.exec_()
    