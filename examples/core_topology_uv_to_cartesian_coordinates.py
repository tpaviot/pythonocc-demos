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

from OCC.Core.gp import gp_Pnt
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeFace
from OCC.Core.TColgp import TColgp_Array2OfPnt
from OCC.Core.GeomAPI import GeomAPI_PointsToBSplineSurface
from OCC.Core.GeomAbs import GeomAbs_C2
from OCC.Core.ShapeAnalysis import ShapeAnalysis_Surface, shapeanalysis_GetFaceUVBounds

from OCC.Display.SimpleGui import init_display
display, start_display, add_menu, add_function_to_menu = init_display()


def build_surf():
    p1 = gp_Pnt(-15, 200, 10)
    p2 = gp_Pnt(5, 204, 0)
    p3 = gp_Pnt(15, 200, 0)
    p4 = gp_Pnt(-15, 20, 15)
    p5 = gp_Pnt(-5, 20, 0)
    p6 = gp_Pnt(15, 20, 35)

    array = TColgp_Array2OfPnt(1, 3, 1, 2)
    array.SetValue(1, 1, p1)
    array.SetValue(2, 1, p2)
    array.SetValue(3, 1, p3)
    array.SetValue(1, 2, p4)
    array.SetValue(2, 2, p5)
    array.SetValue(3, 2, p6)
    bspl_surf = GeomAPI_PointsToBSplineSurface(array, 3, 8, GeomAbs_C2,
                                               0.001).Surface()
    return bspl_surf

def build_points_network(bspl_srf):
    """ Creates a list of gp_Pnt points from a bspline surface
    """
    # first create a face
    face = BRepBuilderAPI_MakeFace(bspl_srf, 1e-6).Face()
    # get face uv bounds
    umin, umax, vmin, vmax = shapeanalysis_GetFaceUVBounds(face)
    print(umin, umax, vmin, vmax)

    pnts = []
    sas = ShapeAnalysis_Surface(bspl_srf)

    u = umin
    while u < umax:
        v = vmin
        while v < vmax:
            p = sas.Value(u, v)
            print("u=", u, " v=", v, "->X=", p.X(), " Y=", p.Y(), " Z=", p.Z())
            pnts.append(p)
            v += 0.1
        u += 0.1
    return pnts

if __name__ == '__main__':
    surf = build_surf()
    display.DisplayShape(surf, update=True)
    pts = build_points_network(surf)
    for pt in pts:
        display.DisplayShape(pt, update=True)
    start_display()
