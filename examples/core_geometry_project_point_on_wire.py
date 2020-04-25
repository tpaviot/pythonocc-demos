#!/usr/bin/env python

##Copyright 2019 Thomas Paviot (tpaviot@gmail.com)
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

from __future__ import print_function

import os

from OCC.Core.BRep import BRep_Builder
from OCC.Core.BRepTools import breptools
from OCC.Core.BRepAdaptor import BRepAdaptor_CompCurve, BRepAdaptor_HCompCurve
from OCC.Core.ShapeAnalysis import ShapeAnalysis_Curve
from OCC.Core.TopoDS import TopoDS_Shape, topods
from OCC.Core.gp import gp_Pnt
from OCC.Core.Approx import Approx_Curve3d
from OCC.Core.GeomAbs import GeomAbs_C2
from OCC.Core.GeomAPI import GeomAPI_ProjectPointOnCurve

# Read wire
wire_filename = os.path.join('..', 'assets', 'models', 'wire.brep')
shp = TopoDS_Shape()
aBuilder = BRep_Builder()
breptools.Read(shp, wire_filename, aBuilder)
wire = topods.Wire(shp)
if wire.IsNull():
    raise AssertionError("Wire is Null")

# discretize the wire and interpolate using a C2
wireAdaptor = BRepAdaptor_CompCurve(wire)
curve = BRepAdaptor_HCompCurve(wireAdaptor)
tol = 1e-7
max_segments = 200
max_degrees = 12
approx = Approx_Curve3d(curve, tol, GeomAbs_C2, max_segments, max_degrees)
if (approx.IsDone() and approx.HasResult()):
    an_approximated_curve = approx.Curve()

# there are two ways to project a point on this curve,
# they both give the same restult

# 1st solution: using GeomAPI_ProjectPointOnCurve
point_to_project = gp_Pnt(1., 2., 3.)
projection = GeomAPI_ProjectPointOnCurve(point_to_project, an_approximated_curve)
# get the results of the projection
projected_point = projection.NearestPoint()
# the number of possible results
nb_results = projection.NbPoints()
print("NbResults : %i" % nb_results)
print("Distance :", projection.LowerDistance())

# 2nd solution : using ShapeAnalysis_Curve().Project
tolerance = 1e-7
proj = gp_Pnt()
distance, parameter = ShapeAnalysis_Curve().Project(an_approximated_curve,
                                                    point_to_project, tolerance, proj)
print("Distance :", distance)
