#!/usr/bin/env python

##Copyright 2020 Thomas Paviot (tpaviot@gmail.com)
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

from OCC.Core.AIS import AIS_ColoredShape
from OCC.Core.Graphic3d import Graphic3d_NOM_ALUMINIUM, Graphic3d_NOM_STEEL
from OCC.Core.Quantity import Quantity_Color
from OCC.Core.TopoDS import TopoDS_Compound, TopoDS_Builder

from OCC.Core.gp import gp_Vec
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeCylinder
from OCC.Extend.ShapeFactory import translate_shp
from OCC.Display.SimpleGui import init_display

available_materials = [Graphic3d_NOM_ALUMINIUM, Graphic3d_NOM_STEEL]

radius = 30
s = BRepPrimAPI_MakeCylinder(radius, 200).Shape()
delta_x = 0.0
solids = []
for _ in available_materials:
    s2 = translate_shp(s, gp_Vec(delta_x, 0.0, 0.0))
    delta_x += 2 * radius + 1.0
    solids.append(s2)

compound = TopoDS_Compound()
builder = TopoDS_Builder()
builder.MakeCompound(compound)
for solid in solids:
    builder.Add(compound, solid)

aColoredShape = AIS_ColoredShape(compound)
aColoredShape.SetCustomColor(solids[0], Quantity_Color(Graphic3d_NOM_STEEL))
aColoredShape.SetCustomColor(solids[1], Quantity_Color(Graphic3d_NOM_ALUMINIUM))

display, start_display, add_menu, add_function_to_menu = init_display()
display.GetContext().Display(aColoredShape, False)
display.FitAll()
start_display()
