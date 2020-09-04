##Copyright 2017 Thomas Paviot (tpaviot@gmail.com)
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

from OCC.Core.Tesselator import ShapeTesselator
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeBox

try:
    import numpy as np
    HAVE_NUMPY = True
except ImportError:
    HAVE_NUMPY = False

# create the shape
box_s = BRepPrimAPI_MakeBox(10, 20, 30).Shape()

# compute the tessellation
tess = ShapeTesselator(box_s)
tess.Compute()

# get vertices
vertices_position = tess.GetVerticesPositionAsTuple()

number_of_triangles = tess.ObjGetTriangleCount()
number_of_vertices = len(vertices_position)

# number of vertices should be a multiple of 3
if number_of_vertices % 3 != 0:
	raise AssertionError("wrong number of vertices returned by the teselator")
if number_of_triangles * 9 != number_of_vertices:
	raise AssertionError("wrong number of triangles returned by the teselator")

# get normals
normals = tess.GetNormalsAsTuple()
number_of_normals = len(normals)
if not number_of_normals == number_of_vertices:
	raise AssertionError("wrong number of normals returned by the tessellator")

# if HAVE_NUMPY, we try to reshape the tuple so that it is of
# a ndarray such as [[x1, y1, z1], [x2, y2, z2], ...]
#
if HAVE_NUMPY:
    vertices = np.array(vertices_position).reshape(int(number_of_vertices / 3), 3)
    normals = np.array(normals).reshape(int(number_of_vertices / 3), 3)
