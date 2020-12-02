#!/usr/bin/env python

##Copyright 2009-2014 Thomas Paviot (tpaviot@gmail.com)
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

from OCC.Core.gp import gp_Dir, gp_Ax2, gp_Circ, gp_Pnt
from OCC.Core.AIS import AIS_Shape, AIS_RadiusDimension
from OCC.Core.Quantity import Quantity_Color, Quantity_NOC_BLACK
from OCC.Core.Prs3d import Prs3d_DimensionAspect
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeEdge
from OCC.Display.SimpleGui import init_display

display, start_display, add_menu, add_function_to_menu = init_display()

c = gp_Circ(gp_Ax2(gp_Pnt(200., 200., 0.), gp_Dir(0., 0., 1.)), 80)
ec = BRepBuilderAPI_MakeEdge(c).Edge()
ais_shp = AIS_Shape(ec)
display.Context.Display(ais_shp, True)

rd = AIS_RadiusDimension(ec)
the_aspect = Prs3d_DimensionAspect()
the_aspect.SetCommonColor(Quantity_Color(Quantity_NOC_BLACK))
rd.SetDimensionAspect(the_aspect)

display.Context.Display(rd, True)
display.FitAll()
start_display()
