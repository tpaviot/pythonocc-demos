##Copyright 2009-2015 Thomas Paviot (tpaviot@gmail.com)
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

import math
from OCC.Core.gp import gp_Dir, gp_Pln, gp_Ax3, gp
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeBox
from OCC.Core.BRepOffsetAPI import BRepOffsetAPI_DraftAngle
from OCC.Core.Precision import precision
from OCC.Core.BRep import BRep_Tool
from OCC.Core.TopExp import TopExp_Explorer
from OCC.Core.TopAbs import TopAbs_FACE
from OCC.Core.Geom import Geom_Plane
from OCC.Core.TopoDS import topods

from OCC.Display.SimpleGui import init_display

display, start_display, add_menu, add_function_to_menu = init_display()


def draft_angle(event=None):
    S = BRepPrimAPI_MakeBox(200.0, 300.0, 150.0).Shape()
    adraft = BRepOffsetAPI_DraftAngle(S)
    topExp = TopExp_Explorer()
    topExp.Init(S, TopAbs_FACE)
    while topExp.More():
        face = topods.Face(topExp.Current())
        surf = Geom_Plane.DownCast(BRep_Tool.Surface(face))
        dirf = surf.Pln().Axis().Direction()
        ddd = gp_Dir(0, 0, 1)
        if dirf.IsNormal(ddd, precision.Angular()):
            adraft.Add(face, ddd, math.radians(15), gp_Pln(gp_Ax3(gp.XOY())))
        topExp.Next()
    adraft.Build()
    display.DisplayShape(adraft.Shape(), update=True)


if __name__ == "__main__":
    draft_angle()
    start_display()
