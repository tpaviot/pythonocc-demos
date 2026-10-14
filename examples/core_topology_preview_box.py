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

"""BRepPreviewAPI_MakeBox, new in OCCT 8.0: a box that accepts a null
dimension. It is used to preview a box while it is drawn interactively:
it degenerates to a face, an edge or a vertex instead of failing as
BRepPrimAPI_MakeBox does."""

from OCC.Core.BRepPreviewAPI import BRepPreviewAPI_MakeBox
from OCC.Core.gp import gp_Pnt
from OCC.Core.TopAbs import TopAbs_ShapeEnum
from OCC.Display.SimpleGui import init_display

display, start_display, add_menu, add_function_to_menu = init_display()

# the opposite corners of the box, relative to its first corner: the box
# is thin in 0, 1, 2 or 3 directions
PREVIEWS = [
    (gp_Pnt(20, 10, 15), "BLUE"),  # a solid
    (gp_Pnt(20, 10, 0), "GREEN"),  # a face, thin along Z
    (gp_Pnt(0, 0, 15), "RED"),  # an edge, thin along X and Y
    (gp_Pnt(0, 0, 0), "BLACK"),  # a vertex, thin in all directions
]

for i, (corner, color) in enumerate(PREVIEWS):
    first_corner = gp_Pnt(i * 40, 0, 0)
    second_corner = gp_Pnt(first_corner.X() + corner.X(), corner.Y(), corner.Z())
    maker = BRepPreviewAPI_MakeBox()
    maker.Init(first_corner, second_corner)
    maker.Build()
    preview = maker.Shape()
    shape_type = TopAbs_ShapeEnum(preview.ShapeType()).name
    print(f"box from {first_corner.Coord()} to {second_corner.Coord()}: {shape_type}")
    display.DisplayShape(preview, color=color)
    display.DisplayMessage(gp_Pnt(i * 40, -5, 0), shape_type.removeprefix("TopAbs_"))

display.View_Iso()
display.FitAll()
# the text labels are out of the bounding box of the shapes
display.ZoomFactor(0.8)
start_display()
