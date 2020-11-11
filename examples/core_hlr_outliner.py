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


from OCC.Display.SimpleGui import init_display
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeBox
from OCC.Core.HLRTopoBRep import HLRTopoBRep_OutLiner
from OCC.Core.BRepTools import breptools_Read
from OCC.Core.TopoDS import TopoDS_Shape
from OCC.Core.BRep import BRep_Builder
from OCC.Core.HLRBRep import HLRBRep_Algo, HLRBRep_HLRToShape

cylinder_head = TopoDS_Shape()
outt = TopoDS_Shape()
builder = BRep_Builder()
breptools_Read(cylinder_head, '../assets/models/cylinder_head.brep', builder)

myAlgo = HLRBRep_Algo()
myAlgo.Add(cylinder_head)
myAlgo.Update()

print(dir(HLRBRep_HLRToShape))
aHLRToShape=HLRBRep_HLRToShape(myAlgo)
o = aHLRToShape.OutLineVCompound3d()
display, start_display, add_menu, add_function_to_menu = init_display('qt-pyqt5')
display.DisplayShape(o, update=True)
start_display()
