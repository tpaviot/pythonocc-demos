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

"""The Geom2dEval package, new in OCCT 8.0: analytic 2D curves (spirals,
involute, sine wave) that are not available as Geom2d classes. They are
Geom2d_Curve subclasses: they can be evaluated and used by the algorithms
working on adaptors. The curves are infinite, a parameter range is chosen
and the trimmed curve is converted to a BSpline, so that the edge can be
discretized and displayed like any other 2D curve."""

import math

from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeEdge2d
from OCC.Core.Geom2d import Geom2d_TrimmedCurve
from OCC.Core.Geom2dConvert import Geom2dConvert_ApproxCurve
from OCC.Core.Geom2dEval import (
    Geom2dEval_ArchimedeanSpiralCurve,
    Geom2dEval_CircleInvoluteCurve,
    Geom2dEval_LogarithmicSpiralCurve,
    Geom2dEval_SineWaveCurve,
)
from OCC.Core.GeomAbs import GeomAbs_C1
from OCC.Core.gp import gp_Ax2d, gp_Dir2d, gp_Pnt2d
from OCC.Display.SimpleGui import init_display

display, start_display, add_menu, add_function_to_menu = init_display()


def frame(x, y):
    """A local 2D coordinate system at (x, y)."""
    return gp_Ax2d(gp_Pnt2d(x, y), gp_Dir2d(1, 0))


def make_edge(curve, u1, u2, tolerance=1e-4):
    """Builds an edge in the XY plane on the (u1, u2) range of a 2D curve.

    The range is approximated by a C1 BSpline curve within tolerance.
    """
    approx = Geom2dConvert_ApproxCurve(
        Geom2d_TrimmedCurve(curve, u1, u2), tolerance, GeomAbs_C1, 64, 8
    )
    if not approx.IsDone():
        raise AssertionError("curve approximation failed")
    return BRepBuilderAPI_MakeEdge2d(approx.Curve()).Edge()


# An Archimedean spiral r = r0 + a * theta, here r0 = 1 and a = 2: the
# distance between two consecutive turns is 2 * pi * a. The parameter is the
# angle theta, 5 turns are displayed
archimedean = Geom2dEval_ArchimedeanSpiralCurve(frame(0, 0), 1.0, 2.0)
print(f"archimedean spiral at theta = pi: {archimedean.Value(math.pi).Coord()}")
display.DisplayShape(make_edge(archimedean, 0.0, 5 * 2 * math.pi), color="BLUE")

# A logarithmic spiral r = scale * exp(k * theta), self similar: each turn is
# exp(2 * pi * k) times larger than the previous one
logarithmic = Geom2dEval_LogarithmicSpiralCurve(frame(250, 0), 1.0, 0.15)
display.DisplayShape(make_edge(logarithmic, 0.0, 4.5 * 2 * math.pi), color="RED")

# The involute of a circle of radius 20, the profile of gear teeth: the curve
# traced by the end of a string unwound from the circle
involute = Geom2dEval_CircleInvoluteCurve(frame(0, 300), 20.0)
display.DisplayShape(make_edge(involute, 0.0, 2 * math.pi), color="GREEN")

# A sine wave of amplitude 10 and angular frequency 0.25, i.e. a period of
# 8 * pi, over three periods
sine = Geom2dEval_SineWaveCurve(frame(250, 300), 10.0, 0.25)
display.DisplayShape(make_edge(sine, 0.0, 24 * math.pi), color="ORANGE")

display.View_Top()
display.FitAll()
start_display()
