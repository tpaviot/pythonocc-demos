##Copyright 2025 Thomas Paviot (tpaviot@gmail.com)
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

import os

from OCC.Core.gp import gp_Pnt
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeBox

from OCC.Core.BRepAlgoAPI import BRepAlgoAPI_Cut
from OCC.Display.SimpleGui import init_display
from OCC.Extend.DataExchange import read_stl_file

display, start_display, add_menu, add_function_to_menu = init_display()

stl_filename = os.path.join("..", "assets", "models", "fan.stl")


def cut_with_box(shp):
    box = BRepPrimAPI_MakeBox(gp_Pnt(30, -50, 0), 20, 40, 60).Shape()
    cut_result = BRepAlgoAPI_Cut(shp, box).Shape()
    return cut_result


def load_surf(event=None):
    """This is the default behavior"""
    display.EraseAll()
    stl_shp = read_stl_file(stl_filename)
    display.DisplayShape(cut_with_box(stl_shp), update=True)


def load_solid(event=None):
    """Explicit solid transformation"""
    display.EraseAll()
    stl_shp = read_stl_file(stl_filename, sew_shape=True, make_solid=True)
    display.DisplayShape(cut_with_box(stl_shp), update=True)


if __name__ == "__main__":
    add_menu("load STL")
    add_function_to_menu("load STL", load_surf)
    add_function_to_menu("load STL", load_solid)
    start_display()
