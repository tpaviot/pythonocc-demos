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

"""The DE (data exchange) framework: one provider per file format, chosen
by a DE_Wrapper from the file extension. The same Read and Write calls
convert an XCAF document, with its assembly structure, names and colors,
to and from STEP, IGES, glTF, OBJ, STL, VRML, PLY or BREP. The parameters
of each format are set on its configuration node."""

import os
import tempfile

from OCC.Core.BRepMesh import BRepMesh_IncrementalMesh
from OCC.Core.DE import DE_Wrapper
from OCC.Core.DEGLTF import DEGLTF_ConfigurationNode
from OCC.Core.DEIGES import DEIGES_ConfigurationNode
from OCC.Core.DEOBJ import DEOBJ_ConfigurationNode
from OCC.Core.DESTEP import DESTEP_ConfigurationNode, DESTEP_Parameters
from OCC.Core.DESTL import DESTL_ConfigurationNode
from OCC.Core.TDF import TDF_LabelSequence
from OCC.Core.TDocStd import TDocStd_Document
from OCC.Core.TopoDS import TopoDS_Shape
from OCC.Core.XCAFDoc import XCAFDoc_DocumentTool
from OCC.Display.SimpleGui import init_display

display, start_display, add_menu, add_function_to_menu = init_display()

# the formats the wrapper can read and write, with their parameters
step_node = DESTEP_ConfigurationNode()
step_node.InternalParameters.WriteSchema = (
    DESTEP_Parameters.WriteMode_StepSchema_AP242DIS
)
iges_node = DEIGES_ConfigurationNode()
iges_node.InternalParameters.WriteHeaderAuthor = "pythonocc"
gltf_node = DEGLTF_ConfigurationNode()
gltf_node.InternalParameters.WriteAuthor = "pythonocc"
stl_node = DESTL_ConfigurationNode()
stl_node.InternalParameters.WriteAscii = False

wrapper = DE_Wrapper()
for node in (step_node, iges_node, gltf_node, DEOBJ_ConfigurationNode(), stl_node):
    wrapper.Bind(node)

# read an assembly in an XCAF document: the provider is chosen from the
# extension of the file
step_file = os.path.join("..", "assets", "models", "as1-oc-214.stp")
document = TDocStd_Document("BinXCAF")
if not wrapper.Read(step_file, document):
    raise RuntimeError(f"{step_file} not read")
shape_tool = XCAFDoc_DocumentTool.ShapeTool(document.Main())
free_shapes = TDF_LabelSequence()
shape_tool.GetFreeShapes(free_shapes)
print(f"{step_file}: {free_shapes.Length()} assembly")

# the mesh based formats write the triangulation of the faces
for i in range(1, free_shapes.Length() + 1):
    BRepMesh_IncrementalMesh(shape_tool.GetShape(free_shapes.Value(i)), 0.5)

# write the document to each format, the colors and names are kept by
# the formats that support them
with tempfile.TemporaryDirectory() as output_dir:
    for extension in ("step", "igs", "glb", "obj", "stl"):
        file_name = os.path.join(output_dir, f"as1.{extension}")
        if not wrapper.Write(file_name, document):
            raise RuntimeError(f"{file_name} not written")
        print(f"{os.path.basename(file_name)}: {os.path.getsize(file_name)} bytes")

    # read back the glTF file as a single shape
    gltf_shape = TopoDS_Shape()
    if not wrapper.Read(os.path.join(output_dir, "as1.glb"), gltf_shape):
        raise RuntimeError("as1.glb not read")

display.DisplayShape(gltf_shape, update=True)
start_display()
