##Copyright 2021 Thomas Paviot (tpaviot@gmail.com)
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

from OCC.Core.BRepPrimAPI import (
    BRepPrimAPI_MakeBox,
    BRepPrimAPI_MakeCylinder,
    BRepPrimAPI_MakeSphere,
)
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_Transform
from OCC.Core.gp import gp_Trsf, gp_Vec

from OCC.Display.SimpleGui import init_display


def erase_box(event=None):
    display.Context.Erase(ais_box, True)


def erase_cylinder(event=None):
    display.Context.Erase(ais_cylinder, True)


def erase_sphere(event=None):
    display.Context.Erase(ais_sphere, True)


display, start_display, add_menu, add_function_to_menu = init_display()
# a box at the origin
a_box = BRepPrimAPI_MakeBox(10.0, 20.0, 30.0).Shape()

# a translated sphere along the x axis
trns = gp_Trsf()
trns.SetTranslation(gp_Vec(50, 0, 0))
a_sphere = BRepBuilderAPI_Transform(
    BRepPrimAPI_MakeSphere(10.0).Shape(), trns, False
).Shape()

# a translated cylinder along the x axis
trns = gp_Trsf()
trns.SetTranslation(gp_Vec(-50, 0, 0))
a_cylinder = BRepBuilderAPI_Transform(
    BRepPrimAPI_MakeCylinder(10.0, 40.0).Shape(), trns, False
).Shape()

ais_box = display.DisplayShape(a_box)[0]
ais_sphere = display.DisplayShape(a_sphere)[0]
ais_cylinder = display.DisplayShape(a_cylinder)[0]


if __name__ == "__main__":
    add_menu("Erase Shapes")
    add_function_to_menu("Erase Shapes", erase_box)
    add_function_to_menu("Erase Shapes", erase_cylinder)
    add_function_to_menu("Erase Shapes", erase_sphere)
    display.FitAll()
    start_display()
