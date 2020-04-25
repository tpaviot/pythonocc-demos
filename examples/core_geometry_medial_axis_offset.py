#!/usr/bin/env python

##Copyright 2009-2016 Jelle Feringa (jelleferinga@gmail.com)
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

# this example was ported from: http://heekscnc.blogspot.nl/2009/09/occ-offset.html, by Dan Heeks

from OCC.Core.BRepOffsetAPI import BRepOffsetAPI_MakeOffset
from OCC.Display.SimpleGui import init_display
from OCC.Core.GeomAbs import GeomAbs_Arc
from OCC.Core.gp import gp_Pnt
from OCC.Extend.ShapeFactory import make_edge, make_vertex, make_wire, make_face
from OCC.Extend.TopologyUtils import TopologyExplorer

display, start_display, add_menu, add_function_to_menu = init_display()


def boolean_cut(shapeToCutFrom, cuttingShape):
    from OCC.Core.BRepAlgoAPI import BRepAlgoAPI_Cut
    cut = BRepAlgoAPI_Cut(shapeToCutFrom, cuttingShape)

    shp = cut.Shape()
    return shp


def make_face_to_contour_from():
    v1 = make_vertex(gp_Pnt(0, 0, 0))
    v2 = make_vertex(gp_Pnt(10, 0, 0))
    v3 = make_vertex(gp_Pnt(7, 10, 0))
    v4 = make_vertex(gp_Pnt(10, 20, 0))
    v5 = make_vertex(gp_Pnt(0, 20, 0))
    v6 = make_vertex(gp_Pnt(3, 10, 0))
    e1 = make_edge(v1, v2)
    e2 = make_edge(v2, v3)
    e3 = make_edge(v3, v4)
    e4 = make_edge(v4, v5)
    e5 = make_edge(v5, v6)
    e6 = make_edge(v6, v1)
    v7 = make_vertex(gp_Pnt(2, 2, 0))
    v8 = make_vertex(gp_Pnt(8, 2, 0))
    v9 = make_vertex(gp_Pnt(7, 3, 0))
    v10 = make_vertex(gp_Pnt(3, 3, 0))
    e7 = make_edge(v7, v8)
    e8 = make_edge(v8, v9)
    e9 = make_edge(v9, v10)
    e10 = make_edge(v10, v7)
    w1 = make_wire([e1, e2, e3, e4, e5, e6])
    f = make_face(w1)
    w2 = make_wire(e7, e8, e9, e10)
    f2 = make_face(w2)
    f3 = boolean_cut(f, f2)
    return f3


def create_offsets(face, nr_of_counters, distance_between_contours):
    offset = BRepOffsetAPI_MakeOffset()
    offset.Init(GeomAbs_Arc)

    for wi in TopologyExplorer(face).wires():
        offset.AddWire(wi)

    for i in range(nr_of_counters):
        offset.Perform(-distance_between_contours * i)
        if offset.IsDone():
            yield offset.Shape()


face = make_face_to_contour_from()
display.DisplayShape(face)

for contour in create_offsets(face, 50, 0.12):
    display.DisplayShape(contour)

display.FitAll()
start_display()
