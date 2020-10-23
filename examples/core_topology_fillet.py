##Copyright 2009-2016 Thomas Paviot (tpaviot@gmail.com)
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
import sys
from math import cos, pi

from OCC.Core.BRepAlgoAPI import BRepAlgoAPI_Fuse
from OCC.Core.BRepFilletAPI import BRepFilletAPI_MakeFillet
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeBox, BRepPrimAPI_MakeCylinder
from OCC.Display.SimpleGui import init_display
from OCC.Core.TColgp import TColgp_Array1OfPnt2d
from OCC.Core.gp import gp_Ax2, gp_Pnt, gp_Dir, gp_Pnt2d
from OCC.Extend.TopologyUtils import TopologyExplorer

display, start_display, add_menu, add_function_to_menu = init_display()


def fillet(event=None):
    display.EraseAll()
    box = BRepPrimAPI_MakeBox(gp_Pnt(-400, 0, 0), 200, 230, 180).Shape()
    fillet = BRepFilletAPI_MakeFillet(box)
    # Add fillet on each edge
    for e in TopologyExplorer(box).edges():
        fillet.Add(20, e)

    blended_box = fillet.Shape()

    p_1 = gp_Pnt(250, 150, 75)
    s_1 = BRepPrimAPI_MakeBox(300, 200, 200).Shape()
    s_2 = BRepPrimAPI_MakeBox(p_1, 120, 180, 70).Shape()
    fused_shape = BRepAlgoAPI_Fuse(s_1, s_2).Shape()

    fill = BRepFilletAPI_MakeFillet(fused_shape)
    for e in TopologyExplorer(fused_shape).edges():
        fill.Add(e)

    for i in range(1, fill.NbContours() + 1):
        length = fill.Length(i)
        radius = 0.15 * length
        fill.SetRadius(radius, i, 1)

    blended_fused_solids = fill.Shape()

    display.DisplayShape(blended_box)
    display.DisplayShape(blended_fused_solids, update=True)


def rake(event=None):
    display.EraseAll()
    # Create Box
    box = BRepPrimAPI_MakeBox(200, 200, 200).Shape()
    # Fillet
    rake = BRepFilletAPI_MakeFillet(box)
    expl = list(TopologyExplorer(box).edges())

    rake.Add(8, 50, expl[3])
    rake.Build()
    if rake.IsDone():
        evolved_box = rake.Shape()
        display.DisplayShape(evolved_box, update=True)
    else:
        print("Rake not done.")


def fillet_cylinder(event=None):
    display.EraseAll()
    # Create Cylinder
    cylinder = BRepPrimAPI_MakeCylinder(gp_Ax2(gp_Pnt(-300, 0, 0), gp_Dir(0, 0, 1)), 100, 200).Shape()
    fillet = BRepFilletAPI_MakeFillet(cylinder)
    display.DisplayShape(cylinder, update=True)
    tab_point_2 = TColgp_Array1OfPnt2d(0, 20)
    for i in range(0, 20):
        point_2d = gp_Pnt2d(i * 2 * pi / 19, 60 * cos(i * pi / 19 - pi / 2) + 10)
        tab_point_2.SetValue(i, point_2d)
        display.DisplayShape(point_2d)

    expl2 = TopologyExplorer(cylinder).edges()
    fillet.Add(tab_point_2, next(expl2))
    fillet.Build()
    if fillet.IsDone():
        law_evolved_cylinder = fillet.Shape()
        display.DisplayShape(law_evolved_cylinder, update=True)
    else:
        print("fillet not done.")


def variable_filleting(event=None):
    a_pnt = gp_Pnt(350, 0, 0)
    box_2 = BRepPrimAPI_MakeBox(a_pnt, 200, 200, 200).Shape()
    a_fillet = BRepFilletAPI_MakeFillet(box_2)

    tab_point = TColgp_Array1OfPnt2d(1, 6)
    p_1 = gp_Pnt2d(0., 8.)
    p_2 = gp_Pnt2d(0.2, 16.)
    p_3 = gp_Pnt2d(0.4, 25.)
    p_4 = gp_Pnt2d(0.6, 55.)
    p_5 = gp_Pnt2d(0.8, 28.)
    p_6 = gp_Pnt2d(1., 20.)
    tab_point.SetValue(1, p_1)
    tab_point.SetValue(2, p_2)
    tab_point.SetValue(3, p_3)
    tab_point.SetValue(4, p_4)
    tab_point.SetValue(5, p_5)
    tab_point.SetValue(6, p_6)

    expl3 = list(TopologyExplorer(box_2).edges())

    a_fillet.Add(tab_point, expl3[9])
    a_fillet.Build()
    if a_fillet.IsDone():
        law_evolved_box = a_fillet.Shape()
        display.DisplayShape(law_evolved_box)
    else:
        print("aFillet not done.")
    display.FitAll()


def exit(event=None):
    sys.exit()


if __name__ == '__main__':
    add_menu('topology fillet operations')
    add_function_to_menu('topology fillet operations', fillet)
    add_function_to_menu('topology fillet operations', rake)
    add_function_to_menu('topology fillet operations', variable_filleting)
    add_function_to_menu('topology fillet operations', fillet_cylinder)
    add_function_to_menu('topology fillet operations', exit)
    start_display()
