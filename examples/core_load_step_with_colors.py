##Copyright 2010-2014 Thomas Paviot (tpaviot@gmail.com)
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

from OCC.Extend.DataExchange import read_step_file_with_names_colors
from OCC.Core.Quantity import Quantity_Color, Quantity_TOC_RGB
from OCC.Display.SimpleGui import init_display

filename = '../assets/models/as1-oc-214.stp'
#filename = '../assets/models/Personal_Computer.stp'
#filename = '../assets/models/KR600_R2830-4.stp'
#filename = '../assets/models/mod-mpu9150.step'
shapes_labels_colors = read_step_file_with_names_colors(filename)

# init graphic display
display, start_display, add_menu, add_function_to_menu = init_display()

for shpt_lbl_color in shapes_labels_colors:
    label, c = shapes_labels_colors[shpt_lbl_color]
    display.DisplayColoredShape(shpt_lbl_color, color=Quantity_Color(c.Red(),
    	                                                             c.Green(),
    	                                                             c.Blue(),
    	                                                             Quantity_TOC_RGB))
start_display()
