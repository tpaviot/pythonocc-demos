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

import os

from OCC.Core.MeshDataSource import Mesh_DataSource
from OCC.Core.RWStl import rwstl_ReadFile
from OCC.Core.MeshVS import *

from OCC.Display.SimpleGui import init_display

stl_filename = os.path.join('..', 'assets', 'models', 'fan.stl')

a_stl_mesh = rwstl_ReadFile(stl_filename)

a_data_source = Mesh_DataSource(a_stl_mesh)

a_mesh_prs = MeshVS_Mesh()
a_mesh_prs.SetDataSource(a_data_source)
a_builder = MeshVS_MeshPrsBuilder(a_mesh_prs)

a_mesh_prs.AddBuilder (a_builder, True)

# assign nodal builder to the mesh
a_builder = MeshVS_NodalColorPrsBuilder (a_mesh_prs, MeshVS_DMF_NodalColorDataPrs | MeshVS_DMF_OCCMask)
a_builder.UseTexture(True)

display, start_display, add_menu, add_function_to_menu = init_display()

display.Context.Display(a_mesh_prs, True)
display.FitAll()
start_display()
