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
from OCC.Core.Message import Message_ProgressRange
from OCC.Core.RWGltf import RWGltf_CafReader
from OCC.Core.IFSelect import IFSelect_RetDone

from OCC.Display.SimpleGui import init_display

filename = "../assets/models/2CylinderEngine.glb"

# create an handle to a document
doc = TDocStd_Document("pythonocc-doc")

gltf_reader = RWGltf_CafReader()

# gltf_reader.SetSystemLengthUnit(aScaleFactorM)
# gltf_reader.SetSystemCoordinateSystem(RWMesh_CoordinateSystem_Zup)
gltf_reader.SetDocument(doc)
# gltf_reader.SetParallel(True)
# gltf_reader.SetDoublePrecision(True)
# gltf_reader.SetToSkipLateDataLoading(True)
# gltf_reader.SetToKeepLateData(True)
# gltf_reader.SetToPrintDebugMessages(True)
# gltf_reader.SetLoadAllScenes(True)
status = gltf_reader.Perform(filename, Message_ProgressRange())

assert status == IFSelect_RetDone

shp = gltf_reader.SingleShape()

#
# Display
#
display, start_display, add_menu, add_function_to_menu = init_display()
display.DisplayShape(shp, update=True)
start_display()
