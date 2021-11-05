from OCC.Display.SimpleGui import init_display
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeBox
from OCC.Core.gp import gp_Pnt, gp_Vec, gp_Trsf
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_Transform
from OCC.Extend.LayerMgmt import Layer
display,start_display, add_menu,add_functionto_menu = init_display()

box1 = BRepPrimAPI_MakeBox(gp_Pnt(0, 0, 10), 10, 10, 100).Shape()
box2 = BRepPrimAPI_MakeBox(gp_Pnt(), 100, 10, 10).Shape()
box3 = BRepPrimAPI_MakeBox(10, 100, 10).Shape()
box4 = BRepPrimAPI_MakeBox(gp_Pnt(100, 100, 0), 10, 10, 100).Shape()
box5 = BRepPrimAPI_MakeBox(gp_Pnt(0, 100, 0), 100, 10, 10).Shape()
box6 = BRepPrimAPI_MakeBox(gp_Pnt(100, 0, 0), 10, 100, 10).Shape()
trns = gp_Trsf()
trns.SetTranslation(gp_Vec(0, 0, 110))

layer1 = Layer(display, color=123)
layer1.add(box1)

layer2 = Layer(display, box4, 86)
layer2.add(box5)
layer2.show()

layer3 = Layer(display, box2, 76)
layer3.add(box3)
layer3.add(box6)

layer3.join(layer1, True)
layer3.show()
layer3_shapes = layer3.get_shapes()
layer4 = Layer(display, color=32)
for shape in layer3_shapes:
    translated = BRepBuilderAPI_Transform(shape, trns).Shape()
    layer4.add(translated)
layer4.show()

display.FitAll()
start_display()
