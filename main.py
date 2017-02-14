#!/usr/bin/env python
# -*- coding:utf-8 -*-
import sys

# import PyQt4 QtCore and QtGui modules
import pandas as pd
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4 import uic
import functions as f
import numpy as np

form_class, base_class = uic.loadUiType('window.ui')


class MainWindow(QWidget, form_class):
    def __init__(self, *args):
        super(MainWindow, self).__init__(*args)

        self.setupUi(self)

    def gettable1values(self):
        cols = self.tableWidget.columnCount()
        rows = self.tableWidget.rowCount()
        data1 = pd.DataFrame(index=range(rows), columns=range(cols))
        for j in range(rows):
            for i in range(cols):
                if str(self.tableWidget.item(j,i).text())=='':
                    data1.iloc[j,i] = np.nan
                else:
                    data1.iloc[j,i] = float(str(self.tableWidget.item(j,i).text()))
        return data1

    def gettable2values(self):
        cols = self.tableWidget_2.columnCount()
        rows = self.tableWidget_2.rowCount()
        data2 = pd.DataFrame(index=range(rows), columns=range(cols))
        for j in range(rows):
            for i in range(cols):
                if str(self.tableWidget_2.item(j,i).text())=='':
                    data2.iloc[j,i] = np.nan
                else:
                    data2.iloc[j,i] = float(str(self.tableWidget_2.item(j,i).text()))
        return data2

    def gettable3values(self):
        cols = self.tableWidget_3.columnCount()
        rows = self.tableWidget_3.rowCount()
        data3 = pd.DataFrame(index=range(rows), columns=range(cols))
        for j in range(rows):
            for i in range(cols):
                if str(self.tableWidget_3.item(j,i).text())=='':
                    data3.iloc[j,i] = np.nan
                else:
                    data3.iloc[j,i] = float(str(self.tableWidget_3.item(j,i).text()))
        return data3

    def gettable4values(self):
        cols = self.tableWidget_4.columnCount()
        profit = []
        for i in range(cols):
            if str(self.tableWidget_4.item(0,i).text())=='':
                profit.append(np.nan)
            else:
                profit.append(float(str(self.tableWidget_4.item(0,i).text())))
        MatrixC = pd.Series(profit,index=range(cols))
        return MatrixC

    def gettable5values(self):
        rows = self.tableWidget_5.rowCount()
        timelimit = []
        for i in range(rows):
            if str(self.tableWidget_5.item(i,0).text())=='':
                timelimit.append(np.nan)
            else:
                timelimit.append(float(str(self.tableWidget_5.item(i,0).text())))
        MatrixB = pd.Series(timelimit,index=range(rows))
        return MatrixB

    def begincalculation(self):
        r = float(self.lineEdit_2.text())
        probability = self.doubleSpinBox.value()
        task1 = self.radioButton.isChecked()
        task2 = self.radioButton_2.isChecked()

        way1 = self.gettable1values()
        way2 = self.gettable2values()
        way3 = self.gettable3values()
        MatrixC = self.gettable4values()
        MatrixB = self.gettable5values()


        MatrixA = pd.concat([way1.iloc[:3], way2.iloc[:3], way3.iloc[:3]], axis=1,ignore_index=True)
        MatrixD = pd.concat([way1.iloc[3:], way2.iloc[3:], way3.iloc[3:]], axis=1,ignore_index=True)
        MatrixA=MatrixA.fillna(0)
        MatrixD=MatrixD.fillna(0)
        MatrixD.index = range(3)

        p=2

        vr = {1:0.68,
              0.95: 0.65788,
              0.90: 0.63188,
              0.85: 0.60468,
              0.80: 0.57628,
              0.75: 0.54674,
              0.70: 0.51607,
              0.65: 0.4843,
              0.60: 0.4515}

        ver = vr.get(round(probability, 2), 0.45149)
        try:
            if task1 == True:
                b=20
                x=f.func1(MatrixC, MatrixA, MatrixB, MatrixD, r, b, p, ver)
            elif task2 == True:
                b=10
                x=f.func2(MatrixC, MatrixA, MatrixB, MatrixD, r, b, p, ver)
            else:
                self.errormes(0)
                return
            sum = 0
            X=[]
            X.append(int(round(x.iloc[0]))+int(round(x.iloc[1])))
            X.append(int(round(x.iloc[2]))+int(round(x.iloc[3]))+int(round(x.iloc[4])))
            X.append(int(round(x.iloc[5]))+int(round(x.iloc[6])))
            for i in range(len(X)):
                sum += MatrixC.iloc[i] * X[i]
            resstr = "x1 = " + str(X[0]) + ";\n" +\
                " 1-м способом=" + str(int(round(x[0]))) + ";\n" +\
                " 2-м способом=" + str(int(round(x[1]))) + ";\n" +\
                "x2 = " + str(X[1]) + ";\n" +\
                " 1-м способом=" + str(int(round(x[2]))) + ";\n" +\
                " 2-м способом=" + str(int(round(x[3]))) + ";\n" +\
                " 3-м способом=" + str(int(round(x[4]))) + ";\n" +\
                "x3 = " + str(X[2]) + ";\n" +\
                " 1-м способом=" + str(int(round(x[5]))) + ";\n" +\
                " 2-м способом=" + str(int(round(x[6]))) + ";\n"

            sumstr = str(sum)
            self.outobjfunc(resstr, sumstr)

        except Exception:
                self.errormes(1)


    def errormes(self, i):
        mes={0:'Выберите задачу',
             1:'Error'}
        self.textBrowser.setText(mes.get(i,0))


    def outobjfunc(self, rs,sm):
        self.lineEdit.setText(sm)
        self.textBrowser.setText(rs)




#-----------------------------------------------------#
if __name__ == '__main__':
    # create application
    app = QApplication(sys.argv)
    app.setApplicationName('PDPC')

    # create widget
    w = MainWindow()
    w.setWindowTitle('PDPC')
    #w.setWindowIcon(QIcon('calculator.png'))

    w.tableWidget_5.setColumnWidth(0, 120)

    w.tableWidget.setColumnWidth(0, 140)
    w.tableWidget.setColumnWidth(1, 140)
    w.tableWidget.setColumnWidth(2, 140)
    w.tableWidget_2.setColumnWidth(0, 140)
    w.tableWidget_2.setColumnWidth(1, 140)
    w.tableWidget_2.setColumnWidth(2, 140)
    w.tableWidget_3.setColumnWidth(0, 140)
    w.tableWidget_3.setColumnWidth(1, 140)
    w.tableWidget_3.setColumnWidth(2, 140)

    w.show()


    # execute application
    sys.exit(app.exec_())
