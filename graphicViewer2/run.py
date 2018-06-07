#!/usr/bin/python3
# -*- coding: utf-8 -*-

import rlcompleter, readline
import sys
import numpy as np
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.Qt import *
from SceneView import *
from ChartScene import *
from ChartLine import *
from MainWindow import *
from Trading import *

readline.parse_and_bind('tab:complete')

app = QApplication(sys.argv)


def loadData(start=None, end=None):
    fd = open('history.txt')
    content = fd.read()
    fd.close()
    tmp = []
    for row in content.split():
        time, price = row.split(',')
        time = int(time)
        price = float(price)
        tmp.append((time, price))

    sorted(tmp)

    ret = []
    cnt = 0
    startTime = tmp[0][0];
    prevSecTime = 0
    for row in tmp:
        time = row[0] - startTime
        secTime = round(time / 1000)
        if secTime != prevSecTime:
            cnt += secTime - prevSecTime
        prevSecTime = secTime

        if start and cnt < start:
            continue;
        ret.append({'time': time, 'price': row[1]})
        if end and cnt > end:
            break

    return ret



def keyPress(key):
    global trading
    global historyData
    global pos


    print("key = %d" % key)
    if key >= 49 and key < 56:  # 1 - 7
        chart = trading.chartByNum(key - 49)
        if chart.isVisible():
             chart.hide()
        else:
            chart.show()

    integratorKeys = (81, 87, 69, 82, 84, 89, 85)  # q - u
    num = 7
    for k in integratorKeys:
        if k == key:
            chart = trading.chartByNum(num)
            if chart.isVisible():
                 chart.hide()
            else:
                chart.show()
        num += 1


    if key == 80:  # p
        if trading.chartPointsIsVisible():
            trading.chartDisablePoints()
        else:
            trading.chartEnablePoints()
        return

    if key == 32:  # Space
        for i in range(1):
            row = historyData[pos]
            print("push %d, %.2f" % (row['time'], row['price']))
            trading.push(row['time'], row['price'])
            pos += 1


startPoint = 0
endPoint = 0
if len(sys.argv) > 1:
    if len(sys.argv) >= 2:
        startPoint = int(sys.argv[1])

    if len(sys.argv) == 3:
        endPoint = int(sys.argv[2])

print("startPoint = %d, endPoint = %d" % (startPoint, endPoint));
historyData = loadData(startPoint, endPoint)

scene = ChartScene()
view = SceneView(scene)
mainWindow = MainWindow(view)
mainWindow.show()
mainWindow.setKeyPressAction(keyPress)

trading = Trading(scene)

pos = 0
for row in historyData:
    trading.push(row['time'], row['price'])
    pos += 1
    if pos > 1000:
        break


