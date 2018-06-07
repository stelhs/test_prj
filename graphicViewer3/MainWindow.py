from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.Qt import *

class MainWindow(QMainWindow):
    def __init__(self, view):
        QMainWindow.__init__(self)
        self.view = view
        mainWidwet = QWidget()
        self.setCentralWidget(mainWidwet)
        self.mainLayout = QVBoxLayout(mainWidwet)
        self.setLayout(self.mainLayout)
        self.keyPressAction = None

        self.currentCursorCoordinatesLabel = QLabel()
        self.currentCursorCoordinatesLabel.setFrameStyle(Qt.SolidLine)

        self.statusBar = QStatusBar()
        self.statusBar.addPermanentWidget(self.currentCursorCoordinatesLabel)
        self.mainLayout.addWidget(view);
        self.mainLayout.addWidget(self.statusBar);

        scene = view.scene()


    def displayCoordinate(self, x , y):
            self.currentCursorCoordinatesLabel.setText(
                                    "sec: %.3f, price: %.2f" % (x, y))


    def setKeyPressAction(self, action):
        self.keyPressAction = action


    def keyPressEvent(self, event):
        key = event.key()
        if self.keyPressAction:
            self.keyPressAction(key)
        QMainWindow.keyPressEvent(self, event)


