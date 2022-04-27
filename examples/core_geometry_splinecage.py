#!/usr/bin/env python

# #Copyright 2009-2011 Jelle Feringa (jelleferinga@gmail.com)
# #
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

# TODO:
# * need examples where the tangency to constraining faces is respected

import random

from OCC.Core.BRepAdaptor import BRepAdaptor_Curve
from OCC.Core.GCPnts import GCPnts_AbscissaPoint, GCPnts_UniformAbscissa
from OCC.Core.GeomAbs import GeomAbs_G1
from OCC.Core.BRepOffsetAPI import BRepOffsetAPI_MakeFilling
from OCC.Core.TopAbs import TopAbs_FACE, TopAbs_EDGE

from OCC.Display.SimpleGui import init_display
from OCC.Display.OCCViewer import rgb_color
from OCC.Extend.TopologyUtils import TopologyExplorer
from OCC.Extend.DataExchange import read_step_file

display, start_display, add_menu, add_function_to_menu = init_display()


def random_color():
    return rgb_color(random.random(), random.random(), random.random())


def length_from_edge(edg):
    curve_adapt = BRepAdaptor_Curve(edg)
    length = GCPnts_AbscissaPoint().Length(
        curve_adapt, curve_adapt.FirstParameter(), curve_adapt.LastParameter(), 1e-6
    )
    return length


def divide_edge_by_nr_of_points(edg, n_pts):
    """returns a nested list of parameters and points on the edge
    at the requested interval [(param, gp_Pnt),...]
    """
    curve_adapt = BRepAdaptor_Curve(edg)
    _lbound, _ubound = curve_adapt.FirstParameter(), curve_adapt.LastParameter()

    if n_pts <= 1:
        # minimally two points or a Standard_ConstructionError is raised
        raise AssertionError("minimally 2 points required")

    npts = GCPnts_UniformAbscissa(curve_adapt, n_pts, _lbound, _ubound)
    if npts.IsDone():
        tmp = []
        for i in range(1, npts.NbPoints() + 1):
            param = npts.Parameter(i)
            pnt = curve_adapt.Value(param)
            tmp.append((param, pnt))
        return tmp


def hash_edge_length_to_face(faces):
    """
    for every edge in the list `faces`

        loop through the edges of the face
        associate (hash) the edge length to point to the face


    :note: this approach would blow less if you use a tuple ( length, edge-mid-point )

    the TopoDS_Edge entity has a HashCode method
    that might be actually a proper idea

    :param faces:
    :return: dict hashing all edge lengths
    """
    _edge_length_to_face = {}
    _edge_length_to_edge = {}

    for f in faces:
        tp = TopologyExplorer(f)
        for e in tp.edges():
            length = round(length_from_edge(e), 3)
            _edge_length_to_face[length] = f
            _edge_length_to_edge[length] = e

    return _edge_length_to_face, _edge_length_to_edge


def build_curve_network(event=None, enforce_tangency=True):
    """
    mimic the curve network surfacing command from rhino
    """
    root_compound_shape = read_step_file("../assets/models/splinecage.stp")
    topology_explorer = TopologyExplorer(root_compound_shape)

    tangent_constraint_faces = [f for f in topology_explorer.faces()]

    # loop through the imported faces
    # associate the length of each of the faces edges to the corresponding face
    _edge_length_to_face, _edge_length_to_edge = hash_edge_length_to_face(
        tangent_constraint_faces
    )

    # loop through the imported curves, avoiding the imported faces
    # when we've got these filtered out, we retrieved the geometry to build the surface from
    filtered_edges = [
        e
        for e in topology_explorer._loop_topo(
            TopAbs_EDGE, root_compound_shape, TopAbs_FACE
        )
    ]

    filtered_length = {}
    for e in filtered_edges:
        l = round(length_from_edge(e), 3)
        filtered_length[l] = e

    input_edge_face_pairs, edges_no_adjacent_face = [], []
    for l, edg in filtered_length.items():
        if l in _edge_length_to_edge:
            edge_face_pair = [_edge_length_to_edge[l], _edge_length_to_face[l]]
            input_edge_face_pairs.append(edge_face_pair)
        else:
            edges_no_adjacent_face.append(edg)

    brep_plate_builder = BRepOffsetAPI_MakeFilling()

    if enforce_tangency:
        print("going for surface quality...")
        brep_plate_builder.SetConstrParam(
            0.0001, 0.001, 0.01, 0.01
        )  # Tol2d=1.0, Tol3d=1.0, TolAng=1.0, TolCurv=1.0
        brep_plate_builder.SetApproxParam(8, 240)  # MaxDeg=8, MaxSegments=9
        print("done.")
    else:
        print("quick and dirty")

    # illegal instruction 4???
    for i in input_edge_face_pairs:
        display.DisplayShape(i, color=random_color())
        constraint_edg, support_face = i
        if constraint_edg.IsNull() or support_face.IsNull():
            print("Edge of face is null")
        brep_plate_builder.Add(constraint_edg, support_face, GeomAbs_G1)

    for e in edges_no_adjacent_face:
        display.DisplayShape(e)
        for pt in divide_edge_by_nr_of_points(e, 12)[2:-2]:
            brep_plate_builder.Add(pt[1])

    brep_plate_builder.Build()

    if brep_plate_builder.IsDone():
        face = brep_plate_builder.Shape()
        display.DisplayColoredShape(face, "ORANGE")
    else:
        print("constructing the surface failed")


if __name__ == "__main__":
    build_curve_network()
    display.FitAll()
    start_display()
