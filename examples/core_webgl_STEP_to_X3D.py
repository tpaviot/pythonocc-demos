##Copyright 2010-2014 Thomas Paviot (tpaviot@gmail.com)
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

from OCC.Extend.DataExchange import read_step_file_with_names_colors
from OCC.Extend.TopologyUtils import TopologyExplorer
from OCC.Display.WebGl import x3dom_renderer

filename = '../assets/models/as1-oc-214.stp'
shapes_labels_colors = read_step_file_with_names_colors(filename)

# create the x3dom renderer
my_renderer = x3dom_renderer.X3DomRenderer()

# traverse shapes, render in "face" mode
for shpt_lbl_color in shapes_labels_colors:
    shape, label, c = shpt_lbl_color
    all_faces = TopologyExplorer(shape).faces()
    for face in all_faces:
        my_renderer.DisplayShape(face, color=(c.Red(), c.Green(), c.Blue()))

my_renderer.render()
