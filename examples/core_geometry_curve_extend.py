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

from OCC.Core.gp import gp_Pnt
from OCC.Core.GeomAPI import GeomAPI_Interpolate
from OCC.Core.TColgp import TColgp_HArray1OfPnt
from OCC.Core.GeomLib import geomlib

from OCC.Display.SimpleGui import init_display

display, start_display, add_menu, add_function_to_menu = init_display()
# a bspline from three points
points = TColgp_HArray1OfPnt(1, 3)
points.SetValue(1, gp_Pnt(0, 0, 0))
points.SetValue(2, gp_Pnt(1, 1, 0))
points.SetValue(3, gp_Pnt(2, 3, 4))

interpolator = GeomAPI_Interpolate(points, False, 1e-6)
interpolator.Perform()
curve_to_extend = interpolator.Curve()
# Display the curve
display.DisplayShape(curve_to_extend, color="BLUE")

# Extend the curve to another point
new_pnt = gp_Pnt(2.5, 6, -1)

# Display this new point
display.DisplayShape(new_pnt, color="RED")

# Extend the curve
CONTINUITY = 1  # degree of continuity 1, 2 or 3
AFTER = True  # insert the new point at the end of the curve

extended_curve = geomlib.ExtendCurveToPoint(curve_to_extend, new_pnt, CONTINUITY, AFTER)

display.DisplayShape(extended_curve, update=True)
start_display()
