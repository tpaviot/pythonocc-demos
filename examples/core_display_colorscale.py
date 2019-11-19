#!/usr/bin/env python
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

from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeBox
from OCC.Core.AIS import AIS_Shape, AIS_ColorScale
from OCC.Core.Graphic3d import Graphic3d_ZLayerId_TopOSD, Graphic3d_TMF_2d
from OCC.Core.Quantity import Quantity_NOC_BLACK
from OCC.Core.gp import gp_XY, gp_Pnt

from OCC.Display.SimpleGui import init_display

display, start_display, add_menu, add_function_to_menu = init_display()

myBox = BRepPrimAPI_MakeBox(60, 60, 50).Shape()

colorscale = AIS_ColorScale()

# colorscale properties
aMinRange    = colorscale.GetMin()
aMaxRange    = colorscale.GetMax()
aNbIntervals = colorscale.GetNumberOfIntervals()
aTextHeight  = colorscale.GetTextHeight()
labPosition = colorscale.GetLabelPosition()
position =  gp_XY(colorscale.GetXPosition(), colorscale.GetYPosition())
title = colorscale.GetTitle()

# colorscale display
colorscale.SetSize(300, 300)
colorscale.SetRange(0.0, 10.0)
colorscale.SetNumberOfIntervals(10)

colorscale.SetZLayer (Graphic3d_ZLayerId_TopOSD)
colorscale.SetTransformPersistence(Graphic3d_TMF_2d, gp_Pnt (-1, -1, 0))
colorscale.SetToUpdate()

display.Context.Display(colorscale, True)
display.DisplayShape(myBox)

start_display()
