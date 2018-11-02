##Copyright Paul Hideaki (paul.hideaki@gmail.com)
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

from OCC.Core.gp import gp_Pnt
from OCC.Core.BRepBuilderAPI import (BRepBuilderAPI_MakeFace, BRepBuilderAPI_MakePolygon,
                                     BRepBuilderAPI_Sewing, BRepBuilderAPI_MakeSolid)
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeBox
from OCC.Core.BRepAlgoAPI import BRepAlgoAPI_Fuse, BRepAlgoAPI_Common, BRepAlgoAPI_Cut
from OCC.Core.TopoDS import topods
from OCC.Display.SimpleGui import init_display


def MakeSolidFromShell(shell):
    ms = BRepBuilderAPI_MakeSolid()
    ms.Add(topods.Shell(shell))
    solid = ms.Solid()
    return solid


def make_face_from_4_points(pnt1, pnt2, pnt3, pnt4):
    # frist create a closed polygon
    poly = BRepBuilderAPI_MakePolygon(pnt1, pnt2, pnt3, pnt4, True).Wire()
    # then build the face from the closed wire
    return BRepBuilderAPI_MakeFace(poly).Face()


def get_faceted_L_shape(x, y, z):
    pnt_A = gp_Pnt(x + 0, y + 0, z + 0)
    pnt_B = gp_Pnt(x +20, y + 0, z + 0)
    pnt_C = gp_Pnt(x +20, y +10, z + 0)
    pnt_D = gp_Pnt(x + 0, y +10, z + 0)
    pnt_E = gp_Pnt(x + 0, y + 0, z +20)
    pnt_F = gp_Pnt(x +10, y + 0, z +20)
    pnt_G = gp_Pnt(x +10, y +10, z +20)
    pnt_H = gp_Pnt(x +0, y +10, z +20)
    pnt_I = gp_Pnt(x +10, y + 0, z +10)
    pnt_J = gp_Pnt(x +10, y +10, z +10)
    pnt_K = gp_Pnt(x +20, y + 0, z +10)
    pnt_L = gp_Pnt(x +20, y +10, z +10)

    face_1 = make_face_from_4_points(pnt_A, pnt_B, pnt_C, pnt_D)
    face_2 = make_face_from_4_points(pnt_B, pnt_C, pnt_L, pnt_K)
    face_3 = make_face_from_4_points(pnt_E, pnt_F, pnt_G, pnt_H)
    face_4 = make_face_from_4_points(pnt_A, pnt_E, pnt_H, pnt_D)
    face_5 = make_face_from_4_points(pnt_G, pnt_F, pnt_I, pnt_J)
    face_6 = make_face_from_4_points(pnt_I, pnt_K, pnt_L, pnt_J)

    polygon_1 = BRepBuilderAPI_MakePolygon()
    polygon_1.Add(pnt_A)
    polygon_1.Add(pnt_B)
    polygon_1.Add(pnt_K)
    polygon_1.Add(pnt_I)
    polygon_1.Add(pnt_F)
    polygon_1.Add(pnt_E)
    polygon_1.Close()

    face_7 = BRepBuilderAPI_MakeFace(polygon_1.Wire()).Face()
    polygon_2 = BRepBuilderAPI_MakePolygon()
    polygon_2.Add(pnt_D)
    polygon_2.Add(pnt_H)
    polygon_2.Add(pnt_G)
    polygon_2.Add(pnt_J)
    polygon_2.Add(pnt_L)
    polygon_2.Add(pnt_C)
    polygon_2.Close()
    face_8 = BRepBuilderAPI_MakeFace(polygon_2.Wire()).Face()

    sew = BRepBuilderAPI_Sewing()
    for face in [face_1, face_2, face_3, face_4, face_5, face_6, face_7, face_8]:
        sew.Add(face)
    sew.Perform()

    return sew.SewedShape()

spacing = 30
# cut (box - box)
yshift = 0
myBox11 = BRepPrimAPI_MakeBox(gp_Pnt(0, yshift, 0), 10, 10, 10).Shape()
myBox12 = BRepPrimAPI_MakeBox(gp_Pnt(5, yshift + 5, 5), 10, 10, 10).Shape()
myCut1 = BRepAlgoAPI_Cut(myBox11, myBox12).Shape()

# cut (L-Shape - box)
yshift += spacing
myBox21 = get_faceted_L_shape(0, yshift, 0)
myBox22 = BRepPrimAPI_MakeBox(gp_Pnt(15, yshift + 5, 5), 10, 10, 10).Shape()
myCut2 = BRepAlgoAPI_Cut(myBox21, myBox22).Shape()

# intersection  (L-Shape - box)
yshift += spacing
myBox23 = get_faceted_L_shape(0, yshift, 0)
myBox24 = BRepPrimAPI_MakeBox(gp_Pnt(15, yshift + 5, 5), 10, 10, 10).Shape()
myCut3 = BRepAlgoAPI_Common(myBox23, myBox24).Shape()

# Simple box CUT from LShape using MakeSolidFromShell
yshift += spacing
myBox31 = MakeSolidFromShell(get_faceted_L_shape(0, yshift, 0))
myBox32 = BRepPrimAPI_MakeBox(gp_Pnt(15, yshift + 5, 5), 10, 10, 10).Shape()
myCut4 = BRepAlgoAPI_Cut(myBox31, myBox32).Shape()

# Simple box FUSE from LShape using MakeSolidFromShell
yshift += spacing
myBox33 = MakeSolidFromShell(get_faceted_L_shape(0, yshift, 0))
myBox34 = BRepPrimAPI_MakeBox(gp_Pnt(15, yshift + 5, 5), 10, 10, 10).Shape()
myCut5 = BRepAlgoAPI_Fuse(myBox33, myBox34).Shape()


# Simple box COMMON with LShape using MakeSolidFromShell
yshift += spacing
myBox35 = MakeSolidFromShell(get_faceted_L_shape(0, yshift, 0))
myBox36 = BRepPrimAPI_MakeBox(gp_Pnt(15, yshift + 5, 5), 10, 10, 10).Shape()
myCut6 = BRepAlgoAPI_Common(myBox35, myBox36).Shape()

# display stage
display, start_display, add_menu, add_function_to_menu = init_display()
display.DisplayShape(myCut1, color="RED")
display.DisplayShape(myCut2, color="BLUE")
display.DisplayShape(myCut3, color="WHITE")
display.DisplayShape(myCut4, color="GREEN")
display.DisplayShape(myCut5, color="YELLOW")
display.DisplayShape(myCut6, color="CYAN")
display.FitAll()
start_display()
