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

"""The GeomGridEval package, new in OCCT 8.0: evaluate a curve or a surface
on a grid of parameters in a single call, instead of calling Value() for
each parameter. The result is an array, converted to a numpy array."""

import math
import time

import numpy as np
from OCC.Core.AIS import AIS_PointCloud
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeFace
from OCC.Core.Geom import Geom_ToroidalSurface
from OCC.Core.GeomGridEval import GeomGridEval_Surface
from OCC.Core.gp import gp_Ax3
from OCC.Core.Graphic3d import Graphic3d_ArrayOfPoints
from OCC.Core.TColStd import TColStd_Array1OfReal
from OCC.Display.SimpleGui import init_display

display, start_display, add_menu, add_function_to_menu = init_display()

torus = Geom_ToroidalSurface(gp_Ax3(), 10.0, 3.0)

# the parameters of the grid: 200 values in U, 100 in V
u_params = TColStd_Array1OfReal.from_numpy_array(np.linspace(0, 2 * math.pi, 200))
v_params = TColStd_Array1OfReal.from_numpy_array(np.linspace(0, 2 * math.pi, 100))

# the 20000 points of the grid in a single call
start = time.perf_counter()
evaluator = GeomGridEval_Surface(torus)
points = evaluator.EvaluateGrid(u_params, v_params).to_numpy_array()
grid_time = time.perf_counter() - start
print(f"grid of {points.shape[0]} x {points.shape[1]} points in {grid_time:.4f}s")

# the same points, one Value() call for each
start = time.perf_counter()
loop_points = np.array(
    [[torus.Value(u, v).Coord() for v in v_params] for u in u_params]
)
loop_time = time.perf_counter() - start
print(f"the same points with Value() in {loop_time:.4f}s")
print(f"max difference: {np.abs(points - loop_points).max():.2e}")

# the derivatives on the same grid, here the first derivative along U
d1u = evaluator.EvaluateGridDN(u_params, v_params, 1, 0).to_numpy_array()
print(f"norm of dS/du at (0, 0): {np.linalg.norm(d1u[0, 0]):.3f}")

# display the grid points as a point cloud, on top of the torus
point_array = Graphic3d_ArrayOfPoints(points.shape[0] * points.shape[1])
for x, y, z in points.reshape(-1, 3):
    point_array.AddVertex(float(x), float(y), float(z))
point_cloud = AIS_PointCloud()
point_cloud.SetPoints(point_array)
display.GetContext().Display(point_cloud, True)
display.DisplayShape(
    BRepBuilderAPI_MakeFace(torus, 1e-6).Face(), color="BLUE", transparency=0.7
)

display.FitAll()
start_display()
