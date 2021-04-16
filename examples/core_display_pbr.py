##Copyright 2021 Thomas Paviot (tpaviot@gmail.com)
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

import sys

from OCC.Display.SimpleGui import init_display
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeBox, BRepPrimAPI_MakeCone
from OCC.Core.Graphic3d import (Graphic3d_NOM_PLASTIC, Graphic3d_NOM_ALUMINIUM,
                                Graphic3d_TOSM_PBR, Graphic3d_TOSM_PBR_FACET,
                                Graphic3d_TOSM_FRAGMENT, Graphic3d_TOSM_VERTEX,
                                Graphic3d_PBRMaterial, Graphic3d_MaterialAspect)
from OCC.Core.V3d import V3d_SpotLight, V3d_XnegYnegZpos, V3d_AmbientLight, V3d_DirectionalLight
from OCC.Core.Quantity import Quantity_Color, Quantity_NOC_WHITE, Quantity_NOC_CORAL2, Quantity_NOC_BROWN, Quantity_NOC_GRAY
from OCC.Core.BRepAlgoAPI import BRepAlgoAPI_Cut
from OCC.Core.gp import gp_Vec, gp_Pnt, gp_Dir

from OCC.Extend.ShapeFactory import translate_shp

# first create geometry
from core_classic_occ_bottle import bottle
table = translate_shp(BRepPrimAPI_MakeBox(100, 100, 10).Shape(), gp_Vec(-50, -50, -10))
glass_out = BRepPrimAPI_MakeCone(7, 9, 25).Shape()
glass_in = translate_shp(BRepPrimAPI_MakeCone(7, 9, 25).Shape(), gp_Vec(0., 0., 0.2))
glass = BRepAlgoAPI_Cut(glass_out, glass_in).Shape()
translated_glass = translate_shp(glass, gp_Vec(-30, -30, 0))

# then inits display
display, start_display, add_menu, add_function_to_menu = init_display()

# ambient light
ambient_light = V3d_AmbientLight(Quantity_Color(Quantity_NOC_WHITE))
display.Viewer.AddLight(ambient_light)

# directional light
dir_light = V3d_DirectionalLight(gp_Dir(0,0,1), Quantity_Color(Quantity_NOC_WHITE))
display.Viewer.AddLight(dir_light)

# create one spotlight
spot_light = V3d_SpotLight(gp_Pnt(-100, -100, 100),
                           V3d_XnegYnegZpos, Quantity_Color(Quantity_NOC_WHITE))
## display the spotlight in rasterized mode
display.Viewer.AddLight(spot_light)

display.View.SetLightOn()

# first create the PBR material
pbr_mat = Graphic3d_PBRMaterial()
print(dir(pbr_mat))
pbr_mat.SetMetallic(0.8)
pbr_mat.SetRoughness(0.5)
# modifies albedo color
#pbr_mat.SetColor(Quantity_Color(Quantity_NOC_GRAY))

# then the material aspect
alu_pbr_aspect = Graphic3d_MaterialAspect(Graphic3d_NOM_ALUMINIUM)
alu_pbr_aspect.SetPBRMaterial(pbr_mat)

#print(dir(pbr_mat))
display.EnableAntiAliasing()
display.DisplayShape(bottle, material=alu_pbr_aspect)
display.DisplayShape(table, material=Graphic3d_NOM_PLASTIC, color=Quantity_NOC_CORAL2)
display.DisplayShape(translated_glass,
                     material=Graphic3d_NOM_PLASTIC,
                     color=Quantity_NOC_BROWN,
                     transparency=0.6,
                     update=True)

def pbr(event=None):
    display.View.SetShadingModel(Graphic3d_TOSM_PBR)
    display.View.Redraw()

def pbr_facet(event=None):
    display.View.SetShadingModel(Graphic3d_TOSM_PBR_FACET)
    display.View.Redraw()

def phong(event=None):
    display.View.SetShadingModel(Graphic3d_TOSM_VERTEX)
    display.View.Redraw()

def gouraud(event=None):
    display.View.SetShadingModel(Graphic3d_TOSM_FRAGMENT)
    display.View.Redraw()

def rasterization(event=None):
    display.SetRasterizationMode()
    display.View.Redraw()

def exit(event=None):
    sys.exit(0)


#display.View.GeneratePBREnvironment(True)

if __name__ == '__main__':
    add_menu('PBR')
    add_function_to_menu('PBR', rasterization)
    add_function_to_menu('PBR', gouraud)
    add_function_to_menu('PBR', phong)
    add_function_to_menu('PBR', pbr)
    add_function_to_menu('PBR', pbr_facet)
    start_display()
