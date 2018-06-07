from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.Qt import *
from PyQt5.QtChart import *


class Trading():
    aggregateIntervals = (
                          {'interval': 1,
                           'color': QColor(0, 0, 255)},
                          {'interval': 5,
                           'color': QColor(255, 255, 0)},
                          {'interval': 10,
                           'color': QColor(0, 255, 0)},
                          {'interval': 30,
                           'color': QColor(255, 0, 0)},
                          {'interval': 60,
                           'color': QColor(0, 255, 255)},
                          {'interval': 5 * 60,
                           'color': QColor(130, 130, 130)},
                          {'interval': (10 * 60),
                           'color': QColor(130, 130, 0)},
                         )
    integratorIntervals = (
                          {'interval': 1,
                           'color': QColor(0, 0, 200)},
                          {'interval': 5,
                           'color': QColor(200, 200, 0)},
                          {'interval': 10,
                           'color': QColor(0, 200, 0)},
                          {'interval': 30,
                           'color': QColor(200, 0, 0)},
                          {'interval': 60,
                           'color': QColor(0, 200, 200)},
                          {'interval': 5 * 60,
                           'color': QColor(80, 80, 80)},
                          {'interval': (10 * 60),
                           'color': QColor(80, 80, 0)},
                         )
    def __init__(self, scene):
        self.priceHistory = []
        self.chartHistories = []
        self.scene = scene
        self.chartPointsEnabled = False

        self.mainChart = QLineSeries()
        self.mainChart.setPen(QPen(QColor(180, 180, 180)))
        scene.addChart(self.mainChart)

        for row in Trading.aggregateIntervals:
           chart = HistoryChart(scene, row['interval'], row['color'])
           self.chartHistories.append(chart)

        for row in Trading.integratorIntervals:
            chart = IntegratorChart(scene, row['interval'], row['color'])
            self.chartHistories.append(chart)


    def push(self, time, price):
        self.priceHistory.append((time, price))
        self.mainChart.append(time / 1000, price)
        self.scene.setMaxLen(len(self.priceHistory))
        for chart in self.chartHistories:
            chart.push(time, price)
        self.scene.update()
        view = self.scene.views()[0]
        view.setZoom(view.zoom(), self.scene.mapToScene(QPointF(time / 1000, price)))


    def chartByNum(self, chartNum):
        return self.chartHistories[chartNum]


    def chartEnablePoints(self):
        self.chartPointsEnabled = True
        for chart in self.chartHistories:
            chart.setPointsVisible(True)
        self.mainChart.setPointsVisible(True)


    def chartDisablePoints(self):
        self.chartPointsEnabled = False
        for chart in self.chartHistories:
            chart.setPointsVisible(False)
        self.mainChart.setPointsVisible(False)


    def chartPointsIsVisible(self):
        return self.chartPointsEnabled




class AggregateHistory():
    def __init__(self, interval):
        self.interval = interval
        self.history = []
        self.lastTime = 0
        self.integrator = []
        self.newPointAction = None


    def integrate(self):
        if not len(self.integrator):
            return 0

        sum = 0
        for val in self.integrator:
            sum += val
        return sum / len(self.integrator)


    def push(self, time, price):
        if not self.lastTime:
            self.lastTime = time

        if time > (self.lastTime + self.interval * 1000):
            self.lastTime = time
            val = self.integrate()
            if not val:
                return

            self.history.append(val)
            if self.newPointAction:
                self.newPointAction(time, val)
            self.integrator = []
            return

        self.integrator.append(price)


    def setAction(self, fn, type):
        if type == 'newPoint':
            self.newPointAction = fn




class HistoryChart(AggregateHistory, QLineSeries):
    def __init__(self, scene, interval, color):
        AggregateHistory.__init__(self, interval)
        QLineSeries.__init__(self)
        self.scene = scene
        pen = QPen(color)
        pen.setWidth(1)
        self.setPen(pen)

        def drawPoint(time, price):
            self.append(float(time) / 1000, price)
        self.setAction(drawPoint, 'newPoint')
        self.hide()
        self.scene.addChart(self)





class IntegratorSec():
    def __init__(self, interval):
        self.integrator = []
        self.interval = interval
        self.full = False


    def push(self, time, price):

        self.integrator.append((time, price))

        time1 = self.integrator[0][0]
        time2 = self.integrator[-1][0]
        if (time2 - time1) > (self.interval * 1000):
            self.full = True
            del(self.integrator[:1])
            return


    def reset(self):
        self.integrator = []


    def integratedPrice(self):
        summ = 0
        for time, price in self.integrator:
            summ += price
        return summ / len(self.integrator)


    def isEmpty(self):
        return not len(self.integrator)


    def isFull(self):
        return self.full






class IntegratorChart(IntegratorSec, QLineSeries):
    def __init__(self, scene, interval, color):
        IntegratorSec.__init__(self, interval)
        QLineSeries.__init__(self)
        self.scene = scene
        pen = QPen(color)
        pen.setWidth(1)
        self.setPen(pen)
        self.hide()
        self.scene.addChart(self)


    def push(self, time, price):
        IntegratorSec.push(self, time, price)
        if not self.isFull():
            return
        integratedPrice = self.integratedPrice()
        self.append(float(time) / 1000, integratedPrice)




class LinearRegression():
    def __init__(self, points):
        x = np.array([item[0] for item in points])
        y = np.array([item[1] for item in points])
        A = np.vstack([x, np.ones(len(x))]).T
        self.a, self.b = np.linalg.lstsq(A, y)[0]

    def point(self, time):
        price = self.a * time + self.b
        return QPointF(time, price)




