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

"""The GeomEval package, new in OCCT 8.0: analytic 3D curves that are not
available as Geom classes. They are Geom_Curve subclasses, so they can be
evaluated, bounded to an edge, displayed or used in any algorithm."""

import math

from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeEdge
from OCC.Core.GCPnts import GCPnts_AbscissaPoint
from OCC.Core.GeomAdaptor import GeomAdaptor_Curve
from OCC.Core.GeomEval import (
    GeomEval_CircularHelixCurve,
    GeomEval_SineWaveCurve,
    GeomEval_TBezierCurve,
)
from OCC.Core.gp import gp_Ax2, gp_Dir, gp_Pnt
from OCC.Core.TColgp import TColgp_Array1OfPnt
from OCC.Display.SimpleGui import init_display

display, start_display, add_menu, add_function_to_menu = init_display()

# A circular helix of radius 10 around the Z axis, going up 5 per turn.
# The curve is infinite: an edge is built on a parameter range, here 4 turns
helix = GeomEval_CircularHelixCurve(gp_Ax2(gp_Pnt(0, 0, 0), gp_Dir(0, 0, 1)), 10.0, 5.0)
print(f"helix after one turn: {helix.Value(2 * math.pi).Coord()}")
helix_edge = BRepBuilderAPI_MakeEdge(helix, 0.0, 4 * 2 * math.pi).Edge()
helix_length = GCPnts_AbscissaPoint.Length(
    GeomAdaptor_Curve(helix, 0.0, 4 * 2 * math.pi)
)
print(f"helix length over 4 turns: {helix_length:.3f}")
display.DisplayShape(helix_edge, color="BLUE")

# A sine wave in the XY plane: amplitude 5, angular frequency 0.5, so a
# period of 4 * pi along X
sine = GeomEval_SineWaveCurve(gp_Ax2(gp_Pnt(30, 0, 0), gp_Dir(0, 0, 1)), 5.0, 0.5)
sine_edge = BRepBuilderAPI_MakeEdge(sine, 0.0, 8 * math.pi).Edge()
display.DisplayShape(sine_edge, color="RED")

# A trigonometric Bezier curve (T-Bezier): a trigonometric series whose
# coefficients are the poles, C(t) = P0 + P1 sin(a t) + P2 cos(a t)
# + P3 sin(2 a t) + P4 cos(2 a t) + ... on the parameter domain [0, pi / a].
# The poles are not interpolated nor approximated, unlike a Bezier curve:
# P0 is the center, the other poles the amplitudes of the harmonics
poles = TColgp_Array1OfPnt(1, 5)
for i, pnt in enumerate(
    (
        gp_Pnt(60, 40, 0),  # center
        gp_Pnt(20, 0, 0),  # sin(a t)
        gp_Pnt(0, 20, 0),  # cos(a t)
        gp_Pnt(0, 0, 8),  # sin(2 a t)
        gp_Pnt(5, 5, 0),  # cos(2 a t)
    ),
    start=1,
):
    poles.SetValue(i, pnt)
tbezier = GeomEval_TBezierCurve(poles, 1.0)
print(
    f"T-Bezier parameter domain: [{tbezier.FirstParameter()}, {tbezier.LastParameter()}]"
)
tbezier_edge = BRepBuilderAPI_MakeEdge(
    tbezier, tbezier.FirstParameter(), tbezier.LastParameter()
).Edge()
display.DisplayShape(tbezier_edge, color="GREEN")
display.DisplayShape(poles.Value(1), color="GREEN")

display.FitAll()
start_display()
