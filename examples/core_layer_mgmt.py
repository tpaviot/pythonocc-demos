##Copyright 2021 Tanneguy de Villemagne (tanneguydv@gmail.com)
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

from OCC.Display.SimpleGui import init_display
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeBox
from OCC.Core.gp import gp_Pnt, gp_Vec, gp_Trsf
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_Transform
from OCC.Extend.LayerManager import Layer

display, start_display, add_menu, add_functionto_menu = init_display()

box1 = BRepPrimAPI_MakeBox(gp_Pnt(0, 0, 10), 10, 10, 100).Shape()
box2 = BRepPrimAPI_MakeBox(gp_Pnt(), 100, 10, 10).Shape()
box3 = BRepPrimAPI_MakeBox(10, 100, 10).Shape()
box4 = BRepPrimAPI_MakeBox(gp_Pnt(100, 100, 0), 10, 10, 100).Shape()
box5 = BRepPrimAPI_MakeBox(gp_Pnt(0, 100, 0), 100, 10, 10).Shape()
box6 = BRepPrimAPI_MakeBox(gp_Pnt(100, 0, 0), 10, 100, 10).Shape()
trns = gp_Trsf()
trns.SetTranslation(gp_Vec(0, 0, 110))

layer1 = Layer(display, color=123)
layer1.add(box1)

layer2 = Layer(display, box4, 86)
layer2.add(box5)
layer2.show()

layer3 = Layer(display, box2, 76)
layer3.add(box3)
layer3.add(box6)

layer3.merge(layer1, True)
layer3.show()
layer3_shapes = layer3.get_shapes()
layer4 = Layer(display, color=32)
for shape in layer3_shapes:
    translated = BRepBuilderAPI_Transform(shape, trns).Shape()
    layer4.add(translated)
layer4.show()

display.FitAll()
start_display()
