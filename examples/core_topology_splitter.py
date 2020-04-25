##Copyright 2009-2016 Thomas Paviot (tpaviot@gmail.com)
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

import sys

from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeEdge, BRepBuilderAPI_MakeFace
from OCC.Core.BOPAlgo import BOPAlgo_Splitter
from OCC.Core.TopAbs import TopAbs_EDGE
from OCC.Core.TopExp import TopExp_Explorer
from OCC.Core.gp import gp_Dir, gp_Pln, gp_Pnt

from OCC.Extend.TopologyUtils import TopologyExplorer
from OCC.Display.SimpleGui import init_display
display, start_display, add_menu, add_function_to_menu = init_display()


def split_face_with_edge(event=None):
    display.EraseAll()
    p0 = gp_Pnt()
    vnorm = gp_Dir(1, 0, 0)
    pln = gp_Pln(p0, vnorm)
    face = BRepBuilderAPI_MakeFace(pln, -10, 10, -10, 10).Face()
    p1 = gp_Pnt(0, 0, 15)
    p2 = gp_Pnt(0, 0, -15)
    edge = BRepBuilderAPI_MakeEdge(p1, p2).Edge()
    # Initialize splitter
    splitter = BOPAlgo_Splitter()
    # Add the face as an argument and the edge as a tool. This will split
    # the face with the edge.
    splitter.AddArgument(face)
    splitter.AddTool(edge)
    splitter.Perform()
    # resulting shapes
    faces = TopologyExplorer(splitter.Shape()).faces()
    for face in faces:
        display.DisplayShape(face)
    display.FitAll()


def split_edge_with_face(event=None):
    display.EraseAll()
    p0 = gp_Pnt()
    vnorm = gp_Dir(1, 0, 0)
    pln = gp_Pln(p0, vnorm)
    face = BRepBuilderAPI_MakeFace(pln, -10, 10, -10, 10).Face()
    p1 = gp_Pnt(0, 0, 15)
    p2 = gp_Pnt(0, 0, -15)
    edge = BRepBuilderAPI_MakeEdge(p1, p2).Edge()
    # Initialize splitter
    splitter = BOPAlgo_Splitter()
    # Add the edge as an argument and the face as a tool. This will split
    # the edge with the face.
    splitter.AddArgument(edge)
    splitter.AddTool(face)
    splitter.Perform()

    edges = []
    exp = TopExp_Explorer(splitter.Shape(), TopAbs_EDGE)
    while exp.More():
        edges.append(exp.Current())
        exp.Next()
    print('Number of edges in split shape: ', len(edges))
    display.DisplayShape(edges[0], color='red')
    display.DisplayShape(edges[1], color='green')
    display.DisplayShape(edges[2], color='yellow')
    display.FitAll()


def exit(event=None):
    sys.exit()


if __name__ == '__main__':
    add_menu('BOPAlgo Splitter Example')
    add_function_to_menu('BOPAlgo Splitter Example', split_face_with_edge)
    add_function_to_menu('BOPAlgo Splitter Example', split_edge_with_face)
    add_function_to_menu('BOPAlgo Splitter Example', exit)
    start_display()
