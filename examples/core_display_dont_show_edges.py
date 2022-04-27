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

"""
The very first pythonocc example. This used to be the script
used to check the following points:

pythonocc installation is correct, i.e. pythonocc modules are found
and properly imported

a GUI manager is installed. Whether it is wxpython or pyqt/pyside, it's necessary
to display a 3d window

the rendering window can be initialized and set up, that is to say the
graphic driver and OpenGl works correctly.

If this example runs on your machine, that means you're ready to explore the wide
pythonocc world and run all the other examples.
"""

from OCC.Display.SimpleGui import init_display
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeBox

display, start_display, add_menu, add_function_to_menu = init_display()
my_box = BRepPrimAPI_MakeBox(10.0, 20.0, 30.0).Shape()

display.default_drawer.SetFaceBoundaryDraw(False)
display.DisplayShape(my_box, update=True)
start_display()
