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
stp_file = os.path.join("..", "assets", "models", "3864470050F1.stp")
if not os.path.isfile(stp_file):
    directory = os.path.join("..", "assets", "models")
    zip_file_path = os.path.join(directory, "3864470050F1.zip")

    # unzip file
    import zipfile

    with zipfile.ZipFile(zip_file_path, "r") as zip_ref:
        zip_ref.extractall(directory)
    assert os.path.isfile(stp_file)
    print(f"File {zip_file_path} extracted to {stp_file}")

# file exist, we can load the file
big_shp = read_step_file(stp_file)

all_subshapes = TopologyExplorer(big_shp).solids()

my_renderer = threejs_renderer.ThreejsRenderer()
for single_shape in all_subshapes:
    my_renderer.DisplayShape(single_shape)
# then call the renderer
my_renderer.render()
