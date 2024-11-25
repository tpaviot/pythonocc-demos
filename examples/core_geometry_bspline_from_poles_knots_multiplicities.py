#!/usr/bin/env python

##Copyright 2024 Thomas Paviot (tpaviot@gmail.com)
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

from OCC.Core.gp import gp_Pnt
from OCC.Core.TColgp import TColgp_Array1OfPnt
from OCC.Core.TColStd import TColStd_Array1OfReal, TColStd_Array1OfInteger
from OCC.Core.Geom import Geom_BSplineCurve
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeVertex

from OCC.Display.SimpleGui import init_display


# Initialize the display
display, start_display, add_menu, add_function_to_menu = init_display()

# Define curve degree (cubic B-spline)
degree = 3

# Define control points in 3D space
points = [
    gp_Pnt(0, 0, 1),  # Start point
    gp_Pnt(1, 2, 0),  # First control point
    gp_Pnt(2, -1, -1),  # Second control point
    gp_Pnt(3, 1, 2),  # Third control point
    gp_Pnt(4, -2, 3),  # Fourth control point
    gp_Pnt(5, 0, -4),  # End point
]

# Convert points list to OCC array structure (indices start at 1 in OCC)
poles = TColgp_Array1OfPnt(1, len(points))
for i, point in enumerate(points, 1):
    poles.SetValue(i, point)

# Define knot vector (parameter values where the curve segments join)
knot_values = [0, 0.3, 0.7, 1]  # Normalized parameter range [0,1]
knots = TColStd_Array1OfReal(1, len(knot_values))
for i, k in enumerate(knot_values, 1):
    knots.SetValue(i, k)

# Define multiplicities (affecting curve continuity at knots)
# 4 at ends (degree+1) ensures curve passes through end points
# 1 for interior knots gives maximum continuity
mult_values = [4, 1, 1, 4]
multiplicities = TColStd_Array1OfInteger(1, len(mult_values))
for i, m in enumerate(mult_values, 1):
    multiplicities.SetValue(i, m)

# Create B-spline curve from poles, knots, multiplicities and degree
bspline_curve = Geom_BSplineCurve(poles, knots, multiplicities, degree)

# Display the curve
display.DisplayShape(bspline_curve, update=True)

# Display poles
for p in points:
    display.DisplayShape(BRepBuilderAPI_MakeVertex(p).Vertex())
start_display()
