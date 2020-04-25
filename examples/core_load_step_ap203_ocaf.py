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

from __future__ import print_function


from OCC.Core.TCollection import TCollection_ExtendedString

from OCC.Core.TDocStd import TDocStd_Document
from OCC.Core.XCAFDoc import (XCAFDoc_DocumentTool_ShapeTool,
                              XCAFDoc_DocumentTool_ColorTool,
                              XCAFDoc_DocumentTool_LayerTool,
                              XCAFDoc_DocumentTool_MaterialTool)
from OCC.Core.STEPCAFControl import STEPCAFControl_Reader
from OCC.Core.IFSelect import IFSelect_RetDone
from OCC.Core.TDF import TDF_LabelSequence

from OCC.Display.SimpleGui import init_display

filename = '../assets/models/as1_pe_203.stp'
_shapes = []

# create an handle to a document
doc = TDocStd_Document(TCollection_ExtendedString("pythonocc-doc"))

# Get root assembly
shape_tool = XCAFDoc_DocumentTool_ShapeTool(doc.Main())
l_colors = XCAFDoc_DocumentTool_ColorTool(doc.Main())
l_layers = XCAFDoc_DocumentTool_LayerTool(doc.Main())
l_materials = XCAFDoc_DocumentTool_MaterialTool(doc.Main())

step_reader = STEPCAFControl_Reader()
step_reader.SetColorMode(True)
step_reader.SetLayerMode(True)
step_reader.SetNameMode(True)
step_reader.SetMatMode(True)

status = step_reader.ReadFile(filename)
if status == IFSelect_RetDone:
    step_reader.Transfer(doc)

labels = TDF_LabelSequence()
color_labels = TDF_LabelSequence()

shape_tool.GetFreeShapes(labels)

print("Number of shapes at root :%i" % labels.Length())
for i in range(labels.Length()):
    sub_shapes_labels = TDF_LabelSequence()
    print("Is Assembly :", shape_tool.IsAssembly(labels.Value(i+1)))
    sub_shapes = shape_tool.GetSubShapes(labels.Value(i+1), sub_shapes_labels)
    print("Number of subshapes in the assemly :%i" % sub_shapes_labels.Length())
l_colors.GetColors(color_labels)

print("Number of colors=%i" % color_labels.Length())
for i in range(color_labels.Length()):
    color = color_labels.Value(i+1)
    print(color.DumpToString())

for i in range(labels.Length()):
    label = labels.Value(i+1)
    a_shape = shape_tool.GetShape(label)
    m = l_layers.GetLayers(a_shape)
    _shapes.append(a_shape)

#
# Display
#
display, start_display, add_menu, add_function_to_menu = init_display()
display.DisplayShape(_shapes, update=True)
start_display()
