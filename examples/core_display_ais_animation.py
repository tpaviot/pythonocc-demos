#!/usr/bin/env python

##Copyright 2023 KimPyoungGang (fgdr159@naver.com)
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

# Small example how to use the AIS_Animation for pythonocc

  
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeBox
from OCC.Core.gp import gp_Trsf
from OCC.Core.AIS import AIS_Animation, AIS_AnimationObject
from OCC.Display.SimpleGui import init_display
from OCC.Core.TCollection import TCollection_AsciiString

display, start_display, add_menu, add_function_to_menu = init_display()

obj1 = BRepPrimAPI_MakeBox(100, 500, 20).Shape()
test = display.DisplayShape(obj1)[0]

def run(event=None):
    
    start_pnt = gp_Trsf()
    end_pnt = gp_Trsf()

    start_pnt.SetValues(1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0)
    end_pnt.SetValues(1, 0, 0, 100, 0, 1, 0, 100, 0, 0, 1, 100)

    s = TCollection_AsciiString("Hello, OpenCASCADE!")
    ais_animation = AIS_Animation(s)

    ais_ao = AIS_AnimationObject(s, display.Context, test, start_pnt, end_pnt)

    ais_ao.SetOwnDuration(10)
    ais_ao.SetStartPts(0)

    ais_animation.Add(ais_ao)
    duration = ais_animation.Duration()
    ais_animation.StartTimer(0, 1.0, True)

    # Update viewer
    while not ais_animation.IsStopped():
        ais_animation.UpdateTimer()
        display.Context.UpdateCurrentViewer()


if __name__ == "__main__":
    add_menu("Animation")
    add_function_to_menu("Animation", run)
    display.FitAll()
    start_display()
