##Copyright 2020 Thomas Paviot (tpaviot@gmail.com)
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

from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeTorus
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_NurbsConvert
from OCC.Core.BRepAdaptor import BRepAdaptor_Surface

from OCC.Extend.TopologyUtils import TopologyExplorer
from OCC.Core.GeomAbs import GeomAbs_BSplineSurface

base_shape = BRepPrimAPI_MakeTorus(30, 10).Shape()

# conversion to a nurbs representation
nurbs_converter = BRepBuilderAPI_NurbsConvert(base_shape, True)
# nurbs_converter.Perform()
converted_shape = nurbs_converter.Shape()

# now, all edges should be BSpline curves and surfaces BSpline surfaces
# see https://www.opencascade.com/doc/occt-7.4.0/refman/html/class_b_rep_builder_a_p_i___nurbs_convert.html#details

expl = TopologyExplorer(converted_shape)

for fc_idx, face in enumerate(expl.faces(), start=1):
    print("=== Face %i ===" % fc_idx)
    surf = BRepAdaptor_Surface(face, True)
    surf_type = surf.GetType()
    # check each of the is a BSpline surface
    # it should be, since we used the nurbs converter before
    if surf_type != GeomAbs_BSplineSurface:
        raise AssertionError("the face was not converted to a GeomAbs_BSplineSurface")
    # get the nurbs
    bsrf = surf.BSpline()
    print("UDegree:", bsrf.UDegree())
    print("VDegree:", bsrf.VDegree())
    # uknots array
    uknots = bsrf.UKnots()
    print("Uknots:", end="")
    for i in range(bsrf.NbUKnots()):
        print(uknots.Value(i + 1), end=" ")
    # vknots array
    vknots = bsrf.VKnots()
    print("\nVknots:", end="")
    for i in range(bsrf.NbVKnots()):
        print(vknots.Value(i + 1), end=" ")
    print("\n")
    # weights, a 2d array
    weights = bsrf.Weights()
    # weights can be None
    if weights is not None:
        print("Weights:", end="")
        for i in range(bsrf.NbUKnots()):
            for j in range(bsrf.NbVKnots()):
                print(weights.Value(i + 1, j + 1), end=" ")
    # control points (aka poles), as a 2d array
    poles = bsrf.Poles()
    # weights can be None
    if poles is not None:
        print("Poles (control points):", end="")
        for i in range(bsrf.NbUPoles()):
            for j in range(bsrf.NbVPoles()):
                p = poles.Value(i + 1, j + 1)
                print(p.X(), p.Y(), p.Z(), end=" ")
    print()
