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
        time, price, qty = row.split(',')
        time = int(time)
        price = float(price)
        tmp.append((time, price, float(qty)))

    sorted(tmp)

    ret = []
    cnt = 0
    startTime = tmp[0][0];
    prevSecTime = 0
    num = 0
    lastPrice = 0
    for row in tmp:
        time = row[0] - startTime
        secTime = round(time / 1000)
        if secTime != prevSecTime:
            cnt += secTime - prevSecTime
        prevSecTime = secTime

        if start and cnt < start:
            continue;
        price = row[1]
        if not lastPrice:
            lastPrice = price

        if abs(lastPrice - price) > 2:
            lastPrice = price
            ret.append({'num': num, 'time': time / 1000, 'price': price, 'qty': row[2]})
            num += 1
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
            print("push %d, %.2f, %.2f" % (row['time'], row['price'], row['normedQty']))
            trading.push(row['num'], row['time'], row['price'], row['normedQty'])
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


def setStatusCursorCoordinates(point):
    x = -1
    for row in historyData:
        if row['num'] == int(point.x()):
            x = row['time']
            break
    if x == -1:
        mainWindow.displayCoordinate(0, 0)
        return

    mainWindow.displayCoordinate(x, point.y())

scene.setChangeMousePosAction(setStatusCursorCoordinates)


minQty = 1000000000000
for row in historyData:
    if minQty > row['qty']:
        minQty = row['qty']

maxQty = 0
for row in historyData:
    if maxQty < row['qty']:
        maxQty = row['qty']

minPrice = 1000000000000
for row in historyData:
    if minPrice > row['price']:
        minPrice = row['price']

maxPrice = 0
for row in historyData:
    if maxPrice < row['price']:
        maxPrice = row['price']

print('minQty = %f, maxQty = %f, minPrice = %f, maxPrice = %f' % (minQty,
                                                                  maxQty,
                                                                  minPrice,
                                                                  maxPrice))

rangePrice = maxPrice - minPrice
rangeQty = maxQty - minQty
for row in historyData:
    row['normedQty'] = ((row['qty'] - minQty) * rangePrice / rangeQty) + minPrice

pos = 0
lastTime = 0
for row in historyData:
    if not lastTime:
        lastTime = row['time']
    if row['time'] > (lastTime + 60):
        print("loadTime = %.2f" % row['time'])
        lastTime = row['time']

    trading.push(row['num'], row['time'], row['price'], row['normedQty'])
    pos += 1
    # if pos > 10:
     #   break


