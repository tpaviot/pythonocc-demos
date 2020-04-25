##Copyright 2020 Doug Blanding (dblanding@gmail.com)
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

# based on https://www.cnblogs.com/opencascade/p/MakeFaceWithHoles.html

from OCC.Core.gp import gp_Circ, gp_Pln, gp_XOY, gp_Pnt
from OCC.Core.BRepBuilderAPI import (BRepBuilderAPI_MakeEdge,
                                     BRepBuilderAPI_MakeWire,
                                     BRepBuilderAPI_MakeFace)
from OCC.Display.SimpleGui import init_display

display, start_display, add_menu, add_function_to_menu = init_display()

def holes_in_face():
    aPlane = gp_Pln()
    print(type(gp_Pln()))
    print(type(gp_XOY()))

    aCircle1 = gp_Circ(gp_XOY(), 1.0)
    aCircle2 = gp_Circ(gp_XOY(), 1.0)
    aCircle3 = gp_Circ(gp_XOY(), 1.0)

    aCircle1.SetLocation(gp_Pnt(3.0, 3.0, 0.0))
    aCircle2.SetLocation(gp_Pnt(7.0, 3.0, 0.0))
    aCircle3.SetLocation(gp_Pnt(3.0, 7.0, 0.0))

    anEdgeMaker1 = BRepBuilderAPI_MakeEdge(aCircle1)
    anEdgeMaker2 = BRepBuilderAPI_MakeEdge(aCircle2)
    anEdgeMaker3 = BRepBuilderAPI_MakeEdge(aCircle3)

    aWireMaker1 = BRepBuilderAPI_MakeWire(anEdgeMaker1.Edge())
    aWireMaker2 = BRepBuilderAPI_MakeWire(anEdgeMaker2.Edge())
    aWireMaker3 = BRepBuilderAPI_MakeWire(anEdgeMaker3.Edge())

    aFaceMaker = BRepBuilderAPI_MakeFace(aPlane, 0.0, 10.0, 0.0, 10.0)

    if aWireMaker1.IsDone():
        aWire1 = aWireMaker1.Wire()
        aWire1.Reverse()  # Makes this a hole in outer profile
        aFaceMaker.Add(aWire1)

    if aWireMaker2.IsDone():
        aWire2 = aWireMaker2.Wire()
        aWire2.Reverse()  # Makes this a hole in outer profile
        aFaceMaker.Add(aWire2)

    if aWireMaker3.IsDone():
        aWire3 = aWireMaker3.Wire()
        aWire3.Reverse()  # Makes this a hole in outer profile
        aFaceMaker.Add(aWire3)

    if not aFaceMaker.IsDone():
        raise AssertionError("shape not Done.")

    return aFaceMaker.Shape()

if __name__ == "__main__":
    face = holes_in_face()
    display.DisplayShape(face, update=True)
    start_display()
