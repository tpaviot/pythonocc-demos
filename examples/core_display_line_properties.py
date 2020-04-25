#!/usr/bin/env python

##Copyright 2017 Emad Dlala (emad.dlala@gmail.com)
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

from __future__ import print_function

import sys

from OCC.Core.gp import gp_Pnt, gp_Dir
from OCC.Core.Geom import Geom_Line
from OCC.Core.AIS import AIS_Line
from OCC.Core.Prs3d import Prs3d_LineAspect, Prs3d_Drawer
from OCC.Core.Quantity import Quantity_Color

from OCC.Display.SimpleGui import init_display
display, start_display, add_menu, add_function_to_menu = init_display()


def line():
    # create a line
    p1 = gp_Pnt(2., 3., 4.)
    d1 = gp_Dir(4., 5., 6.)
    line1 = Geom_Line(p1, d1)

    ais_line1 = AIS_Line(line1)

    # if we need to edit color, we can simply use SetColor
    # ais_line1.SetColor(Quantity_NOC_RED)

    # but actually we need to edit more, not just color. Line width and style as well
    # To do that, we need to do use AIS_Drawer and apply it to ais_line1
    drawer = Prs3d_Drawer()
    ais_line1.SetAttributes(drawer)

    display.Context.Display(ais_line1, False)
    # we can apply the same rule for other lines by just doing a for loop
    for i in range(1, 5):
        p2 = gp_Pnt(i, 2., 5.)
        d2 = gp_Dir(4*i, 6., 9.)
        line2 = Geom_Line(p2, d2)

        ais_line2 = AIS_Line(line2)

        width = float(i)
        drawer = ais_line2.Attributes()
        # asp : first parameter color, second type, last width
        asp = Prs3d_LineAspect(Quantity_Color(9*i), i, width)
        drawer.SetLineAspect(asp)
        ais_line2.SetAttributes(drawer)

        display.Context.Display(ais_line2, False)
    start_display()


def exit(event=None):
    sys.exit()

if __name__ == '__main__':
    line()
