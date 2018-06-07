from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.Qt import *
from PyQt5.QtChart import *


class ChartScene(QGraphicsScene):
    def __init__(self):
        QGraphicsScene.__init__(self)
        self.chartPlain = QChart()
        self.chartPlain.legend().hide()
        self.chartPlain.setPos(0, 0)
        self.addItem(self.chartPlain)
        self.mousePos = QPointF()
        self.maxChartLen = 1
        self.chartLen = self.maxChartLen
        self.chartSeriesList = []


    def setMaxLen(self, len):
        k = self.maxChartLen / self.chartLen
        self.maxChartLen = len
        self.chartLen = self.maxChartLen / k
        self.setChartWidth(self.chartLen)


    def addChart(self, series):
        self.chartSeriesList.append(series)
        if not series.count():
            return
        self.chartPlain.addSeries(series)


    def update(self):
        for series in self.chartSeriesList:
            if self.chartPlain.series():
                self.chartPlain.removeSeries(series)
            if series.count():
                self.chartPlain.addSeries(series)
        self.chartPlain.createDefaultAxes()


    def setChangeMousePosAction(self, action):
        self.changeMousePosAction = action


    def mapToScene(self, chartPos):
        return self.chartPlain.mapToScene(self.chartPlain.mapToPosition(chartPos))


    def mapFromScene(self, scenePos):
        return self.chartPlain.mapToValue(scenePos)


    def mouseMoveEvent(self, ev):
        self.mousePos = self.mapFromScene(ev.scenePos())
        if self.changeMousePosAction:
            self.changeMousePosAction(self.mousePos)


    def setChartWidth(self, chartLen):
        self.chartPlain.setMinimumSize(chartLen, 800)
        self.chartPlain.setMaximumSize(chartLen, 800)
        self.setSceneRect(0, 0, self.chartLen, 800)


    def chartScaleDelimiterIncrease(self):
        self.chartLen /= 2
        self.setChartWidth(self.chartLen)


    def chartScaleDelimiterDecrease(self):
        self.chartLen *= 2
        self.setChartWidth(self.chartLen)

