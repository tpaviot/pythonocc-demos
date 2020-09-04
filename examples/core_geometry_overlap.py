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

''' Example for shape overlapping detection.
See pythonocc-core issue #628 at
https://github.com/tpaviot/pythonocc-core/issues/628
'''

from OCC.Core.gp import gp_Pnt
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeBox
from OCC.Core.BRepMesh import BRepMesh_IncrementalMesh
from OCC.Core.BRepExtrema import BRepExtrema_ShapeProximity
from OCC.Display.SimpleGui import init_display

display, start_display, add_menu, add_function_to_menu = init_display()
 
# create two boxes that intersect
box1 = BRepPrimAPI_MakeBox(gp_Pnt(0, 0, 0), gp_Pnt(20, 20, 20)).Shape()
box2 = BRepPrimAPI_MakeBox(gp_Pnt(10, 10, 10), gp_Pnt(30, 30, 30)).Shape()

# Create meshes for the proximity algorithm
deflection = 1e-3
mesher1 = BRepMesh_IncrementalMesh(box1, deflection)
mesher2 = BRepMesh_IncrementalMesh(box2, deflection)
mesher1.Perform()
mesher2.Perform()

# Perform shape proximity check
tolerance = 0.1
isect_test = BRepExtrema_ShapeProximity(box1, box2, tolerance)
isect_test.Perform()

# Get intersecting faces from Shape1
overlaps1 = isect_test.OverlapSubShapes1()
face_indices1 = overlaps1.Keys()
shape_1_faces = []
for ind in face_indices1:
    face = isect_test.GetSubShape1(ind)
    shape_1_faces.append(face)

# Get intersecting faces from Shape2
overlaps2 = isect_test.OverlapSubShapes2()
face_indices2 = overlaps2.Keys()
shape_2_faces = []
for ind in face_indices2:
    face = isect_test.GetSubShape2(ind)
    shape_2_faces.append(face)

# display both boxes and intersecting faces, in RED
display.DisplayShape(box1, transparency=0.5)
display.DisplayShape(box2, transparency=0.5)
display.DisplayShape(shape_1_faces + shape_2_faces, color='RED')

display.FitAll()
start_display()
