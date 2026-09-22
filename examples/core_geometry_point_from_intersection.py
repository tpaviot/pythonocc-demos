#!/usr/bin/env python

##Copyright 2009-2014 Jelle Feringa (jelleferinga@gmail.com)
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


from OCC.Core.GC import GC_MakeEllipse, GC_MakePlane
from OCC.Core.Geom import Geom_RectangularTrimmedSurface
from OCC.Core.gp import gp, gp_Ax3, gp_Elips, gp_Pln
from OCC.Core.IntAna import IntAna_IntConicQuad
from OCC.Core.Precision import precision
from OCC.Display.SimpleGui import init_display

display, start_display, add_menu, add_function_to_menu = init_display()


def points_from_intersection():
    """
    @param display:
    """
    plane = gp_Pln(gp_Ax3(gp.XOY()))
    minor_radius, major_radius = 5.0, 8.0
    ellips = gp_Elips(gp.YOZ(), major_radius, minor_radius)
    intersection = IntAna_IntConicQuad(
        ellips, plane, precision.Angular(), precision.Confusion()
    )
    a_plane = GC_MakePlane(plane).Value()
    a_surface = Geom_RectangularTrimmedSurface(
        a_plane, -8.0, 8.0, -12.0, 12.0, True, True
    )
    display.DisplayShape(a_surface, update=True)

    anEllips = GC_MakeEllipse(ellips).Value()
    display.DisplayShape(anEllips)

    if intersection.IsDone():
        nb_results = intersection.NbPoints()
        if nb_results > 0:
            for i in range(1, nb_results + 1):
                P = intersection.Point(i)
                pstring = f"P{i}"
                display.DisplayShape(P)
                display.DisplayMessage(P, pstring)


if __name__ == "__main__":
    points_from_intersection()
    start_display()
