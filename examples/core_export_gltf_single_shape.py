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

from OCC.Core.TDocStd import TDocStd_Document
from OCC.Core.TCollection import TCollection_ExtendedString, TCollection_AsciiString
from OCC.Core.XCAFDoc import (
    XCAFDoc_DocumentTool_ShapeTool,
    XCAFDoc_DocumentTool_LayerTool,
)
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeSphere
from OCC.Core.TColStd import TColStd_IndexedDataMapOfStringString
from OCC.Core.Message import Message_ProgressRange
from OCC.Core.BRepMesh import BRepMesh_IncrementalMesh
from OCC.Core.BRepTools import breptools_Clean

# GLTF export
from OCC.Core.RWGltf import RWGltf_CafWriter, RWGltf_WriterTrsfFormat

# create the shapeto export
shp = BRepPrimAPI_MakeSphere(60.0).Shape()

# create a document
doc = TDocStd_Document(TCollection_ExtendedString("pythonocc-doc"))
shape_tool = XCAFDoc_DocumentTool_ShapeTool(doc.Main())
layer_tool = XCAFDoc_DocumentTool_LayerTool(doc.Main())

# mesh shape
breptools_Clean(shp)
# Triangulate
msh_algo = BRepMesh_IncrementalMesh(shp, True)
msh_algo.Perform()

sub_shape_label = shape_tool.AddShape(shp)

# GLTF options
a_format = RWGltf_WriterTrsfFormat.RWGltf_WriterTrsfFormat_Compact
force_uv_export = True

# metadata
a_file_info = TColStd_IndexedDataMapOfStringString()
a_file_info.Add(
    TCollection_AsciiString("Authors"), TCollection_AsciiString("pythonocc")
)

#
# Binary export
#
binary = True
binary_rwgltf_writer = RWGltf_CafWriter(TCollection_AsciiString("box.glb"), binary)
binary_rwgltf_writer.SetTransformationFormat(a_format)
binary_rwgltf_writer.SetForcedUVExport(force_uv_export)
pr = Message_ProgressRange()  # this is required
binary_rwgltf_writer.Perform(doc, a_file_info, pr)

#
# Ascii export
#
binary = False
ascii_rwgltf_writer = RWGltf_CafWriter(TCollection_AsciiString("box.gla"), binary)
ascii_rwgltf_writer.SetTransformationFormat(a_format)
ascii_rwgltf_writer.SetForcedUVExport(force_uv_export)
pr = Message_ProgressRange()  # this is required
ascii_rwgltf_writer.Perform(doc, a_file_info, pr)
