from distutils.log import info
from fileinput import filename
import sys
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import *
import csv
import json
#for collections import OrderedDict
## module.py file import


## UI file connect : main.ui
form_class = uic.loadUiType("main.ui")[0]

class WindowClass(QMainWindow, form_class) :
    def __init__(self) :
        super().__init__()
        self.setupUi(self)
        self.initUI()

        ## Hide btn
        self.csv_to_json_btn.setVisible(False)

        self.json_to_csv_btn.setVisible(False)
        

    def initUI(self):
        self.load_btn.clicked.connect(self.fileopen)
        

    ## open file & return-> filename
    def fileopen(self):
        global filename
        filename=QtWidgets.QFileDialog.getOpenFileName(self, 'Select File',"","CSV files(*.csv);;JSON files(*.json)")[0]
        
        ## Exception handling : Run only if you open the file
        if filename!='':
            self.input_name.setPlainText(filename)

            ## add - if : csv_open
            self.csv_open()
            ## hide csv_output_screen
            self.json_input_screen.setVisible(False)
            self.csv_output_screen.setVisible(False)
            self.csv_to_json_btn.setVisible(True)
            

    ## csv
    def csv_open(self):
        global row_li
        row_li=[]
        ## load input_name(TextBrowser) value
        input_name_TextBrowser=self.input_name.toPlainText()
        output_name_TextBrowser=input_name_TextBrowser.replace(".csv",".json")
        self.output_name.setPlainText(output_name_TextBrowser)

        ## cellChange() disconnect
        try:
            self.csv_input_screen.cellChanged.disconnect()
        except:
            pass    

        with open(filename, "r") as fp:
            for row in csv.reader(fp):    
                row_li.append(row)
        list_len=len(row_li[0])
        self.csv_input_screen.setColumnCount(list_len)
        self.csv_input_screen.setHorizontalHeaderLabels(row_li[0])
        
        row_count=0
        for row_value in row_li[1:]: #start row_li[1]~ -> row_li[0]: column line 
            widget_row=self.csv_input_screen.rowCount()
            self.csv_input_screen.insertRow(widget_row)
            col_count=0
            for value in row_value:
                self.csv_input_screen.setItem(row_count,col_count,QTableWidgetItem(value))
                col_count+=1
            row_count+=1
        ## output screen update
        self.csv_to_json_data_update()

        ## tablewidget cell change -> csv_update() execution
        self.csv_input_screen.cellChanged.connect(self.csv_update)

    ## csv data -> ouput screen [json date]
    def csv_to_json_data_update(self):
        json_data={}
        list_count=0
        for row_value in row_li[1:]:
            list_value_count=0
            info={}
            for list_column_value in row_li[0]:
                info[list_column_value]=row_value[list_value_count]
                list_value_count+=1
            json_data[list_count]=info
            list_count+=1
        json_output_data=json.dumps(json_data, indent=3)
        self.json_ouput_screen.setPlainText(json_output_data)

    def csv_update(self):
        col=self.csv_input_screen.currentColumn()
        row=self.csv_input_screen.currentRow()
        row_li[row+1][col]=self.csv_input_screen.item(row, col).text()
        self.csv_to_json_data_update()
        

    ## json

if __name__ == "__main__" :
    app = QApplication(sys.argv) 
    myWindow = WindowClass() 
    myWindow.show()
    app.exec_()
    