#!/usr/bin/env python

##Copyright 2009-2016 Thomas Paviot (tpaviot@gmail.com)
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
import sys

from OCC.Extend.DataExchange import read_step_file
from OCC.Extend.TopologyUtils import TopologyExplorer
from OCC.Display.WebGl import threejs_renderer

# opens a big step file
# render each part of the assembly as a shape
stp_file = os.path.join('..', 'assets', 'models', '3864470050F1.stp')
if not os.path.isfile(stp_file):
	print("File 3864470050F1.stp not found. First unzip 3864470050F1.zip file from the assets folder")
	sys.exit(0)
# file exist, we can load the file
big_shp = read_step_file(stp_file)

all_subshapes = TopologyExplorer(big_shp).solids()

my_renderer = threejs_renderer.ThreejsRenderer()
for single_shape in all_subshapes:
	my_renderer.DisplayShape(single_shape)
# then call the renderer
my_renderer.render()
