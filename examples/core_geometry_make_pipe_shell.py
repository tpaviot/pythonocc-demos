# #Copyright 2020 @botengu
# #
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

from OCC.Core.BRepOffsetAPI import BRepOffsetAPI_MakePipeShell
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeEdge, BRepBuilderAPI_MakeWire
from OCC.Core.Geom import Geom_BezierCurve
from OCC.Core.Law import Law_Linear
from OCC.Core.TColgp import TColgp_Array1OfPnt
from OCC.Core.gp import gp_Circ, gp_Pnt, gp_ZOX

from OCC.Display.SimpleGui import init_display

display, start_display, add_menu, add_function_to_menu = init_display()


def thicken_spline(event=None):
    # Creation of points for the spine
    array = TColgp_Array1OfPnt(1, 5)
    array.SetValue(1, gp_Pnt(1, 4, 0))
    array.SetValue(2, gp_Pnt(2, 2, 0))
    array.SetValue(3, gp_Pnt(3, 3, 0))
    array.SetValue(4, gp_Pnt(4, 3, 0))
    array.SetValue(5, gp_Pnt(5, 5, 0))

    # Creation of a Bezier Curve as the spine
    bz_curv = Geom_BezierCurve(array)
    bz_curv_edge = BRepBuilderAPI_MakeEdge(bz_curv).Edge()
    bz_curv_wire = BRepBuilderAPI_MakeWire(bz_curv_edge).Wire()
    display.DisplayShape(bz_curv_wire)

    # Creation of profile to sweep along the spine
    circle = gp_Circ(gp_ZOX(), 1)
    circle.SetLocation(array[0])
    circle_edge = BRepBuilderAPI_MakeEdge(circle).Edge()
    circle_wire = BRepBuilderAPI_MakeWire(circle_edge).Wire()

    # Creation of the law to dictate the evolution of the profile
    brep1 = BRepOffsetAPI_MakePipeShell(bz_curv_wire)
    law_f = Law_Linear()
    law_f.Set(0, 0.5, 1, 1)
    brep1.SetLaw(circle_wire, law_f, False, True)
    return brep1.Shape()


if __name__ == "__main__":
    display.DisplayShape(thicken_spline(), update=True)
    start_display()
