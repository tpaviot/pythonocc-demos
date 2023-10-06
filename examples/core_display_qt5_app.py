##Author github user @Tanneguydv, 2021

import os
import sys
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeBox

from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QPushButton,
    QHBoxLayout,
    QGroupBox,
    QDialog,
    QVBoxLayout,
)

from OCC.Display.backend import load_backend

load_backend("pyqt5")
import OCC.Display.qtDisplay as qtDisplay


class App(QDialog):
    def __init__(self):
        super().__init__()
        self.title = "PyQt5 / pythonOCC"
        self.left = 300
        self.top = 300
        self.width = 800
        self.height = 300
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.createHorizontalLayout()

        windowLayout = QVBoxLayout()
        windowLayout.addWidget(self.horizontalGroupBox)
        self.setLayout(windowLayout)
        self.show()
        self.canvas.InitDriver()
        self.canvas.resize(200, 200)
        self.display = self.canvas._display

    def createHorizontalLayout(self):
        self.horizontalGroupBox = QGroupBox("Display PythonOCC")
        layout = QHBoxLayout()

        disp = QPushButton("Display Box", self)
        disp.clicked.connect(self.displayBOX)
        layout.addWidget(disp)

        eras = QPushButton("Erase Box", self)
        eras.clicked.connect(self.eraseBOX)
        layout.addWidget(eras)

        self.canvas = qtDisplay.qtViewer3d(self)
        layout.addWidget(self.canvas)
        self.horizontalGroupBox.setLayout(layout)

    def displayBOX(self):
        a_box = BRepPrimAPI_MakeBox(10.0, 20.0, 30.0).Shape()
        self.ais_box = self.display.DisplayShape(a_box)[0]
        self.display.FitAll()

    def eraseBOX(self):
        self.display.Context.Erase(self.ais_box, True)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = App()
    if os.getenv("APPVEYOR") is None:
        sys.exit(app.exec_())
