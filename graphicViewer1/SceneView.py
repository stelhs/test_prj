from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.Qt import *


class SceneView(QGraphicsView):
    def __init__(self, scene):
        QGraphicsView.__init__(self, scene)
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.zoomFactor = 1.25
        self.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self.setMouseTracking(True)
        self.scalePercent = 100
        self.keyCTRL = False
        self.keyShift = False
        self.keyAlt = False
        self.setRenderHint(QPainter.Antialiasing);
        self.setZoom(100, QPointF(0, 0))


    def zoomIn(self, zoomPos):
        c = QCursor()
        mousePos = c.pos()
        scenePos = self.mapToScene(zoomPos)

        zoomFactor = self.zoomFactor
        self.scale(zoomFactor, zoomFactor)
        self.centerOn(QPointF(scenePos))

        movedPos = self.mapFromScene(scenePos)
        newMousePos = mousePos + (movedPos - zoomPos)
        c.setPos(newMousePos)
        self.scalePercent *= self.zoomFactor


    def zoomOut(self, zoomPos):
        c = QCursor()
        mousePos = c.pos()
        scenePos = self.mapToScene(zoomPos)

        zoomFactor = 1 / self.zoomFactor
        self.scale(zoomFactor, zoomFactor)
        self.centerOn(QPointF(scenePos))

        movedPos = self.mapFromScene(scenePos)
        newMousePos = mousePos + (movedPos - zoomPos)
        c.setPos(newMousePos)
        self.scalePercent /= self.zoomFactor


    def zoomReset(self, zoomPos):
        c = QCursor()
        mousePos = c.pos()
        scenePos = self.mapToScene(zoomPos)

        self.resetMatrix()
        self.centerOn(QPointF(scenePos))

        movedPos = self.mapFromScene(scenePos)
        newMousePos = mousePos + (movedPos - zoomPos)
        c.setPos(newMousePos)
        self.scalePercent = 100


    def setZoom(self, percent, center=None):
        self.scalePercent = percent
        self.resetTransform()
        if percent == 100:
            self.centerOn(center)
            return
        zoomFactor = percent / 100
        self.scale(zoomFactor, zoomFactor)
        if not center:
            return
        self.centerOn(center)


    def zoom(self):
        return self.scalePercent


    def wheelEvent(self, event):
        if self.keyCTRL:
            deltaY = 0
            if event.angleDelta().y() > 0:
                deltaY += 80
            else:
                deltaY -= 80
            bar = self.verticalScrollBar()
            bar.setValue(bar.value() + deltaY)
            return

        if self.keyShift:
            deltaX = 0
            if event.angleDelta().y() > 0:
                deltaX += 80
            else:
                deltaX -= 80
            bar = self.horizontalScrollBar()
            bar.setValue(bar.value() + deltaX)
            return

        if event.angleDelta().y() > 0:
            self.zoomIn(event.pos())
        else:
            self.zoomOut(event.pos())


    def keyShiftPress(self):
        self.keyShift = True


    def keyCTRLPress(self):
        self.keyCTRL = True


    def keyShiftRelease(self):
        self.keyShift = False


    def keyCTRLRelease(self):
        self.keyCTRL = False


    def keyPressEvent(self, event):
        key = event.key()
        QGraphicsView.keyPressEvent(self, event)
        if key == 16777251:  # ALT
            self.keyAlt = True
            self.setDragMode(QGraphicsView.ScrollHandDrag)
            return

        # increase chart scale
        if key == 45:  # -
            scene = self.scene()
            mousePosChart = scene.mousePos
            scene.chartScaleDelimiterIncrease()
            self.setZoom(self.zoom(), scene.mapToScene(mousePosChart))
            return

        # decrease chart scale
        if key == 43:  # +
            scene = self.scene()
            mousePosChart = scene.mousePos
            scene.chartScaleDelimiterDecrease()
            self.setZoom(self.zoom(), scene.mapToScene(mousePosChart))
            return


    def keyReleaseEvent(self, event):
        key = event.key()
        if key == 16777251:  # ALT
            self.keyAlt = False
            self.setDragMode(QGraphicsView.NoDrag)
            return


    def mousePressEvent(self, ev):
        QGraphicsView.mousePressEvent(self, ev)
        if self.keyAlt:
            return

        if ev.button() == 2:
            scene = self.scene()
            mousePosChart = scene.mousePos
            scene.chartScaleDelimiterIncrease()
            self.setZoom(self.zoom(), scene.mapToScene(mousePosChart))
            return

        if ev.button() == 1:
            scene = self.scene()
            mousePosChart = scene.mousePos
            scene.chartScaleDelimiterDecrease()
            self.setZoom(self.zoom(), scene.mapToScene(mousePosChart))
            return


    def center(self):
        return self.mapToScene(QPoint(self.width() / 2, self.height() / 2))




