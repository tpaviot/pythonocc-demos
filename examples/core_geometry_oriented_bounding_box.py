#!/usr/bin/env python
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

import random

from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeBox
from OCC.Core.gp import gp_Pnt, gp_Ax2, gp_Dir, gp_XYZ
from OCC.Core.BRepBndLib import brepbndlib_AddOBB
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeVertex
from OCC.Core.Bnd import Bnd_OBB

from OCC.Display.SimpleGui import init_display

display, start_display, add_menu, add_function_to_menu = init_display()

def ConvertBndToShape(theBox):
  aBaryCenter = theBox.Center()
  aXDir = theBox.XDirection()
  aYDir = theBox.YDirection()
  aZDir = theBox.ZDirection()
  aHalfX = theBox.XHSize()
  aHalfY = theBox.YHSize()
  aHalfZ = theBox.ZHSize()

  ax = gp_XYZ(aXDir.X(), aXDir.Y(), aXDir.Z())
  ay = gp_XYZ(aYDir.X(), aYDir.Y(), aYDir.Z())
  az = gp_XYZ(aZDir.X(), aZDir.Y(), aZDir.Z())
  p = gp_Pnt(aBaryCenter.X(), aBaryCenter.Y(), aBaryCenter.Z())
  anAxes = gp_Ax2(p, gp_Dir(aZDir), gp_Dir(aXDir))
  anAxes.SetLocation(gp_Pnt(p.XYZ() - ax*aHalfX - ay*aHalfY - az*aHalfZ))
  aBox = BRepPrimAPI_MakeBox(anAxes, 2.0*aHalfX, 2.0*aHalfY, 2.0*aHalfZ).Shape()
  return aBox

# compute the oriented bounding box of a point cloud
obb1 = Bnd_OBB()
n = 10
for _ in range(n):
	x = random.uniform(100, 500)
	y = random.uniform(100, 500)
	z = random.uniform(100, 500)
	p = BRepBuilderAPI_MakeVertex(gp_Pnt(x, y, z)).Shape()
	display.DisplayShape(p)
	brepbndlib_AddOBB(p, obb1)
obb_shape1 = ConvertBndToShape(obb1)
display.DisplayShape(obb_shape1, transparency=0.5)

# then loads a brep file and computes the optimal bounding box
from OCC.Core.BRepTools import breptools_Read
from OCC.Core.TopoDS import TopoDS_Shape
from OCC.Core.BRep import BRep_Builder

cylinder_head = TopoDS_Shape()
builder = BRep_Builder()
breptools_Read(cylinder_head, '../assets/models/cylinder_head.brep', builder)
obb2 = Bnd_OBB()
brepbndlib_AddOBB(cylinder_head, obb2, True, True, True)
obb_shape2 = ConvertBndToShape(obb2)
display.DisplayShape(cylinder_head)
display.DisplayShape(obb_shape2, transparency=0.5, update=True)

start_display()
