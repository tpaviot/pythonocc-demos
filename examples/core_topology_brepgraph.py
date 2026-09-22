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

"""The BRepGraph package, new in OCCT 8.0: a graph based representation of
the topology and geometry, an alternative to the TopoDS_Shape data
structure. Shapes are added to a graph, whose nodes (solids, shells, faces,
wires, edges, vertices) are addressed by typed, 0-based, contiguous ids;
the geometry is read through the graph and a TopoDS_Shape can be
reconstructed from any node."""

from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeVertex
from OCC.Core.BRepGraph import (
    BRepGraph_EdgeId,
    BRepGraph_FaceId,
    BRepGraph_Tool_Face,
    BRepGraph_Tool_Vertex,
    BRepGraph_Validate,
    BRepGraph_VertexId,
    brepgraph,
)
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeBox, BRepPrimAPI_MakeCylinder
from OCC.Display.SimpleGui import init_display

display, start_display, add_menu, add_function_to_menu = init_display()

# A graph is built from TopoDS shapes. Shapes().Add returns the root node
# of the shape in the graph, here a solid node
graph = brepgraph()
box = BRepPrimAPI_MakeBox(60.0, 40.0, 20.0).Shape()
cylinder = BRepPrimAPI_MakeCylinder(15.0, 50.0).Shape()
box_result = graph.Shapes().Add(box)
cylinder_result = graph.Shapes().Add(cylinder)
print(
    f"box added: {box_result.IsOk()}, root node kind {box_result.TopologyRoot.NodeKind}"
)

# The Topo view counts the nodes of each kind, whatever the shape they
# come from: the two solids share the same tables
topo = graph.Topo()
for name, ops in (
    ("solids", topo.Solids()),
    ("shells", topo.Shells()),
    ("faces", topo.Faces()),
    ("wires", topo.Wires()),
    ("edges", topo.Edges()),
    ("vertices", topo.Vertices()),
):
    print(f"{name}: {ops.Nb()}")

# The geometry is read from the graph through typed ids, here the surface
# of every face and the number of faces around every edge
surface_types: dict[str, int] = {}
for index in range(topo.Faces().Nb()):
    face_id = BRepGraph_FaceId(index)
    surface_type = topo.Faces().Surface(face_id).DynamicType().Name()
    surface_types[surface_type] = surface_types.get(surface_type, 0) + 1
print(f"surfaces: {surface_types}")
umin, umax, vmin, vmax = BRepGraph_Tool_Face.Bounds(graph, BRepGraph_FaceId(0))
# the underlying surface is a plane, it is not bounded
print(f"surface bounds of the first face: u in [{umin}, {umax}], v in [{vmin}, {vmax}]")
manifold_edges = sum(
    topo.Edges().NbFaces(BRepGraph_EdgeId(index)) == 2
    for index in range(topo.Edges().Nb())
)
print(f"manifold edges: {manifold_edges} / {topo.Edges().Nb()}")

# The structural validation of the graph
validation = BRepGraph_Validate.Perform(graph)
print(f"graph valid: {validation.IsValid()}")

# A node is found back from its construction shape, and a TopoDS_Shape is
# reconstructed from a node: the two boxes are equivalent but not the same
# object
node = graph.Shapes().FindNode(box)
rebuilt_box = graph.Shapes().Reconstruct(node)
print(f"reconstructed box is the original one: {rebuilt_box.IsSame(box)}")
display.DisplayShape(rebuilt_box, color="BLUE", transparency=0.5)
display.DisplayShape(
    graph.Shapes().Shape(cylinder_result.TopologyRoot), color="ORANGE", transparency=0.5
)

# the vertices of the graph, read through BRepGraph_Tool
for index in range(topo.Vertices().Nb()):
    point = BRepGraph_Tool_Vertex.Pnt(graph, BRepGraph_VertexId(index))
    display.DisplayShape(BRepBuilderAPI_MakeVertex(point).Vertex(), color="RED")

display.FitAll()
start_display()
