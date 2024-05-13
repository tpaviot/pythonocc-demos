##Copyright 2021 Thomas Paviot (tpaviot@gmail.com)
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

from OCC.Core.MeshDS import MeshDS_DataSource
from OCC.Core.MeshVS import *

from OCC.Display.SimpleGui import init_display

import numpy as np

# create data
v1 = [0, 0, 0]
v2 = [0, 1, 0]
v3 = [1, 1, 0]
v4 = [1, 0, 0]
v5 = [0, 0, 1]
v6 = [0, 1, 1]
v7 = [1, 1, 1]
v8 = [1, 0, 1]

# i, j and k give the vertices of triangles
f1 = [7, 3, 0]
f2 = [0, 4, 7]
f3 = [0, 1, 2]
f4 = [0, 2, 3]
f5 = [4, 5, 6]
f6 = [4, 6, 7]
f7 = [6, 5, 1]
f8 = [6, 2, 1]
f9 = [4, 0, 5]
f10 = [0, 1, 5]
f11 = [3, 6, 7]
f12 = [2, 3, 6]
vertices = np.array([v1, v2, v3, v4, v5, v6, v7, v8], dtype=np.float32)
faces = np.array([f1, f2, f3, f4, f5, f6, f7, f8, f9, f10, f11, f12], dtype=np.int32)

# create data source
a_data_source = MeshDS_DataSource(vertices, faces)
a_mesh_prs = MeshVS_Mesh()
a_mesh_prs.SetDataSource(a_data_source)
a_builder = MeshVS_MeshPrsBuilder(a_mesh_prs)

a_mesh_prs.AddBuilder(a_builder, True)

# assign nodal builder to the mesh
a_builder = MeshVS_NodalColorPrsBuilder(
    a_mesh_prs, MeshVS_DMF_NodalColorDataPrs | MeshVS_DMF_OCCMask
)
a_builder.UseTexture(True)

display, start_display, add_menu, add_function_to_menu = init_display()

display.Context.Display(a_mesh_prs, True)
display.FitAll()
start_display()
