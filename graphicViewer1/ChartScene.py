from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.Qt import *
from PyQt5.QtChart import *


class ChartScene(QGraphicsScene):
    def __init__(self, len):
        QGraphicsScene.__init__(self)
        self.originalChartLen = len
        self.chartLen = self.originalChartLen
        self.chart = QChart()
        self.chart.legend().hide()
        self.setChartWidth(self.chartLen)
        self.chart.setPos(0, 0)
        self.addItem(self.chart)
        self.mousePos = QPointF()


    def addChartLine(self, data, color):
        series = QLineSeries()
        pen = QPen(color)
        pen.setWidth(1)
        series.setPen(pen)
        if data:
            for x, y in data:
                series.append(float(x), float(y))
        self.chart.addSeries(series)
        self.chart.createDefaultAxes()
        return series


    def setChangeMousePosAction(self, action):
        self.changeMousePosAction = action


    def mapToScene(self, chartPos):
        return self.chart.mapToScene(self.chart.mapToPosition(chartPos))


    def mapFromScene(self, scenePos):
        return self.chart.mapToValue(scenePos)


    def mouseMoveEvent(self, ev):
        self.mousePos = self.mapFromScene(ev.scenePos())
        if self.changeMousePosAction:
            self.changeMousePosAction(self.mousePos)


    def setChartWidth(self, chartLen):
        self.chart.setMinimumSize(chartLen, 800)
        self.chart.setMaximumSize(chartLen, 800)
        self.setSceneRect(0, 0, self.chartLen, 800)


    def chartScaleDelimiterIncrease(self):
        self.chartLen /= 2
        self.setChartWidth(self.chartLen)


    def chartScaleDelimiterDecrease(self):
        self.chartLen *= 2
        self.setChartWidth(self.chartLen)

