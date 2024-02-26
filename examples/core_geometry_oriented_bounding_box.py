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
from OCC.Core.BRepBndLib import brepbndlib
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeVertex
from OCC.Core.Bnd import Bnd_OBB
from OCC.Core.BRepTools import breptools_Read
from OCC.Core.TopoDS import TopoDS_Shape
from OCC.Core.BRep import BRep_Builder

from OCC.Display.SimpleGui import init_display

display, start_display, add_menu, add_function_to_menu = init_display()


def convert_bnd_to_shape(the_box):
    """Converts a bounding box to a box shape."""
    barycenter = the_box.Center()
    x_dir = the_box.XDirection()
    y_dir = the_box.YDirection()
    z_dir = the_box.ZDirection()
    half_x = the_box.XHSize()
    half_y = the_box.YHSize()
    half_z = the_box.ZHSize()

    x_vec = gp_XYZ(x_dir.X(), x_dir.Y(), x_dir.Z())
    y_vec = gp_XYZ(y_dir.X(), y_dir.Y(), y_dir.Z())
    z_vec = gp_XYZ(z_dir.X(), z_dir.Y(), z_dir.Z())
    point = gp_Pnt(barycenter.X(), barycenter.Y(), barycenter.Z())
    axes = gp_Ax2(point, gp_Dir(z_dir), gp_Dir(x_dir))
    axes.SetLocation(
        gp_Pnt(point.XYZ() - x_vec * half_x - y_vec * half_y - z_vec * half_z)
    )
    return BRepPrimAPI_MakeBox(
        axes, 2.0 * half_x, 2.0 * half_y, 2.0 * half_z
    ).Shape()


# compute the oriented bounding box of a point cloud
obb1 = Bnd_OBB()
num_points = 10
for _ in range(num_points):
    x = random.uniform(100, 500)
    y = random.uniform(100, 500)
    z = random.uniform(100, 500)
    p = BRepBuilderAPI_MakeVertex(gp_Pnt(x, y, z)).Shape()
    display.DisplayShape(p)
    brepbndlib.AddOBB(p, obb1)
obb_shape1 = convert_bnd_to_shape(obb1)
display.DisplayShape(obb_shape1, transparency=0.5)

# then loads a brep file and computes the optimal bounding box
cylinder_head = TopoDS_Shape()
builder = BRep_Builder()
breptools_Read(cylinder_head, "../assets/models/cylinder_head.brep", builder)
obb2 = Bnd_OBB()
brepbndlib.AddOBB(cylinder_head, obb2, True, True, True)
obb_shape2 = convert_bnd_to_shape(obb2)
display.DisplayShape(cylinder_head)
display.DisplayShape(obb_shape2, transparency=0.5, update=True)

start_display()
