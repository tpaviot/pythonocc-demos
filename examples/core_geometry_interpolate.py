##Copyright 2025 Thomas Paviot (tpaviot@gmail.com)
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

from OCC.Core.gp import gp_Pnt
from OCC.Core.BRep import BRep_Tool
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakePolygon
from OCC.Core.GeomAPI import GeomAPI_Interpolate
from OCC.Core.TColgp import TColgp_HArray1OfPnt

from OCC.Display.SimpleGui import init_display

from OCC.Extend.TopologyUtils import ordered_vertices_from_wire

# First create a polygonal wire
polygon = BRepBuilderAPI_MakePolygon()
polygon.Add(gp_Pnt(0, 0, 0))
polygon.Add(gp_Pnt(3, 1, 0))
polygon.Add(gp_Pnt(5, 4, 1))
polygon.Add(gp_Pnt(2, 6, 2))
polygon.Add(gp_Pnt(-1, 5, 1))
polygon.Add(gp_Pnt(-2, 2, 0))
polygon.Close()  # Close the polygon

# Get the polygon wire
polygon_wire = polygon.Wire()

vertices = list(ordered_vertices_from_wire(polygon_wire))

all_points_in_wire = TColgp_HArray1OfPnt(1, len(vertices) + 1)

for i, vertex in enumerate(vertices):
    the_pnt = BRep_Tool.Pnt(vertex)
    all_points_in_wire.SetValue(i + 1, the_pnt)

# Add the first one, again, to close the spline
all_points_in_wire.SetValue(len(vertices) + 1, all_points_in_wire.Value(1))
interpolator = GeomAPI_Interpolate(all_points_in_wire, False, 1e-6)
interpolator.Perform()  # this has to be explicitly called

# Display
display, start_display, add_menu, add_function_to_menu = init_display()
display.DisplayShape(interpolator.Curve())
display.DisplayShape(polygon_wire, color="BLUE", update=True)

start_display()
