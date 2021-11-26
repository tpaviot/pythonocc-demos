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
import random

from OCC.Core.MeshDS import MeshDS_DataSource
from OCC.Core.RWStl import rwstl_ReadFile
from OCC.Core.MeshVS import *
from OCC.Core.Aspect import Aspect_SequenceOfColor
from OCC.Core.Quantity import Quantity_Color, Quantity_NOC_RED, Quantity_NOC_BLUE1, Quantity_NOC_BLACK
from OCC.Core.TColStd import TColStd_DataMapOfIntegerReal

from OCC.Display.SimpleGui import init_display

stl_filename = os.path.join('..', 'assets', 'models', 'fan.stl')

# read the stl file
a_stl_mesh = rwstl_ReadFile(stl_filename)

# create the data source
a_data_source = MeshDS_DataSource(a_stl_mesh)

# create a mesh from the data source
a_mesh = MeshVS_Mesh()
a_mesh.SetDataSource(a_data_source)

# assign nodal builder to the mesh
a_builder = MeshVS_NodalColorPrsBuilder(a_mesh, MeshVS_DMF_NodalColorDataPrs | MeshVS_DMF_OCCMask)
a_builder.UseTexture(True)

# prepare color map
aColorMap = Aspect_SequenceOfColor()
aColorMap.Append(Quantity_Color(Quantity_NOC_RED))
aColorMap.Append(Quantity_Color(Quantity_NOC_BLUE1))

# assign color scale map values (0..1) to nodes
aScaleMap = TColStd_DataMapOfIntegerReal()

# iterate through the nodes and add an node id and
# an appropriate value to the map
# color should be from 0. to 1.
for anId in range(1000):  # TODO use the mesh number of nodes
	aValue = random.uniform(0, 1)
	aScaleMap.Bind(anId, aValue)

# pass color map and color scale values to the builder
a_builder.SetColorMap(aColorMap)
a_builder.SetInvalidColor(Quantity_Color(Quantity_NOC_BLACK))
a_builder.SetTextureCoords(aScaleMap)
a_mesh.AddBuilder(a_builder, True)

# display
display, start_display, add_menu, add_function_to_menu = init_display()
display.Context.Display(a_mesh, True)
display.FitAll()
start_display()
