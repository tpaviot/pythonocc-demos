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

"""Linear algebra with the math package: fit the plane z = a.x + b.y + c
through noisy points, by solving the normal equations (At.A).X = At.Z of
the least squares problem with a Gauss decomposition.

The elements of math_Vector and math_Matrix are set and read with
SetValue/GetValue, with OCCT indices (from Lower() to Upper()). math_Vector
also supports the python sequence protocol, with 0-based indices:
v[0], v[1] = value, len(v), list(v)."""

import random

from OCC.Core.BRep import BRep_Builder
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeFace, BRepBuilderAPI_MakeVertex
from OCC.Core.gp import gp_Dir, gp_Pln, gp_Pnt
from OCC.Core.math import math_Gauss, math_Matrix, math_Vector
from OCC.Core.TopoDS import TopoDS_Compound
from OCC.Display.SimpleGui import init_display

display, start_display, add_menu, add_function_to_menu = init_display()

# points close to the plane z = 0.2.x - 0.1.y + 3
random.seed(0)
points = []
for _ in range(50):
    x, y = random.uniform(-10, 10), random.uniform(-10, 10)
    z = 0.2 * x - 0.1 * y + 3 + random.gauss(0, 0.1)
    points.append((x, y, z))

# normal equations: (At.A) is a 3x3 matrix, At.Z a vector of 3 values
ata = math_Matrix(1, 3, 1, 3, 0.0)
atz = math_Vector(1, 3, 0.0)
for x, y, z in points:
    row = (x, y, 1.0)
    for i in range(3):
        for j in range(3):
            ata.SetValue(i + 1, j + 1, ata.GetValue(i + 1, j + 1) + row[i] * row[j])
        atz[i] += row[i] * z  # 0-based python indexing of the math_Vector

solution = math_Vector(1, 3, 0.0)
gauss = math_Gauss(ata)
gauss.Solve(atz, solution)
a, b, c = list(solution)
print(f"fitted plane: z = {a:.3f}.x + {b:.3f}.y + {c:.3f}")
print(
    f"solution vector: Lower() = {solution.Lower()}, Value(1) = {solution.Value(1):.3f}"
)

# display the points and the fitted plane: normal (-a, -b, 1) through (0, 0, c)
vertices = TopoDS_Compound()
builder = BRep_Builder()
builder.MakeCompound(vertices)
for x, y, z in points:
    builder.Add(vertices, BRepBuilderAPI_MakeVertex(gp_Pnt(x, y, z)).Vertex())
display.DisplayShape(vertices)
plane = gp_Pln(gp_Pnt(0, 0, c), gp_Dir(-a, -b, 1))
face = BRepBuilderAPI_MakeFace(plane, -12, 12, -12, 12).Face()
display.DisplayShape(face, color="BLUE", transparency=0.6, update=True)
start_display()
