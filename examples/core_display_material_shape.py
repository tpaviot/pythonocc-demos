#!/usr/bin/env python

##Copyright 2019 Thomas Paviot (tpaviot@gmail.com)
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

import os

from OCC.Core.Graphic3d import (Graphic3d_NOM_BRASS,
                                Graphic3d_NOM_BRONZE,
                                Graphic3d_NOM_COPPER,
                                Graphic3d_NOM_GOLD,
                                Graphic3d_NOM_PEWTER,
                                Graphic3d_NOM_PLASTER,
                                Graphic3d_NOM_PLASTIC,
                                Graphic3d_NOM_SILVER,
                                Graphic3d_NOM_STEEL,
                                Graphic3d_NOM_STONE,
                                Graphic3d_NOM_SHINY_PLASTIC,
                                Graphic3d_NOM_SATIN,
                                Graphic3d_NOM_METALIZED,
                                Graphic3d_NOM_NEON_GNC,
                                Graphic3d_NOM_CHROME,
                                Graphic3d_NOM_ALUMINIUM,
                                Graphic3d_NOM_OBSIDIAN,
                                Graphic3d_NOM_NEON_PHC,
                                Graphic3d_NOM_JADE,
                                Graphic3d_NOM_CHARCOAL,
                                Graphic3d_NOM_WATER,
                                Graphic3d_NOM_GLASS,
                                Graphic3d_NOM_DIAMOND,
                                Graphic3d_NOM_TRANSPARENT,
                                Graphic3d_NOM_DEFAULT,
                                Graphic3d_NOM_UserDefined)
from OCC.Core.gp import gp_Vec
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeCylinder
from OCC.Extend.ShapeFactory import translate_shp
from OCC.Display.SimpleGui import init_display

display, start_display, add_menu, add_function_to_menu = init_display()

# User defined material names should be chosen among
available_materials = [Graphic3d_NOM_BRASS,
                       Graphic3d_NOM_BRONZE,
                       Graphic3d_NOM_COPPER,
                       Graphic3d_NOM_GOLD,
                       Graphic3d_NOM_PEWTER,
                       Graphic3d_NOM_PLASTER,
                       Graphic3d_NOM_PLASTIC,
                       Graphic3d_NOM_SILVER,
                       Graphic3d_NOM_STEEL,
                       Graphic3d_NOM_STONE,
                       Graphic3d_NOM_SHINY_PLASTIC,
                       Graphic3d_NOM_SATIN,
                       Graphic3d_NOM_METALIZED,
                       Graphic3d_NOM_NEON_GNC,
                       Graphic3d_NOM_CHROME,
                       Graphic3d_NOM_ALUMINIUM,
                       Graphic3d_NOM_OBSIDIAN,
                       Graphic3d_NOM_NEON_PHC,
                       Graphic3d_NOM_JADE,
                       Graphic3d_NOM_CHARCOAL,
                       Graphic3d_NOM_WATER,
                       Graphic3d_NOM_GLASS,
                       Graphic3d_NOM_DIAMOND,
                       Graphic3d_NOM_TRANSPARENT,
                       Graphic3d_NOM_DEFAULT,
                       Graphic3d_NOM_UserDefined]

# 
# Displays a cylinder with a material
#
radius = 30
s = BRepPrimAPI_MakeCylinder(radius, 200).Shape()
delta_x = 0.
for mat in available_materials:
    s2 = translate_shp(s, gp_Vec(delta_x, 0., 0.))
    display.DisplayShape(s2, material=mat)
    delta_x += 2 * radius + 1.

display.FitAll()
start_display()
