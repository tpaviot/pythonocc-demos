##Author github user @Tanneguydv, 2023

import os
import sys
from OCC.Core.BRepPrimAPI import (
    BRepPrimAPI_MakeBox, 
    BRepPrimAPI_MakeSphere)
from OCC.Core.gp import gp_Pnt
from OCC.Core.AIS import AIS_Manipulator
from OCC.Extend.LayerManager import Layer

from OCC.Display.backend import load_backend
load_backend("qt-pyqt5")
import OCC.Display.qtDisplay as qtDisplay

from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QPushButton,
    QHBoxLayout,
    QGroupBox,
    QDialog,
    QVBoxLayout,
)

class App(QDialog):
    def __init__(self):
        super().__init__()
        self.title = "PyQt5 / pythonOCC / Manipulator"
        self.left = 300
        self.top = 300
        self.width = 800
        self.height = 300
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.createLayout()

        windowLayout = QVBoxLayout()
        windowLayout.addWidget(self.horizontalGroupBox)
        self.setLayout(windowLayout)
        self.show()

    def createLayout(self):
        self.horizontalGroupBox = QGroupBox("Display PythonOCC")
        layout_h = QHBoxLayout()
        layout_v = QVBoxLayout()

        self.activate_manip_button = QPushButton("Activate Manipulator", self)
        self.activate_manip_button.setCheckable(True)
        self.activate_manip_button.clicked.connect(self.activate_manipulator)
        layout_v.addWidget(self.activate_manip_button)

        self.show_layer_button = QPushButton("Show Layer", self)
        self.show_layer_button.setCheckable(True)
        self.show_layer_button.setChecked(True)
        self.show_layer_button.clicked.connect(self.show_layer)
        layout_v.addWidget(self.show_layer_button)
        layout_h.addLayout(layout_v)

        self.canvas = qtDisplay.qtViewer3dManip(self)
        layout_h.addWidget(self.canvas)
        self.horizontalGroupBox.setLayout(layout_h)

        self.canvas.InitDriver()
        self.display = self.canvas._display

        box = BRepPrimAPI_MakeBox(15.0, 15.0, 15.0).Shape()
        self.layer = Layer(self.display, box)
        sphere = BRepPrimAPI_MakeSphere(gp_Pnt(25, 25, 25), 5).Shape()
        self.layer.add_shape(sphere)
        self.show_layer()
        self.layer.merge()

    def show_layer(self):
        if self.show_layer_button.isChecked():
            self.layer.show()
            self.display.FitAll()
        else:
            self.layer.hide()
            self.display.FitAll()

    def activate_manipulator(self):
        if self.activate_manip_button.isChecked():
            selected = self.display.GetSelectedShape()
            if selected is not None:
                # retrieve the AIS_Shape from the selected TopoDS_Shape
                self.ais_element_manip, self.index_element_manip = self.layer.get_aisshape_from_topodsshape(selected)
                self.shape_element_manip = selected
                # Create and attach a Manipulator to AIS_Shape
                self.manip = AIS_Manipulator()
                self.manip.Attach(self.ais_element_manip)
                # Pass the Manipulator to the Qtviewer
                self.canvas.set_manipulator(self.manip)
                self.display.View.Redraw()
            else:
                self.activate_manip_button.setChecked(False)
        else:
            # Get the transformations done with the manipulator
            trsf = self.canvas.get_trsf_from_manip()
            # Apply the transformation to the TopoDS_Shape and replace it in the layer
            self.layer.update_trsf_shape(self.shape_element_manip, self.index_element_manip, trsf)
            self.manip.Detach() 


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = App()
    if os.getenv("APPVEYOR") is None:
        sys.exit(app.exec_())
