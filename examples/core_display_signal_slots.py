import sys

from OCC.Core.BRepGProp import brepgprop
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeBox, BRepPrimAPI_MakeSphere
from OCC.Core.gp import gp_Trsf, gp_Vec
from OCC.Core.GProp import GProp_GProps
from OCC.Core.TopAbs import TopAbs_EDGE, TopAbs_FACE, TopAbs_SOLID
from OCC.Core.TopLoc import TopLoc_Location
from OCC.Display.backend import get_qt_modules
from OCC.Display.SimpleGui import init_display

display, start_display, add_menu, add_function_to_menu = init_display("qt-pyqt5")
QtCore, QtGui, QtWidgets, QtOpenGL = get_qt_modules()

from OCC.Display.qtDisplay import qtViewer3d

print("Usage: press G to find the linear properties for volume, face, edge, vertex...")


def get_occ_viewer():
    """

    Returns
    -------

    qtViewer3d

    """
    app = QtWidgets.QApplication.instance()  # checks if QApplication already exists
    if not app:
        app = QtWidgets.QApplication(sys.argv)
    widgets = app.topLevelWidgets()
    for wi in widgets:
        if hasattr(wi, "_menus"):  # OCC.Display.SimpleGui.MainWindow
            viewer = wi.findChild(qtViewer3d, "qt_viewer_3d")
            return viewer


def on_select(shapes):
    """

    Parameters
    ----------
    shape : TopoDS_Shape

    """
    g1 = GProp_GProps()

    for shape in shapes:
        brepgprop.LinearProperties(shape, g1)
        mass = g1.Mass()
        centre_of_mass = g1.CentreOfMass()
        com_x = centre_of_mass.X()
        com_y = centre_of_mass.Y()
        com_z = centre_of_mass.Z()
        static_moments = g1.StaticMoments()
        print(
            f"shape {shape}: \n mass: {mass}"
            f"\n center of mass: {com_x}, {com_y}, {com_z}"
            f"\n static moments: {static_moments}"
        )


def also_on_select(shapes):
    for shape in shapes:
        if shape.ShapeType() == TopAbs_SOLID:
            print("solid selected")
        if shape.ShapeType() == TopAbs_EDGE:
            print("edge selected")
        if shape.ShapeType() == TopAbs_FACE:
            print("face selected")


def location_from_vector(x, y, z):
    trsf = gp_Trsf()
    trsf.SetTranslation(gp_Vec(x, y, z))
    loc = TopLoc_Location(trsf)
    return loc


cube = BRepPrimAPI_MakeBox(100, 100, 100).Shape()
sphere = BRepPrimAPI_MakeSphere(100).Shape()
sphere.Move(location_from_vector(500, 0, 0))

display.DisplayShape(cube)
display.DisplayShape(sphere)

viewer = get_occ_viewer()
viewer.sig_topods_selected.connect(on_select)
viewer.sig_topods_selected.connect(also_on_select)

display.FitAll()
start_display()
