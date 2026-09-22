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

"""Text labels attached to 3d points, always facing the camera and with a
constant size on screen: the text is a tessellated shape (text_to_brep)
displayed with a zoom and rotate transform persistence. Rotate and zoom the
view, the vertex numbers stay readable and keep their size.

With a transform persistence, the text size is in pixels and the anchor
point is the 3d position of the label. Graphic3d_TMF_ZoomPers alone keeps
the size constant but the text still turns with the camera."""

from OCC.Core.AIS import AIS_Shaded, AIS_Shape
from OCC.Core.Addons import Font_FontAspect_Bold, text_to_brep
from OCC.Core.BRep import BRep_Tool
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeBox
from OCC.Core.Graphic3d import Graphic3d_TMF_ZoomRotatePers, Graphic3d_TransformPers
from OCC.Core.Quantity import Quantity_Color, Quantity_NOC_RED
from OCC.Extend.TopologyUtils import TopologyExplorer
from OCC.Display.SimpleGui import init_display

display, start_display, add_menu, add_function_to_menu = init_display()

box = BRepPrimAPI_MakeBox(100.0, 60.0, 40.0).Shape()

# one label per vertex of the box, 20 pixels high
for number, vertex in enumerate(TopologyExplorer(box).vertices(), start=1):
    anchor = BRep_Tool.Pnt(vertex)
    label = AIS_Shape(
        text_to_brep(str(number), "Arial", Font_FontAspect_Bold, 20.0, True)
    )
    label.SetColor(Quantity_Color(Quantity_NOC_RED))
    label.SetTransformPersistence(
        Graphic3d_TransformPers(Graphic3d_TMF_ZoomRotatePers, anchor)
    )
    display.Context.Display(label, AIS_Shaded, 0, False)

display.DisplayShape(box, color="BLUE", transparency=0.7, update=True)
start_display()
