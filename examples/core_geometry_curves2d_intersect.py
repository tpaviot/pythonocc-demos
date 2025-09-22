#!/usr/bin/env python

##Copyright 2025 Thomas paviot (tpaviot@gmail.com)
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

from OCC.Core.gp import gp_Pnt2d, gp_Dir2d, gp_Circ2d, gp_Ax2d
from OCC.Core.Geom2dAPI import Geom2dAPI_InterCurveCurve
from OCC.Core.Geom2d import Geom2d_Circle

# two 2d circles that intersect at two points
circle_1 = Geom2d_Circle(gp_Circ2d(gp_Ax2d(gp_Pnt2d(0, 0), gp_Dir2d(1, 0)), 10))
circle_2 = Geom2d_Circle(gp_Circ2d(gp_Ax2d(gp_Pnt2d(10, 0), gp_Dir2d(1, 0)), 12))

intersector = Geom2dAPI_InterCurveCurve(circle_1, circle_2)
print(dir(intersector))
nb_segments = intersector.NbSegments()
print(f"Number of segments: {nb_segments}")

nb_points = intersector.NbPoints()
print(f"Number of points: {nb_points}")

p_1 = intersector.Point(1)
p_2 = intersector.Point(2)
print(f"Point 1 coordinates: ({p_1.X()}, {p_1.Y()})")
print(f"Point 1 coordinates: ({p_2.X()}, {p_2.Y()})")

# Note : expected x 14/5 and y to be +-48/5
