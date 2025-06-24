##Copyright 2025 Thomas Paviot (tpaviot@gmail.com)
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

import numpy as np
from OCC.Core.gp import gp_Pnt
from OCC.Core.TColgp import TColgp_Array2OfPnt
from OCC.Core.GeomAPI import GeomAPI_PointsToBSplineSurface
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeFace
from OCC.Core.AIS import AIS_Shape
from OCC.Core.Quantity import Quantity_Color, Quantity_NOC_RED, Quantity_NOC_BLUE
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeEdge

from OCC.Display.SimpleGui import init_display


def create_complex_surface_points():
    """
    Creates a set of points defining a complex surface
    (e.g., a wavy surface)
    """
    # Grid dimensions for points
    u_points = 6
    v_points = 6

    points = []

    # Generate points for a complex wavy surface
    for i in range(u_points):
        row = []
        for j in range(v_points):
            # Normalized parameters
            u = i / (u_points - 1)
            v = j / (v_points - 1)

            # Base coordinates
            x = u * 10.0
            y = v * 10.0

            # Complex surface with undulations
            z = (
                2.0 * np.sin(2 * np.pi * u) * np.cos(2 * np.pi * v)
                + 1.0 * np.sin(4 * np.pi * u)
                + 0.5 * np.cos(6 * np.pi * v)
                + 0.3 * np.sin(8 * np.pi * u * v)
            )

            row.append(gp_Pnt(x, y, z))
        points.append(row)

    return points, u_points, v_points


def points_to_bspline_surface(points, u_points, v_points):
    """
    Converts a point array to a B-spline surface
    """
    # Create 2D point array for OCC
    points_array = TColgp_Array2OfPnt(1, u_points, 1, v_points)

    for i in range(u_points):
        for j in range(v_points):
            points_array.SetValue(i + 1, j + 1, points[i][j])

    # Create B-spline surface
    surface_builder = GeomAPI_PointsToBSplineSurface(points_array)

    if not surface_builder.IsDone():
        raise Exception("Unable to create B-spline surface")

    return surface_builder.Surface()


def create_iso_curves(surface, num_u_iso=10, num_v_iso=10):
    """
    Creates U and V isoparametric curves on the surface
    """
    # Get parametric bounds of the surface
    u_min, u_max, v_min, v_max = surface.Bounds()

    iso_curves = []

    # U isoparametric curves (constant V)
    for i in range(num_v_iso):
        v_param = v_min + (v_max - v_min) * i / (num_v_iso - 1)
        iso_u = surface.VIso(v_param)
        edge = BRepBuilderAPI_MakeEdge(iso_u, u_min, u_max).Edge()
        iso_curves.append(("U", edge))

    # V isoparametric curves (constant U)
    for i in range(num_u_iso):
        u_param = u_min + (u_max - u_min) * i / (num_u_iso - 1)
        iso_v = surface.UIso(u_param)
        edge = BRepBuilderAPI_MakeEdge(iso_v, v_min, v_max).Edge()
        iso_curves.append(("V", edge))

    return iso_curves


if __name__ == "__main__":

    points, u_points, v_points = create_complex_surface_points()
    surface = points_to_bspline_surface(points, u_points, v_points)

    display, start_display, add_menu, add_function_to_menu = init_display()

    # Create surface points
    points, u_points, v_points = create_complex_surface_points()

    print(f"Surface created with {u_points}x{v_points} control points")

    # Create B-spline surface
    surface = points_to_bspline_surface(points, u_points, v_points)

    # Create face from surface
    face = BRepBuilderAPI_MakeFace(surface, 1e-6).Face()

    # Create and display isoparametric curves
    iso_curves = create_iso_curves(surface, num_u_iso=8, num_v_iso=8)

    print(f"Creating {len(iso_curves)} isoparametric curves")

    # Display isoparametric curves with different colors
    for curve_type, edge in iso_curves:
        if curve_type == "U":
            # Red for iso-U curves
            display.DisplayShape(edge, color=Quantity_NOC_RED)
        else:
            # Blue for iso-V curves
            display.DisplayShape(edge, color=Quantity_NOC_BLUE)

    # Display control points (optional)
    for i in range(u_points):
        for j in range(v_points):
            display.DisplayShape(points[i][j])

    # Display surface
    display.DisplayShape(face, transparency=0.9, update=True)

    # Start display loop
    start_display()
