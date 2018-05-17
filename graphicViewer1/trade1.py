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




class LinearRegression():
    def __init__(self, points):
        x = np.array([item[0] for item in points])
        y = np.array([item[1] for item in points])
        A = np.vstack([x, np.ones(len(x))]).T
        self.a, self.b = np.linalg.lstsq(A, y)[0]

    def point(self, time):
        price = self.a * time + self.b
        return QPointF(time, price)



class Integrator():
    def __init__(self):
        self.data = []

    def push(self, val):
        self.data.append(val)

    def reset(self):
        self.data = []

    def value(self):
        summ = 0
        for val in self.data:
            summ += val
        return summ / len(self.data)

    def isEmpty(self):
        return not len(self.data)



def aggregateBySec(data, interval):
    resultData = []
    integrator = Integrator()
    startInterval = 0
    endInterval = 0
    for row in data:
        if not startInterval:
            startInterval = row['time']
            endInterval = startInterval + interval * 1000
        integrator.push(row['price'])

        if endInterval and row['time'] >= endInterval:
            resultData.append({'time': startInterval,
                               'price': integrator.value()})
            startInterval = 0
            endInterval = 0
            integrator.reset()

    if not integrator.isEmpty():
        resultData.append({'time': startInterval,
                           'price': integrator.value()})
        integrator.reset()

    return resultData


def addAggregateChart(data, interval, color):
    global scene
    secData = aggregateBySec(data, interval)
    chartData = []
    for row in secData:
         chartData.append((round(row['time'] / 1000), row['price']))
    return scene.addChartLine(chartData, color)


def keyPress(key):
    global charts
    global pointVisible
    print("key = %d" % key)
    if key >= 49 and key < 57:
        chart = charts[key - 49]
        if chart.isVisible():
             chart.hide()
        else:
            chart.show()

    if key == 80:  # p
        if pointVisible:
            pointVisible = False
        else:
            pointVisible = True
        mainChart.setPointsVisible(pointVisible)
        for chart in charts:
            chart.setPointsVisible(pointVisible)


startPoint = 0
endPoint = 0
if len(sys.argv) > 1:
    if len(sys.argv) >= 2:
        startPoint = int(sys.argv[1])

    if len(sys.argv) == 3:
        endPoint = int(sys.argv[2])

print("startPoint = %d, endPoint = %d" % (startPoint, endPoint));
data = loadData(startPoint, endPoint)
scene = ChartScene(len(data))
view = SceneView(scene)
mainWindow = MainWindow(view)
mainWindow.show()
mainWindow.setKeyPressAction(keyPress)
pointVisible = False


chartData = []
for row in data:
     chartData.append((float(row['time']) / 1000, row['price']))
mainChart = scene.addChartLine(chartData, QColor(180, 180, 180))



charts = []
charts.append(addAggregateChart(data, 1, QColor(0, 0, 255)))
charts.append(addAggregateChart(data, 5, QColor(255, 255, 0)))
charts.append(addAggregateChart(data, 10, QColor(0, 255, 0)))
charts.append(addAggregateChart(data, 30, QColor(255, 0, 0)))
charts.append(addAggregateChart(data, 60, QColor(0, 255, 255)))
charts.append(addAggregateChart(data, 5 * 60, QColor(130, 130, 130)))
charts.append(addAggregateChart(data, 10 * 60, QColor(130, 130, 0)))
for chart in charts:
    chart.hide()




# xyData = dataToXY(data)

# linearRegression = LinearRegression(xyData[3000:6000])
# p1 = linearRegression.point(3000)
# p2 = linearRegression.point(6000)

# l = ChartLine(scene, p1, p2)
# l.setPen(QPen(Qt.red))
# scene.addItem(l)



