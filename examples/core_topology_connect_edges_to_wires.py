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

"""ShapeAnalysis_FreeBounds.ConnectEdgesToWires: build wires from an
unordered bag of edges.

Edges imported from DXF/IGES or produced by a section often come without
any topological connection: each edge has its own vertices, in a random
order. ConnectEdgesToWires chains the edges whose end vertices are closer
than a tolerance and returns one wire per connected chain.

- shared=False: the vertices are compared geometrically, with `toler`
- shared=True: only the edges that really share their TopoDS_Vertex are
  connected, the tolerance is ignored
"""

import math
import random

from OCC.Core.BRep import BRep_Tool
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeEdge, BRepBuilderAPI_MakePolygon
from OCC.Core.GC import GC_MakeArcOfCircle
from OCC.Core.gp import gp_Pnt, gp_Trsf, gp_Vec
from OCC.Core.ShapeAnalysis import ShapeAnalysis_FreeBounds
from OCC.Core.TopLoc import TopLoc_Location
from OCC.Core.TopoDS import TopoDS_Edge, TopoDS_Wire, topods
from OCC.Core.TopTools import TopTools_HSequenceOfShape
from OCC.Display.SimpleGui import init_display
from OCC.Extend.TopologyUtils import TopologyExplorer

display, start_display, add_menu, add_function_to_menu = init_display()

COLORS = ["RED", "GREEN", "BLUE", "YELLOW", "CYAN", "ORANGE", "WHITE", "MAGENTA"]


def segment(p1: gp_Pnt, p2: gp_Pnt) -> TopoDS_Edge:
    """A straight edge with its own, unshared, vertices."""
    return BRepBuilderAPI_MakeEdge(p1, p2).Edge()


def arc(p1: gp_Pnt, p2: gp_Pnt, p3: gp_Pnt) -> TopoDS_Edge:
    """A circular arc through three points, with its own vertices."""
    return BRepBuilderAPI_MakeEdge(GC_MakeArcOfCircle(p1, p2, p3).Value()).Edge()


# 1. A rounded rectangle: 4 segments and 4 arcs, built independently
r = 10.0
w, h = 100.0, 60.0
rounded_rectangle = [
    segment(gp_Pnt(r, 0, 0), gp_Pnt(w - r, 0, 0)),
    arc(gp_Pnt(w - r, 0, 0), gp_Pnt(w - r * 0.2929, r * 0.2929, 0), gp_Pnt(w, r, 0)),
    segment(gp_Pnt(w, r, 0), gp_Pnt(w, h - r, 0)),
    arc(
        gp_Pnt(w, h - r, 0),
        gp_Pnt(w - r * 0.2929, h - r * 0.2929, 0),
        gp_Pnt(w - r, h, 0),
    ),
    segment(gp_Pnt(w - r, h, 0), gp_Pnt(r, h, 0)),
    arc(gp_Pnt(r, h, 0), gp_Pnt(r * 0.2929, h - r * 0.2929, 0), gp_Pnt(0, h - r, 0)),
    segment(gp_Pnt(0, h - r, 0), gp_Pnt(0, r, 0)),
    arc(gp_Pnt(0, r, 0), gp_Pnt(r * 0.2929, r * 0.2929, 0), gp_Pnt(r, 0, 0)),
]

# 2. A circle split in three arcs, inside the rectangle
center = gp_Pnt(w / 2, h / 2, 0)
radius = 18.0


def on_circle(angle_deg: float) -> gp_Pnt:
    a = math.radians(angle_deg)
    return gp_Pnt(
        center.X() + radius * math.cos(a), center.Y() + radius * math.sin(a), 0
    )


circle = [
    arc(on_circle(0), on_circle(60), on_circle(120)),
    arc(on_circle(120), on_circle(180), on_circle(240)),
    arc(on_circle(240), on_circle(300), on_circle(360)),
]

# 3. An open polyline, with a gap of 2 between the 2nd and the 3rd segment
gap = 2.0
polyline = [
    segment(gp_Pnt(0, 80, 0), gp_Pnt(30, 95, 0)),
    segment(gp_Pnt(30, 95, 0), gp_Pnt(60, 80, 0)),
    segment(gp_Pnt(60 + gap, 80, 0), gp_Pnt(90, 95, 0)),
    segment(gp_Pnt(90, 95, 0), gp_Pnt(120, 80, 0)),
]

# Shuffle everything into a single, unordered, sequence of edges
all_edges = rounded_rectangle + circle + polyline
random.Random(42).shuffle(all_edges)
edges = TopTools_HSequenceOfShape()
for edge in all_edges:
    edges.Append(edge)
print(f"{edges.Length()} unordered edges")


def describe(title: str, wires: TopTools_HSequenceOfShape) -> list[TopoDS_Wire]:
    """Prints a summary of each wire and returns them as a Python list."""
    print(f"\n{title}: {wires.Length()} wire(s)")
    result = []
    for i in range(1, wires.Length() + 1):
        wire = topods.Wire(wires.Value(i))
        nb_edges = TopologyExplorer(wire).number_of_edges()
        state = "closed" if BRep_Tool.IsClosed(wire) else "open"
        print(f"  wire {i}: {nb_edges} edge(s), {state}")
        result.append(wire)
    return result


# A tight tolerance: the gap of the polyline is not bridged, so 4 wires are
# expected: the rounded rectangle, the circle and two halves of the polyline
wires = describe(
    "shared=False, toler=1e-6",
    ShapeAnalysis_FreeBounds.ConnectEdgesToWires(edges, 1e-6, False),
)

# A tolerance larger than the gap: the polyline becomes a single open wire
describe(
    f"shared=False, toler={gap * 1.5}",
    ShapeAnalysis_FreeBounds.ConnectEdgesToWires(edges, gap * 1.5, False),
)

# shared=True: none of these edges share a vertex, each edge stays alone
describe(
    "shared=True, unshared vertices",
    ShapeAnalysis_FreeBounds.ConnectEdgesToWires(edges, 1e-6, True),
)

# shared=True on edges that do share their vertices (a polygon): one wire
polygon = BRepBuilderAPI_MakePolygon(
    gp_Pnt(0, -40, 0), gp_Pnt(50, -20, 0), gp_Pnt(100, -40, 0), gp_Pnt(50, -10, 0), True
).Wire()
polygon_edges = TopTools_HSequenceOfShape()
for edge in TopologyExplorer(polygon).edges():
    polygon_edges.Append(edge)
polygon_wires = describe(
    "shared=True, polygon with shared vertices",
    ShapeAnalysis_FreeBounds.ConnectEdgesToWires(polygon_edges, 1e-6, True),
)

# Display the unordered input edges in black, 40 below, and each wire
# of the first call in its own color
below = gp_Trsf()
below.SetTranslation(gp_Vec(0, 0, -40))
for edge in all_edges:
    display.DisplayShape(edge.Moved(TopLoc_Location(below)), color="BLACK")
for i, wire in enumerate(wires + polygon_wires):
    display.DisplayShape(wire, color=COLORS[i % len(COLORS)])
display.FitAll()

start_display()
