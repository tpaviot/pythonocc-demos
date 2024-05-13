##Copyright 2024 Thomas Paviot (tpaviot@gmail.com)
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

import os

from OCC.Core.MeshDS import MeshDS_DataSource
from OCC.Core.MeshVS import *

from OCC.Display.SimpleGui import init_display

import numpy as np
import stl  # numpy-stl

# load a stl file using numpy-stl
stl_filename = os.path.join("..", "assets", "models", "fan.stl")
stl_mesh = stl.mesh.Mesh.from_file(stl_filename)
vertices = stl_mesh.vectors.reshape(-1, 3)
faces = np.array(
    [[i, i + 1, i + 2] for i in range(0, len(vertices), 3)], dtype=np.int32
)

# create data source
a_data_source = MeshDS_DataSource(vertices, faces)
a_mesh_prs = MeshVS_Mesh()
a_mesh_prs.SetDataSource(a_data_source)
a_builder = MeshVS_MeshPrsBuilder(a_mesh_prs)
a_mesh_prs.AddBuilder(a_builder, True)

display, start_display, add_menu, add_function_to_menu = init_display()
display.Context.Display(a_mesh_prs, True)
display.FitAll()
start_display()
