from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.Qt import *
from PyQt5.QtChart import *


class Trading():
    aggregateIntervals = (
                       #   {'interval': 3,
                       #    'color': QColor(0, 0, 255)},
                       #   {'interval': 5,
                       #    'color': QColor(255, 255, 0)},
                       #   {'interval': 10,
                       #    'color': QColor(0, 255, 0)},
                        #  {'interval': 30,
                        #   'color': QColor(255, 0, 0)},
                        #  {'interval': 60,
                        #   'color': QColor(0, 255, 255)},
                        #  {'interval': 100,
                        #   'color': QColor(130, 130, 130)},
                        #  {'interval': 200,
                        #   'color': QColor(130, 130, 0)},
                         )
    integratorIntervals = (
                        #  {'interval': 1,
                        #   'color': QColor(0, 0, 200)},
                        #  {'interval': 2,
                        #   'color': QColor(200, 200, 0)},
                        #  {'interval': 3,
                        #   'color': QColor(0, 200, 0)},
                        #  {'interval': 5,
                        #   'color': QColor(200, 0, 0)},
                        #  {'interval': 10,
                        #   'color': QColor(0, 200, 200)},
                        #  {'interval': 100,
                        #   'color': QColor(80, 80, 80)},
                        #  {'interval': 200,
                        #   'color': QColor(80, 80, 0)},
                         )
    def __init__(self, scene):
        self.priceHistory = []
        self.chartHistories = []
        self.scene = scene
        self.chartPointsEnabled = False

        self.mainChart = QLineSeries()
        self.mainChart.setPen(QPen(QColor(180, 180, 180)))
        scene.addChart(self.mainChart)

        self.mainQtyChart = QLineSeries()
        self.mainQtyChart.setPen(QPen(QColor(200, 0, 0)))
        scene.addChart(self.mainQtyChart)

        for row in Trading.aggregateIntervals:
           chart = HistoryChart(scene, row['interval'], row['color'])
           self.chartHistories.append(chart)

        for row in Trading.integratorIntervals:
            chart = IntegratorChart(scene, row['interval'], row['color'])
            self.chartHistories.append(chart)


    def push(self, num, time, price, qty):
        self.priceHistory.append((num, time, price))
        self.mainChart.append(num, price)
        self.mainQtyChart.append(num, qty)
        self.scene.setMaxLen(len(self.priceHistory))
        for chart in self.chartHistories:
            chart.push(num, price)
        self.scene.update()
        view = self.scene.views()[0]
        view.setZoom(view.zoom(), self.scene.mapToScene(QPointF(num, price)))


    def chartByNum(self, chartNum):
        return self.chartHistories[chartNum]


    def chartEnablePoints(self):
        self.chartPointsEnabled = True
        for chart in self.chartHistories:
            chart.setPointsVisible(True)
        self.mainChart.setPointsVisible(True)
        self.mainQtyChart.setPointsVisible(True)


    def chartDisablePoints(self):
        self.chartPointsEnabled = False
        for chart in self.chartHistories:
            chart.setPointsVisible(False)
        self.mainChart.setPointsVisible(False)
        self.mainQtyChart.setPointsVisible(False)


    def chartPointsIsVisible(self):
        return self.chartPointsEnabled




class AggregateHistory():
    def __init__(self, interval):
        self.interval = interval
        self.history = []
        self.lastNum = 0
        self.integrator = []
        self.newPointAction = None


    def integrate(self):
        if not len(self.integrator):
            return 0

        sum = 0
        for val in self.integrator:
            sum += val
        return sum / len(self.integrator)


    def push(self, num, price):
        if not self.lastNum:
            self.lastNum = num

        if num > (self.lastNum + self.interval):
            self.lastNum = num
            val = self.integrate()
            if not val:
                return

            self.history.append(val)
            if self.newPointAction:
                self.newPointAction(num, val)
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

        def drawPoint(num, price):
            self.append(num, price)
        self.setAction(drawPoint, 'newPoint')
        self.hide()
        self.scene.addChart(self)





class IntegratorNum():
    def __init__(self, interval):
        self.integrator = []
        self.interval = interval
        self.full = False


    def push(self, num, price):
        self.integrator.append((num, price))
        num1 = self.integrator[0][0]
        num2 = self.integrator[-1][0]
        if (num2 - num1) > self.interval:
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





class IntegratorChart(IntegratorNum, QLineSeries):
    def __init__(self, scene, interval, color):
        IntegratorNum.__init__(self, interval)
        QLineSeries.__init__(self)
        self.scene = scene
        pen = QPen(color)
        pen.setWidth(1)
        self.setPen(pen)
        self.hide()
        self.scene.addChart(self)


    def push(self, num, price):
        IntegratorNum.push(self, num, price)
        if not self.isFull():
            return
        integratedPrice = self.integratedPrice()
        self.append(num, integratedPrice)





class LinearRegression():
    def __init__(self, points):
        x = np.array([item[0] for item in points])
        y = np.array([item[1] for item in points])
        A = np.vstack([x, np.ones(len(x))]).T
        self.a, self.b = np.linalg.lstsq(A, y)[0]

    def point(self, time):
        price = self.a * time + self.b
        return QPointF(time, price)




