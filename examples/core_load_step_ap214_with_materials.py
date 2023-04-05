##Copyright 2023 Thomas Paviot (tpaviot@gmail.com)
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
from OCC.Core.XCAFDoc import (
    XCAFDoc_DocumentTool_MaterialTool,
)
from OCC.Core.STEPCAFControl import STEPCAFControl_Reader
from OCC.Core.IFSelect import IFSelect_RetDone
from OCC.Core.TDF import TDF_LabelSequence

filename = "../assets/models/eight_cyl.stp"

# create an handle to a document
doc = TDocStd_Document("pythonocc-doc")

# Get root assembly
mat_tool = XCAFDoc_DocumentTool_MaterialTool(doc.Main())

step_reader = STEPCAFControl_Reader()

status = step_reader.ReadFile(filename)
if status == IFSelect_RetDone:
    step_reader.Transfer(doc)

material_labels = TDF_LabelSequence()

mat_tool.GetMaterialLabels(material_labels)

# materials
for i in range(1, material_labels.Length() + 1):
    (
        ok,
        material_name,
        material_description,
        material_density,
        material_densname,
        material_densvaltype,
    ) = mat_tool.GetMaterial(material_labels.Value(i))

    print(f"Material name: {material_name}")
    print(f"Material description: {material_description}")
    print(f"Material density: {material_density}")
    print(f"Material densname: {material_densname}")
    print(f"Material_densvaltype: {material_densvaltype}\n")
