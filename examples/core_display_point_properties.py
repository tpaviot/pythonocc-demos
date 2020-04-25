#!/usr/bin/env python

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

import sys

from OCC.Core.gp import gp_Pnt
from OCC.Core.Geom import Geom_CartesianPoint
from OCC.Core.Quantity import Quantity_Color, Quantity_TOC_RGB
from OCC.Core.Aspect import (Aspect_TOM_POINT,
                             Aspect_TOM_PLUS,
                             Aspect_TOM_STAR,
                             Aspect_TOM_X,
                             Aspect_TOM_O,
                             Aspect_TOM_O_POINT,
                             Aspect_TOM_O_PLUS,
                             Aspect_TOM_O_STAR,
                             Aspect_TOM_O_X,
                             Aspect_TOM_RING1,
                             Aspect_TOM_RING2,
                             Aspect_TOM_RING3,
                             Aspect_TOM_BALL)
from OCC.Core.AIS import AIS_Point
from OCC.Core.Prs3d import Prs3d_PointAspect, Prs3d_Drawer

from OCC.Display.SimpleGui import init_display
display, start_display, add_menu, add_function_to_menu = init_display()

ALL_ASPECTS = [Aspect_TOM_POINT,
               Aspect_TOM_PLUS,
               Aspect_TOM_STAR,
               Aspect_TOM_X,
               Aspect_TOM_O,
               Aspect_TOM_O_POINT,
               Aspect_TOM_O_PLUS,
               Aspect_TOM_O_STAR,
               Aspect_TOM_O_X,
               Aspect_TOM_RING1,
               Aspect_TOM_RING2,
               Aspect_TOM_RING3,
               Aspect_TOM_BALL]
def pnt():
    # create a point
    for idx in range(10):
        for idy in range(10):
            for idz, aspect in enumerate(ALL_ASPECTS):
                x = 0 + idx * 0.1
                y = 0 + idy * 0.1
                z = 0 + idz / len(ALL_ASPECTS)
                p = Geom_CartesianPoint(gp_Pnt(x, y, z))
                color = Quantity_Color(x / len(ALL_ASPECTS), 0, z, Quantity_TOC_RGB)
                ais_point = AIS_Point(p)

                drawer = ais_point.Attributes()
                asp = Prs3d_PointAspect(aspect, color, 3)
                drawer.SetPointAspect(asp)
                ais_point.SetAttributes(drawer)

                display.Context.Display(ais_point, False)
    display.FitAll()
    start_display()


def exit(event=None):
    sys.exit()

if __name__ == '__main__':
    pnt()
