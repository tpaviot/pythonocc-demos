##Copyright 2026 Thomas Paviot (tpaviot@gmail.com)
##
##This file is part of pythonOCC.
##
##pythonOCC is free software: you can redistribute it and/or modify
##it under the terms of the GNU Lesser General Public License as published by
##the Free Software Foundation, either version 3 of the License, or
##(at your option) any later version.
##
##pythonOCC is distributed in the hope that it will be useful,
##but WITHOUT ANY WARRANTY; without even the implied warranty of
##MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##GNU Lesser General Public License for more details.
##
##You should have received a copy of the GNU Lesser General Public License
##along with pythonOCC.  If not, see <http://www.gnu.org/licenses/>.

"""The GeomBndLib package, new in OCCT 8.0: bounding boxes of Geom curves
and surfaces, computed analytically for the conics and quadrics and
numerically (BoxOptimal) for the free form geometries. Box() is fast but may
be loose, e.g. the box of the poles of a BSpline; BoxOptimal() is tight."""

import math

from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeEdge, BRepBuilderAPI_MakeFace
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeBox
from OCC.Core.Geom import Geom_Circle, Geom_ToroidalSurface
from OCC.Core.GeomAPI import GeomAPI_PointsToBSpline
from OCC.Core.GeomBndLib import GeomBndLib_Curve, GeomBndLib_Surface
from OCC.Core.gp import gp_Ax2, gp_Ax3, gp_Dir, gp_Pnt
from OCC.Core.TColgp import TColgp_Array1OfPnt
from OCC.Display.SimpleGui import init_display

display, start_display, add_menu, add_function_to_menu = init_display()


def display_box(bnd_box, color):
    """Displays a Bnd_Box as a transparent box."""
    xmin, ymin, zmin, xmax, ymax, zmax = bnd_box.Get()
    box = BRepPrimAPI_MakeBox(
        gp_Pnt(xmin, ymin, zmin), gp_Pnt(xmax, ymax, zmax)
    ).Shape()
    display.DisplayShape(box, color=color, transparency=0.8)


def describe(name, bnd_box):
    xmin, ymin, zmin, xmax, ymax, zmax = bnd_box.Get()
    print(f"{name}: {xmax - xmin:.3f} x {ymax - ymin:.3f} x {zmax - zmin:.3f}")


# A tilted circle: the box is computed analytically, Box and BoxOptimal are
# identical
circle = Geom_Circle(gp_Ax2(gp_Pnt(0, 0, 0), gp_Dir(1, 1, 1)), 20.0)
circle_box = GeomBndLib_Curve(circle).Box(0.0)
describe("circle Box", circle_box)
describe("circle BoxOptimal", GeomBndLib_Curve(circle).BoxOptimal(0.0))
display.DisplayShape(BRepBuilderAPI_MakeEdge(circle).Edge(), color="BLUE")
display_box(circle_box, "BLUE")

# A BSpline through points: Box() encloses the control polygon, which
# overshoots the curve, BoxOptimal() is tight to the curve
points = TColgp_Array1OfPnt(1, 5)
for i, (x, y, z) in enumerate(
    ((60, 0, 0), (75, 40, 10), (90, -40, 20), (105, 40, 30), (120, 0, 40)), start=1
):
    points.SetValue(i, gp_Pnt(x, y, z))
bspline = GeomAPI_PointsToBSpline(points).Curve()
bspline_box = GeomBndLib_Curve(bspline).Box(0.0)
bspline_box_optimal = GeomBndLib_Curve(bspline).BoxOptimal(0.0)
describe("bspline Box", bspline_box)
describe("bspline BoxOptimal", bspline_box_optimal)
display.DisplayShape(BRepBuilderAPI_MakeEdge(bspline).Edge(), color="RED")
display_box(bspline_box, "RED")
display_box(bspline_box_optimal, "ORANGE")

# A torus, a quadric handled analytically
torus = Geom_ToroidalSurface(gp_Ax3(gp_Pnt(200, 0, 0), gp_Dir(0, 1, 1)), 25.0, 8.0)
torus_box = GeomBndLib_Surface(torus).Box(0.0)
describe("torus Box", torus_box)
display.DisplayShape(
    BRepBuilderAPI_MakeFace(torus, 0.0, 2 * math.pi, 0.0, 2 * math.pi, 1e-6).Face(),
    color="GREEN",
)
display_box(torus_box, "GREEN")

display.FitAll()
start_display()
