##Copyright 2018 Thomas Paviot (tpaviot@gmail.com)
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

from OCC.Core.gp import gp_Pnt, gp_XYZ, gp_Mat, gp_GTrsf
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeSphere, BRepPrimAPI_MakeBox
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_GTransform
from OCC.Core.BRepAlgoAPI import BRepAlgoAPI_Common

from OCC.Display.SimpleGui import init_display

display, start_display, add_menu, add_function_to_menu = init_display()
orig = gp_Pnt(0., 0., 0.)
sphere = BRepPrimAPI_MakeSphere(orig, 50.).Solid()

# be careful that the following scale numbers are "not too big",
# otherwise boolean operations can be buggy
# see isue 
a1 = 17.1
a2 = 17.1
a3 = 3.5
gTrsf = gp_GTrsf(gp_Mat(a1, 0, 0, 0, a2, 0, 0, 0, a3), gp_XYZ(0., 112.2, 0.))
ellipsoid = BRepBuilderAPI_GTransform(sphere, gTrsf).Shape()

# then perform a boolean intersection with a box
box = BRepPrimAPI_MakeBox(gp_Pnt(-1000, -1000, -1000), gp_Pnt(1000, 112.2, 1000)).Shape()
common = BRepAlgoAPI_Common(box, ellipsoid).Shape()
assert not common.IsNull()

display.DisplayShape(box, color = "BLACK", transparency = 0.8)
display.DisplayShape(ellipsoid, color = "BLACK", transparency = 0.8)
display.DisplayShape(common, color = "BLACK", transparency = 0.8, update=True)
start_display() 
