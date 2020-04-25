##Copyright 2020 Thomas Paviot (tpaviot@gmail.com)
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

from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeBox, BRepPrimAPI_MakeSphere
from OCC.Core.Graphic3d import Graphic3d_ZLayerSettings

from OCC.Display.SimpleGui import init_display

display, start_display, add_menu, add_function_to_menu = init_display()

myBox = BRepPrimAPI_MakeBox(60, 60, 50).Shape()
mySphere = BRepPrimAPI_MakeSphere(30).Shape()

# the V3d_Viewer
viewer = display.Viewer
print(viewer)

# create 2 layers with different settings
settings_1 = Graphic3d_ZLayerSettings()
layer_created_1, layer_id_1 = viewer.AddZLayer(settings_1)
if layer_created_1:
    print("Layer 1 successfully created")
    print("Layer 1 id:", layer_id_1)
settings_2 = Graphic3d_ZLayerSettings()
layer_created_2, layer_id_2 = viewer.AddZLayer(settings_2)
if layer_created_1:
    print("Layer 2 successfully created")
    print("Layer 2 id:", layer_id_2)

# draw sphere and box, and set each one a z layer index
[ais_box] = display.DisplayShape(myBox)
ais_box.SetZLayer(layer_id_1)
[ais_sphere] = display.DisplayShape(mySphere)
ais_sphere.SetZLayer(layer_id_2)

display.FitAll()
start_display()
