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
        self.csv_to_json_btn.clicked.connect(self.csv_to_json_save)

    ## open file & return-> filename
    def fileopen(self):
        global filename
        filename=QtWidgets.QFileDialog.getOpenFileName(self, 'Select File',"","ALL files(*.csv;*.json);;CSV files(*.csv);;JSON files(*.json)")[0]

        ## Exception handling : Run only if you open the file
        if filename!='':
            self.input_name.setPlainText(filename)

            ## if : open csv file
            if filename.find('.csv')!=-1:
                ## add - if : csv_open
                self.csv_open()
                self.csv_input_screen.setVisible(True)
                self.json_output_screen.setVisible(True)

                self.json_input_screen.setVisible(False)
                self.csv_output_screen.setVisible(False)
                self.csv_to_json_btn.setVisible(True)
            
            ## if : open json file
            if filename.find('.json')!=-1:
                self.json_open()
                self.json_input_screen.setVisible(True)
                self.csv_output_screen.setVisible(True)

                self.csv_input_screen.setVisible(False)
                self.json_output_screen.setVisible(False)
                self.json_to_csv_btn.setVisible(True)

    ## csv_open
    def csv_open(self):
        global row_li
        row_li=[]
        ## load input_name(TextBrowser) value
        input_name_TextBrowser=self.input_name.toPlainText()

        global output_name_TextBrowser
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

    ##csv data -> output screen [json date]
    def csv_to_json_data_update(self):
        global json_data
        json_data=[]
        list_count=0
        for row_value in row_li[1:]:
            list_value_count=0
            info={}
            for list_column_value in row_li[0]:
                info[list_column_value]=row_value[list_value_count]
                list_value_count+=1
            json_data.append(info)
            list_count+=1
        json_output_data=json.dumps(json_data, indent=3)
        self.json_output_screen.setPlainText(json_output_data)
        
    def csv_update(self):
        col=self.csv_input_screen.currentColumn()
        row=self.csv_input_screen.currentRow()
        row_li[row+1][col]=self.csv_input_screen.item(row, col).text()
        self.csv_to_json_data_update()

    def csv_to_json_save(self):
        with open(output_name_TextBrowser,'w')as f:
            json.dump(json_data, f, ensure_ascii=False,indent=4)


    ## json_open
    def json_open(self):
        ## cellChange() disconnect
        try:
            self.json_input_screen.cellChanged.disconnect()
        except:
            pass 
        
        with open(filename, "r") as fp:
            json_dict=json.load(fp)
        json_input_data=json.dumps(json_dict, indent=3)

        ## load input_name(TextBrowser) value
        input_name_TextBrowser=self.input_name.toPlainText()
        ## set output_name(TextBrowser) value
        global output_name_TextBrowser
        output_name_TextBrowser=input_name_TextBrowser.replace(".json",".csv")
        self.output_name.setPlainText(output_name_TextBrowser)

        global json_li
        json_li=[]
        
        ## json_li[0] : column line 
        json_li.append(list(json_dict[0].keys()))
        for json_li_values in json_dict:
            json_li.append(list(json_li_values.values()))
       
        ## code edit...
        #list_len=len(json_li[0])
        self.json_input_screen.setColumnCount(4)
        widget_row=self.json_input_screen.rowCount()
        self.json_input_screen.insertRow(widget_row)
        self.json_input_screen.setItem(widget_row,0,QTableWidgetItem('{'))

        col_count=0
        column_count=0
        list_len=len(json_li[0])

        ## json file load -> json_input_screen
        for row_value in json_li[1:]:
            widget_row=self.json_input_screen.rowCount()
            self.json_input_screen.insertRow(widget_row)
            self.json_input_screen.setItem(widget_row,1,QTableWidgetItem('{'))

            for value in row_value:     
                widget_row=self.json_input_screen.rowCount()
                self.json_input_screen.insertRow(widget_row)
                self.json_input_screen.setItem(widget_row,2,QTableWidgetItem(json_li[0][column_count]))
                self.json_input_screen.setItem(widget_row,3,QTableWidgetItem(value))
                column_count+=1
                column_count%=list_len

            widget_row=self.json_input_screen.rowCount()
            self.json_input_screen.insertRow(widget_row)
            self.json_input_screen.setItem(widget_row,1,QTableWidgetItem('}'))
            
        widget_row=self.json_input_screen.rowCount()
        self.json_input_screen.insertRow(widget_row)
        self.json_input_screen.setItem(widget_row,0,QTableWidgetItem('}'))


        ## input data -> csv output screen
        list_len=len(json_li[0])
        self.csv_output_screen.setColumnCount(list_len)
        self.csv_output_screen.setHorizontalHeaderLabels(json_li[0])

        row_count=0
        for row_value in json_li[1:]: ##start json_li[1]~ -> json_li[0]: column line 
            widget_row=self.csv_output_screen.rowCount()
            self.csv_output_screen.insertRow(widget_row)
            col_count=0
            for value in row_value:
                self.csv_output_screen.setItem(row_count,col_count,QTableWidgetItem(value))
                col_count+=1
            row_count+=1
            
        self.json_input_screen.cellChanged.connect(self.json_update)
    
    def json_to_csv_data_update(self):
        print('json_to_csv_data')

    def json_update(self):
        column_len=len(json_li[0])
        col=self.json_input_screen.currentColumn()
        row=self.json_input_screen.currentRow()
        print((row-1)%(column_len+2))
        print(col,"-",row)
        #json_li[row+1][col]=self.json_input_screen.item(row, col).text()
        self.json_to_csv_data_update()
    
if __name__ == "__main__" :
    app = QApplication(sys.argv) 
    myWindow = WindowClass() 
    myWindow.show()
    app.exec_()