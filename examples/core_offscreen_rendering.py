##Copyright 2017 Thomas Paviot (tpaviot@gmail.com)
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

from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeBox
from OCC.Core.Graphic3d import Graphic3d_BufferType
from OCC.Display.OCCViewer import Viewer3d

# create the renderer
offscreen_renderer = Viewer3d()
# by default, the offscreenrenderer size is 640*480
offscreen_renderer.Create()
offscreen_renderer.SetModeShaded()

# then the shape
my_box = BRepPrimAPI_MakeBox(10., 20., 30.).Shape()

# send the shape to the renderer
offscreen_renderer.DisplayShape(my_box, update=True)

# export to a 640*480 image data
data_640_480 = offscreen_renderer.GetImageData(640, 480, Graphic3d_BufferType.Graphic3d_BT_Depth)

# the same image to 1024*768
data_1024_768 = offscreen_renderer.GetImageData(1024, 768, Graphic3d_BufferType.Graphic3d_BT_Depth)

# be aware that the data_1024_768 image above is
# just a zoom of the 640*480 image.

# a better result can be obtained below
# export the view to image
offscreen_renderer.View.Dump('./capture_640_480_jpeg.jpeg')

# then resize the renderer
offscreen_renderer.SetSize(1024, 768)
offscreen_renderer.View.Dump('./capture_1024_768_jpeg.jpeg')

# the second solution produces a better image but need a resize event, it's a bit longer.
