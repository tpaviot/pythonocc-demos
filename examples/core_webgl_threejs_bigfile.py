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

from OCC.Extend.DataExchange import read_step_file
from OCC.Display.WebGl import threejs_renderer

big_shp = read_step_file(
    os.path.join("..", "assets", "models", "RC_Buggy_2_front_suspension.stp")
)

my_renderer = threejs_renderer.ThreejsRenderer()
my_renderer.DisplayShape(big_shp)
my_renderer.render()
