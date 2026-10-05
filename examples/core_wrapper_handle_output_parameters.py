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

"""Handle output parameters, since pythonocc-core 8.0.1.1.

Many OCCT functions return a handle through a non-const reference
parameter, e.g. TDocStd_Application::Open(path, Handle(TDocStd_Document)&).
In Python, None is passed for such a parameter and the handle is appended to
the returned values, like the other output parameters (numbers, strings):

- a void function with a single handle output returns the handle alone
- a void function with several outputs returns a tuple, in the order of the
  parameters
- a non-void function returns a tuple whose first item is the function result

Before 8.0.1.1, the handle replaced the function result and the other
outputs: TDocStd_Application.Open() returned the document and lost the
PCDM_ReaderStatus, BRep_Tool.CurveOnSurface() lost the pcurve. This is a
breaking change for the non-void functions with a handle output, their
result is now a tuple.
"""

import os
import tempfile

from OCC.Core.AIS import AIS_Line
from OCC.Core.BinDrivers import bindrivers
from OCC.Core.BRep import BRep_Tool
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeEdge, BRepBuilderAPI_MakeWire
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeBox
from OCC.Core.Geom import Geom_CartesianPoint
from OCC.Core.gp import gp_Pnt
from OCC.Core.PCDM import PCDM_ReaderStatus, PCDM_StoreStatus
from OCC.Core.ShapeAnalysis import ShapeAnalysis_FreeBounds
from OCC.Core.TDataStd import TDataStd_Name
from OCC.Core.TDocStd import TDocStd_Application
from OCC.Core.TopLoc import TopLoc_Location
from OCC.Core.TopTools import TopTools_HSequenceOfShape
from OCC.Core.UnitsAPI import unitsapi
from OCC.Extend.TopologyUtils import TopologyExplorer

# 1. A void function with several handle outputs: AIS_Line.Points fills the
# two Geom_Point handles, both are returned, in the parameter order
line = AIS_Line(
    Geom_CartesianPoint(gp_Pnt(0, 0, 0)), Geom_CartesianPoint(gp_Pnt(10, 20, 30))
)
p_start, p_end = line.Points(None, None)
assert p_start is not None and p_end is not None
print("AIS_Line.Points:")
print(f"  start {p_start.X()}, {p_start.Y()}, {p_start.Z()}")
print(f"  end   {p_end.X()}, {p_end.Y()}, {p_end.Z()}")

# 2. Handle outputs followed by number outputs: BRep_Tool.CurveOnSurface
# returns the pcurve, the surface, then the parameter range of the edge
box = BRepPrimAPI_MakeBox(10.0, 20.0, 30.0).Shape()
edge = next(TopologyExplorer(box).edges())
pcurve, surface, first, last = BRep_Tool.CurveOnSurface(
    edge, None, None, TopLoc_Location(), 1
)
print("BRep_Tool.CurveOnSurface:")
print(
    f"  pcurve {type(pcurve).__name__} on {type(surface).__name__}, [{first}, {last}]"
)

# 3. A non-void function: the function result comes first, then the handle.
# unitsapi.AnyToLS converts a value to the local unit system and fills the
# Units_Dimensions of the quantity
value, dimensions = unitsapi.AnyToLS(1.0, "in", None)
assert dimensions is not None
print("unitsapi.AnyToLS:")
print(f"  1 in = {value} m, dimensions: {dimensions.Quantity()}")

# 4. The breaking change: TDocStd_Application.Open returns [status, document]
# where it returned the document alone before 8.0.1.1. NewDocument is a void
# function with a single handle output, it returns the new document alone
app = TDocStd_Application()
bindrivers.DefineFormat(app)
doc = app.NewDocument("BinOcaf", None)
assert doc is not None
TDataStd_Name.Set(doc.Main(), "handle outputs demo")
with tempfile.TemporaryDirectory() as tmp:
    path = os.path.join(tmp, "demo.cbf")
    assert app.SaveAs(doc, path) == PCDM_StoreStatus.PCDM_SS_OK
    app.Close(doc)
    # before 8.0.1.1: doc2 = app.Open(path, None)
    open_status, doc2 = app.Open(path, None)
print("TDocStd_Application.Open:")
print(f"  status {PCDM_ReaderStatus(open_status).name}, document {type(doc2).__name__}")

# 5. Two sequence outputs: ShapeAnalysis_FreeBounds.SplitWires sorts the
# wires into the closed and the open sequences
wire_builder = BRepBuilderAPI_MakeWire()
for p1, p2 in (
    ((0, 0, 0), (10, 0, 0)),
    ((10, 0, 0), (10, 10, 0)),
    ((10, 10, 0), (0, 0, 0)),
):
    wire_builder.Add(BRepBuilderAPI_MakeEdge(gp_Pnt(*p1), gp_Pnt(*p2)).Edge())
wires = TopTools_HSequenceOfShape()
wires.Append(wire_builder.Wire())
wires.Append(
    BRepBuilderAPI_MakeWire(
        BRepBuilderAPI_MakeEdge(gp_Pnt(0, 0, 0), gp_Pnt(5, 5, 5)).Edge()
    ).Wire()
)
closed, opened = ShapeAnalysis_FreeBounds.SplitWires(wires, 1e-7, False, None, None)
assert closed is not None and opened is not None
print("ShapeAnalysis_FreeBounds.SplitWires:")
print(f"  {closed.Length()} closed wire(s), {opened.Length()} open wire(s)")
