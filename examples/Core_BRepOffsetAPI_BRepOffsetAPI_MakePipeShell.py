from OCC.Display.SimpleGui import init_display
from OCC.Core.BRepOffsetAPI import BRepOffsetAPI_MakePipeShell
from OCC.Core.Geom import Geom_BezierCurve
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeEdge, BRepBuilderAPI_MakeWire
from OCC.Core.TColgp import TColgp_Array1OfPnt
from OCC.Core.Law import Law_Linear
from OCC.Core.gp import *

display, start_display, add_menu, add_function_to_menu = init_display()

# Main function 
def Thicken_spline(event=None): 
    # Creation of points for the spine  
    array = TColgp_Array1OfPnt(1, 5)
    array.SetValue(1, gp_Pnt(1, 4,0))
    array.SetValue(2, gp_Pnt(2, 2,0))
    array.SetValue(3, gp_Pnt(3, 3,0))
    array.SetValue(4, gp_Pnt(4, 3,0))
    array.SetValue(5, gp_Pnt(5, 5,0))
  
    # Creation of a Bezier Curve as the spine
    Bz_curv = Geom_BezierCurve(array)
    Bz_curv_Edge = BRepBuilderAPI_MakeEdge(Bz_curv).Edge()
    Bz_curv_Wire = BRepBuilderAPI_MakeWire(Bz_curv_Edge).Wire()

    display.DisplayShape(Bz_curv_Wire)
    
    # Creation of profile to sweep along the spine 
    circle = gp_Circ(gp_ZOX(), 1)
    circle.SetLocation(array[0])

    circle_Edge = BRepBuilderAPI_MakeEdge(circle).Edge()
    circle_Wire = BRepBuilderAPI_MakeWire(circle_Edge).Wire()
    
    # Creation of the law to dictate the evolution of the profile
    brep1  =BRepOffsetAPI_MakePipeShell(Bz_curv_Wire)
    Law_f = Law_Linear()
    Law_f.Set(0,0.5,1,1)

    brep1.SetLaw(circle_Wire,Law_f,False, True)
    return brep1.Shape() 

# Display section 
if __name__ == '__main__':
   
    display.DisplayShape(Thicken_spline())

    start_display()

