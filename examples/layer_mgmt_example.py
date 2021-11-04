from OCC.Display.SimpleGui import init_display
display,start_display, add_menu,add_functionto_menu = init_display()
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeBox

box = BRepPrimAPI_MakeBox(10,10,100).Shape()
box2 = BRepPrimAPI_MakeBox(100,10,10).Shape()
box3 = BRepPrimAPI_MakeBox(10,100,10).Shape()

class Layer():

    def __init__(self):
        self.clear()

    def create(self, shape, color=0):
        self.color = color
        self.to_display = display.DisplayShape(shape, color=self.color)[0]
        self.count += 1
        self.list_to_display.append(self.to_display)
        display.Context.Erase(self.to_display, False)

    def show(self):
        for shape in self.list_to_display:
            display.Context.Display(shape, True)

    def hide(self):
        for shape in self.list_to_display:
            display.Context.Erase(shape, False)

    def add(self, shape):
        self.to_display = {self.count}
        self.to_display = display.DisplayShape(shape, color=self.color)[0]
        self.list_to_display.append(self.to_display)
        display.Context.Erase(self.to_display, False)

    def clear(self):
        self.list_to_display = []
        self.count = 0
        self.to_display = {self.count}


layer1 = Layer()
layer1.create(box)
layer1.add(box2)
layer1.show()

layer2 = Layer()
layer2.create(box3, 123)
layer2.show()

display.FitAll()
start_display()
