#!/usr/bin/env python

##Copyright 2009-2014 Jelle Feringa (jelleferinga@gmail.com)
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
from math import pi

from OCC.Core.gp import gp_Pnt2d, gp_XOY, gp_Lin2d, gp_Ax3, gp_Dir2d
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeEdge
from OCC.Core.Geom import Geom_CylindricalSurface
from OCC.Core.GCE2d import GCE2d_MakeSegment

from OCC.Display.WebGl import threejs_renderer

# First buil an helix
aCylinder = Geom_CylindricalSurface(gp_Ax3(gp_XOY()), 6.0)
aLine2d = gp_Lin2d (gp_Pnt2d(0.0, 0.0), gp_Dir2d(1.0, 1.0))
aSegment = GCE2d_MakeSegment(aLine2d, 0.0, pi * 2.0)

helix_edge = BRepBuilderAPI_MakeEdge(aSegment.Value(), aCylinder, 0.0, 6.0 * pi).Edge()

display = threejs_renderer.ThreejsRenderer()
display.DisplayShape(helix_edge, color=(1, 0, 0), line_width=1.)
display.render()
