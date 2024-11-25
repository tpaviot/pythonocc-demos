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

# Create array of 3 control points (poles), indexed from 1 to 3
poles = TColgp_Array1OfPnt(1, 3)

# Define control points forming an arc-like shape
poles.SetValue(1, gp_Pnt(0, 0, 0))  # Start point (0,0,0)
poles.SetValue(2, gp_Pnt(1, 1, 0))  # Middle point (1,1,0)
poles.SetValue(3, gp_Pnt(2, 0, 0))  # End point (2,0,0)

# Define weights for rational B-spline (NURBS)
weights = TColStd_Array1OfReal(1, 3)
weights.SetValue(1, 1.0)  # Normal weight for start point
weights.SetValue(2, 2.0)  # Double weight for middle point - pulls curve closer
weights.SetValue(3, 1.0)  # Normal weight for end point

# Define knot vector [0,1] with 2 knots
knots = TColStd_Array1OfReal(1, 2)
knots.SetValue(1, 0)  # Start parameter
knots.SetValue(2, 1)  # End parameter

# Define multiplicities for knots
multiplicities = TColStd_Array1OfInteger(1, 2)
multiplicities.SetValue(1, 3)  # Triple multiplicity at start (degree+1)
multiplicities.SetValue(2, 3)  # Triple multiplicity at end (degree+1)

# Create quadratic (degree=2) rational B-spline curve
degree = 2
periodic = False
check_rational = True
curve = Geom_BSplineCurve(
    poles, weights, knots, multiplicities, degree, periodic, check_rational
)

# Display the curve
display.DisplayShape(curve, update=True)

# Display poles
for p in poles:
    display.DisplayShape(BRepBuilderAPI_MakeVertex(p).Vertex())
start_display()
