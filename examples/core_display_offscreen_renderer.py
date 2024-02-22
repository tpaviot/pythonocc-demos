from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeBox

from OCC.Display.OCCViewer import OffscreenRenderer

a_box_shape = BRepPrimAPI_MakeBox(10, 20, 30).Shape()

my_renderer = OffscreenRenderer()
my_renderer.DisplayShape(a_box_shape)

my_renderer2 = OffscreenRenderer()
my_renderer2.DisplayShape(a_box_shape, dump_image_path='.', dump_image_filename='my_capture.png')
my_renderer2.DisplayShape(a_box_shape, dump_image_path='.', dump_image_filename='my_capture.ppm')
my_renderer2.DisplayShape(a_box_shape, dump_image_path='.', dump_image_filename='my_capture.jpg')
