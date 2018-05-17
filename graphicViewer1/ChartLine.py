from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.Qt import *
from ChartScene import *

class ChartLine(QGraphicsLineItem):

    def __init__(self, chart, p1, p2):
        QGraphicsLineItem.__init__(self)
        print("p1 = %s" % p1)
        print("p2 = %s" % p2)
        p1 = chart.mapToScene(p1)
        p2 = chart.mapToScene(p2)
        print("p1 = %s" % p1)
        print("p2 = %s" % p2)
        self.setPos(p1)
        self.setLine(QLineF(QPointF(0, 0), p2 - p1))

