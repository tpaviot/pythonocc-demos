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

"""The HelixGeom and HelixBRep packages, new in OCCT 8.0: build helices,
cylindrical or conical, approximated by BSpline curves. HelixGeom builds
the curves, HelixBRep a wire made of several sections of different
pitches."""

import math

from OCC.Core.BRepAdaptor import BRepAdaptor_CompCurve
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeEdge, BRepBuilderAPI_MakeWire
from OCC.Core.BRepCheck import BRepCheck_Analyzer
from OCC.Core.BRepOffsetAPI import BRepOffsetAPI_MakePipeShell
from OCC.Core.GC import GC_MakeCircle
from OCC.Core.GeomAbs import GeomAbs_C1
from OCC.Core.gp import gp_Ax2, gp_Ax3, gp_Dir, gp_Pnt, gp_Vec
from OCC.Core.HelixBRep import HelixBRep_BuilderHelix
from OCC.Core.HelixGeom import HelixGeom_BuilderHelix
from OCC.Core.TColStd import TColStd_Array1OfBoolean, TColStd_Array1OfReal
from OCC.Display.SimpleGui import init_display

display, start_display, add_menu, add_function_to_menu = init_display()


def make_array(*values):
    array = TColStd_Array1OfReal(1, len(values))
    for i, value in enumerate(values, start=1):
        array.SetValue(i, value)
    return array


# A spring with closed ends: 3 sections along the axis, of heights 3, 24
# and 3. The end sections have a pitch of 1.5, the middle one of 6
builder = HelixBRep_BuilderHelix()
heights = make_array(3.0, 24.0, 3.0)
pitches = make_array(1.5, 6.0, 1.5)
# the values of pitches are pitches, not numbers of turns
is_pitches = TColStd_Array1OfBoolean(1, 3)
for i in range(1, 4):
    is_pitches.SetValue(i, True)
builder.SetParameters(gp_Ax3(), 20.0, heights, pitches, is_pitches)
builder.SetApproxParameters(1e-4, 8, GeomAbs_C1)
builder.Perform()
assert builder.ErrorStatus() == 0
spring_wire = builder.Shape()
print(f"spring approximated with a tolerance of {builder.ToleranceReached():.2e}")
display.DisplayShape(spring_wire, color="RED")

# the spring solid: sweep a circle along the helix. The profile is in the
# plane normal to the helix at its start point
helix_curve = BRepAdaptor_CompCurve(spring_wire)
first_point = gp_Pnt()
first_tangent = gp_Vec()
helix_curve.D1(helix_curve.FirstParameter(), first_point, first_tangent)
profile = GC_MakeCircle(gp_Ax2(first_point, gp_Dir(first_tangent)), 0.8).Value()
profile_wire = BRepBuilderAPI_MakeWire(BRepBuilderAPI_MakeEdge(profile).Edge()).Wire()
pipe = BRepOffsetAPI_MakePipeShell(spring_wire)
pipe.SetMode(gp_Dir(0, 0, 1))  # the profile keeps its orientation to the axis
pipe.Add(profile_wire)
pipe.Build()
pipe.MakeSolid()
spring = pipe.Shape()
print(f"spring solid valid: {BRepCheck_Analyzer(spring).IsValid()}")
display.DisplayShape(spring, color="GREEN", transparency=0.3)

# A conical helix, with HelixGeom: 8 turns of pitch 4, from a radius of 10,
# the radius decreasing with a taper angle of -0.15 rad. HelixGeom builds
# the BSpline curves that approximate the helix, HelixBRep the edges
geom_builder = HelixGeom_BuilderHelix()
geom_builder.SetPosition(gp_Ax2(gp_Pnt(40, 0, 0), gp_Dir(0, 0, 1)))
geom_builder.SetCurveParameters(0.0, 8 * 2 * math.pi, 4.0, 10.0, -0.15, False)
geom_builder.SetTolerance(1e-4)
geom_builder.Perform()
assert geom_builder.ErrorStatus() == 0
curves = geom_builder.Curves()
print(f"conical helix approximated by {curves.Length()} BSpline curve(s)")
conical_wire = BRepBuilderAPI_MakeWire()
for curve in curves:
    conical_wire.Add(BRepBuilderAPI_MakeEdge(curve).Edge())
display.DisplayShape(conical_wire.Wire(), color="BLUE")

display.FitAll()
start_display()
