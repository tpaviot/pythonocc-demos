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

"""The GeomEval package, new in OCCT 8.0: analytic quadrics and helicoid
surfaces that are not available as Geom classes. They are Geom_Surface
subclasses: they can be evaluated (Value, D1, D2, normals...) and used by
the algorithms working on adaptors. They do not provide iso curves, so a
face cannot be built on them directly: the surfaces are displayed through
a BSpline approximation of the trimmed patch."""

import math

from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeFace
from OCC.Core.Geom import Geom_RectangularTrimmedSurface
from OCC.Core.GeomAbs import GeomAbs_C1
from OCC.Core.GeomConvert import GeomConvert_ApproxSurface
from OCC.Core.GeomEval import (
    GeomEval_CircularHelicoidSurface,
    GeomEval_EllipsoidSurface,
    GeomEval_HyperboloidSurface,
    GeomEval_HypParaboloidSurface,
    GeomEval_ParaboloidSurface,
)
from OCC.Core.GeomLProp import GeomLProp_SLProps
from OCC.Core.gp import gp_Ax3, gp_Dir, gp_Pnt
from OCC.Display.SimpleGui import init_display

display, start_display, add_menu, add_function_to_menu = init_display()

TOLERANCE = 1e-6


def frame(x):
    """A local coordinate system at (x, 0, 0), Z up."""
    return gp_Ax3(gp_Pnt(x, 0, 0), gp_Dir(0, 0, 1))


def make_face(surface, u1, u2, v1, v2, tolerance=1e-4):
    """Builds a face on the (u1, u2) x (v1, v2) patch of a GeomEval surface.

    The patch is approximated by a C1 BSpline surface within tolerance.
    """
    patch = Geom_RectangularTrimmedSurface(surface, u1, u2, v1, v2)
    approx = GeomConvert_ApproxSurface(
        patch, tolerance, GeomAbs_C1, GeomAbs_C1, 8, 8, 64, 1
    )
    if not approx.IsDone():
        raise AssertionError("surface approximation failed")
    return BRepBuilderAPI_MakeFace(approx.Surface(), TOLERANCE).Face()


# An ellipsoid with semi-axes 10, 6 and 4, a closed surface: its natural
# bounds are used to build the face
ellipsoid = GeomEval_EllipsoidSurface(frame(0), 10.0, 6.0, 4.0)
print(f"ellipsoid bounds (u1, u2, v1, v2): {ellipsoid.Bounds()}")
print(f"ellipsoid point at u = 0, v = 0: {ellipsoid.Value(0.0, 0.0).Coord()}")
# the local properties of the surface are available, like on any Geom_Surface
props = GeomLProp_SLProps(ellipsoid, 0.3, 0.4, 2, 1e-6)
props.IsCurvatureDefined()
print(f"ellipsoid gaussian curvature at (0.3, 0.4): {props.GaussianCurvature():.5f}")
display.DisplayShape(make_face(ellipsoid, *ellipsoid.Bounds()), color="BLUE")

# A paraboloid of focal distance 2, infinite: trimmed at v = 8
paraboloid = GeomEval_ParaboloidSurface(frame(30), 2.0)
display.DisplayShape(make_face(paraboloid, 0.0, 2 * math.pi, 0.0, 8.0), color="RED")

# Hyperboloids of one sheet and of two sheets, semi-axes 5 and 5
one_sheet = GeomEval_HyperboloidSurface(frame(60), 5.0, 5.0)
display.DisplayShape(make_face(one_sheet, 0.0, 2 * math.pi, -1.5, 1.5), color="GREEN")
two_sheets = GeomEval_HyperboloidSurface(
    frame(90), 5.0, 5.0, GeomEval_HyperboloidSurface.SheetMode.TwoSheets
)
print(f"hyperboloid mode: {two_sheets.Mode()}")
display.DisplayShape(make_face(two_sheets, 0.0, 2 * math.pi, 0.0, 1.5), color="ORANGE")

# A hyperbolic paraboloid (saddle) z = x^2 / a^2 - y^2 / b^2
saddle = GeomEval_HypParaboloidSurface(frame(120), 4.0, 4.0)
display.DisplayShape(make_face(saddle, -8.0, 8.0, -8.0, 8.0), color="CYAN")

# A circular helicoid of pitch 6, one turn, radius 8
helicoid = GeomEval_CircularHelicoidSurface(frame(150), 6.0)
display.DisplayShape(make_face(helicoid, 0.0, 2 * math.pi, -8.0, 8.0), color="YELLOW")

display.FitAll()
start_display()
