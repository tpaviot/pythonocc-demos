##Copyright 2026 Thomas Paviot (tpaviot@gmail.com)
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

"""Custom user data in a glTF file: the TDataStd_NamedData attribute of a
shape label is exported as the "extras" of the glTF node, and the glTF
reader imports the "extras" back into a TDataStd_NamedData attribute.

On import, the extras of a node are attached to the XCAF instance
(reference) label of the shape, not to the shape label itself: look at all
the labels of the document."""

from OCC.Core.BRepMesh import BRepMesh_IncrementalMesh
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeBox, BRepPrimAPI_MakeSphere
from OCC.Core.Message import Message_ProgressRange
from OCC.Core.RWGltf import RWGltf_CafReader, RWGltf_CafWriter
from OCC.Core.TCollection import TCollection_AsciiString
from OCC.Core.TColStd import TColStd_IndexedDataMapOfStringString
from OCC.Core.TDataStd import TDataStd_Name, TDataStd_NamedData
from OCC.Core.TDF import TDF_ChildIterator
from OCC.Core.TDocStd import TDocStd_Document
from OCC.Core.XCAFDoc import XCAFDoc_DocumentTool

GLB_FILENAME = "shapes_with_extras.glb"

#
# Export: a box and a sphere, each with its user data
#
doc = TDocStd_Document("pythonocc-doc")
shape_tool = XCAFDoc_DocumentTool.ShapeTool(doc.Main())

shapes = {
    "box": (BRepPrimAPI_MakeBox(10.0, 20.0, 30.0).Shape(), "steel", 3),
    "sphere": (BRepPrimAPI_MakeSphere(15.0).Shape(), "aluminium", 7),
}
for name, (shape, material, quantity) in shapes.items():
    BRepMesh_IncrementalMesh(shape, 0.5)
    label = shape_tool.AddShape(shape)
    TDataStd_Name.Set(label, name)
    user_data = TDataStd_NamedData.Set(label)
    user_data.SetString("material", material)
    user_data.SetInteger("quantity", quantity)

writer = RWGltf_CafWriter(GLB_FILENAME, True)
writer.Perform(doc, TColStd_IndexedDataMapOfStringString(), Message_ProgressRange())

#
# Import: read the extras back
#
imported_doc = TDocStd_Document("pythonocc-doc")
reader = RWGltf_CafReader()
reader.SetDocument(imported_doc)
reader.Perform(GLB_FILENAME, Message_ProgressRange())

imported_shape_tool = XCAFDoc_DocumentTool.ShapeTool(imported_doc.Main())
label_iterator = TDF_ChildIterator(imported_shape_tool.BaseLabel(), True)
while label_iterator.More():
    label = label_iterator.Value()
    # FindAttribute returns None if the label has no such attribute
    user_data = label.FindAttribute(TDataStd_NamedData.GetID(), TDataStd_NamedData())
    if user_data is not None:
        material = TCollection_AsciiString(user_data.GetString("material")).ToCString()
        quantity = user_data.GetInteger("quantity")
        print(f"{label.GetLabelName()}: material={material}, quantity={quantity}")
    label_iterator.Next()
