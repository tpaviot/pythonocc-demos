##Copyright 2010-2014 Thomas Paviot (tpaviot@gmail.com)
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
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeVertex
from OCC.Core.BRepLProp import BRepLProp_SLProps
from OCC.Core.BRepAdaptor import BRepAdaptor_Surface
from OCC.Core.TopExp import TopExp_Explorer
from OCC.Core.TopAbs import TopAbs_FACE
from OCC.Core.gp import gp_Pnt
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeTorus
from OCC.Core.Quantity import Quantity_Color, Quantity_TOC_RGB
from OCC.Display.SimpleGui import init_display
from OCC.Core.BRepTools import breptools

from OCC.Extend.TopologyUtils import TopologyExplorer


def calculate_mean_curvature_at_point(face, u, v):
    """
    Calculates the mean curvature at a point (u,v) on a face

    Args:
        face: BRep face
        u, v: UV parameters of the point

    Returns:
        float: Mean curvature at the point
    """
    # Create the local properties analyzer
    surf_adaptor = BRepAdaptor_Surface(face)
    props = BRepLProp_SLProps(surf_adaptor, 2, 1e-6)

    # Set UV parameters
    props.SetParameters(u, v)

    # Check if curvature is defined
    if props.IsCurvatureDefined():
        return props.MeanCurvature()

    return 0.0


def curvature_to_color(curvature, min_curv, max_curv):
    """
    Converts a curvature value to color (blue -> red)

    Args:
        curvature: Curvature value
        min_curv: Minimum curvature
        max_curv: Maximum curvature

    Returns:
        Quantity_Color: Corresponding color
    """
    if max_curv == min_curv:
        # Avoid division by zero
        normalized = 0.5
    else:
        # Normalize between 0 and 1
        normalized = (curvature - min_curv) / (max_curv - min_curv)
        normalized = max(0.0, min(1.0, normalized))  # Clamp between 0 and 1

    # Convert to color: blue (0) -> red (1)
    # Use a palette blue -> cyan -> green -> yellow -> red
    if normalized <= 0.25:
        # Blue to cyan
        t = normalized / 0.25
        r, g, b = 0.0, t, 1.0
    elif normalized <= 0.5:
        # Cyan to green
        t = (normalized - 0.25) / 0.25
        r, g, b = 0.0, 1.0, 1.0 - t
    elif normalized <= 0.75:
        # Green to yellow
        t = (normalized - 0.5) / 0.25
        r, g, b = t, 1.0, 0.0
    else:
        # Yellow to red
        t = (normalized - 0.75) / 0.25
        r, g, b = 1.0, 1.0 - t, 0.0

    return Quantity_Color(r, g, b, Quantity_TOC_RGB)


def analyze_curvature_grid(face, grid_size=20):
    """
    Analyzes curvature on a grid of points and returns statistics

    Args:
        face: Face to analyze
        grid_size: Number of points per direction

    Returns:
        tuple: (points, curvatures, min_curv, max_curv)
    """
    umin, umax, vmin, vmax = breptools.UVBounds(face)

    points = []
    curvatures = []

    # Create a grid of UV points
    u_vals = np.linspace(umin, umax, grid_size)
    v_vals = np.linspace(vmin, vmax, grid_size)

    for u in u_vals:
        for v in v_vals:
            curvature = calculate_mean_curvature_at_point(face, u, v)
            points.append((u, v))
            curvatures.append(curvature)

    if curvatures:
        min_curv = min(curvatures)
        max_curv = max(curvatures)
    else:
        min_curv = max_curv = 0.0

    return points, curvatures, min_curv, max_curv


def visualize_curvature_at_points(shape):
    """
    Visualizes curvature by displaying colored points according to their mean curvature
    """
    # Iterate through all faces
    # explorer = TopExp_Explorer(shape, TopAbs_FACE)
    explorer = TopologyExplorer(shape)

    for face in explorer.faces():  # while explorer.More():
        # face = explorer.Current()

        # Analyze curvature on this face
        points, curvatures, min_curv, max_curv = analyze_curvature_grid(
            face, grid_size=15
        )

        print("Face analyzed:")
        print(f"  Min curvature: {min_curv:.6f}")
        print(f"  Max curvature: {max_curv:.6f}")
        print(f"  Number of points: {len(points)}")
        surface_adaptor = BRepAdaptor_Surface(face)
        # Create the properties analyzer to get 3D coordinates
        props = BRepLProp_SLProps(surface_adaptor, 1, 1e-6)

        # Display each point with its curvature color
        for (u, v), curvature in zip(points, curvatures):
            props.SetParameters(u, v)
            if props.IsNormalDefined():
                point_3d = props.Value()
                color = curvature_to_color(curvature, min_curv, max_curv)

                # Display the point with the corresponding color
                display.DisplayColoredShape(
                    BRepBuilderAPI_MakeVertex(
                        gp_Pnt(point_3d.X(), point_3d.Y(), point_3d.Z())
                    ).Vertex(),
                    color,
                )


def calculate_curvature_at_specific_point(shape, u_param=0.5, v_param=0.5):
    """
    Calculates and displays curvature at a specific point

    Args:
        shape: Shape to analyze
        u_param: U parameter (between 0 and 1, relative to bounds)
        v_param: V parameter (between 0 and 1, relative to bounds)
    """
    explorer = TopExp_Explorer(shape, TopAbs_FACE)

    if explorer.More():
        face = explorer.Current()

        # Get UV bounds
        umin, umax, vmin, vmax = breptools.UVBounds(face)

        # Convert relative parameters to absolute parameters
        u = umin + u_param * (umax - umin)
        v = vmin + v_param * (vmax - vmin)

        # Calculate curvature
        mean_curvature = calculate_mean_curvature_at_point(face, u, v)

        # Get the corresponding 3D point
        surf_adaptor = BRepAdaptor_Surface(face)
        props = BRepLProp_SLProps(surf_adaptor, 2, 1e-6)
        props.SetParameters(u, v)

        if props.IsNormalDefined():
            point_3d = props.Value()
            normal = props.Normal()

            print(f"\nAnalysis at point (u={u:.3f}, v={v:.3f}):")
            print(
                f"  3D position: ({point_3d.X():.3f}, {point_3d.Y():.3f}, {point_3d.Z():.3f})"
            )
            print(f"  Mean curvature: {mean_curvature:.6f}")
            print(f"  Normal: ({normal.X():.3f}, {normal.Y():.3f}, {normal.Z():.3f})")

            if props.IsCurvatureDefined():
                gaussian_curv = props.GaussianCurvature()
                min_curv = props.MinCurvature()
                max_curv = props.MaxCurvature()

                print(f"  Gaussian curvature: {gaussian_curv:.6f}")
                print(f"  Minimum curvature: {min_curv:.6f}")
                print(f"  Maximum curvature: {max_curv:.6f}")

            # Mark the analyzed point
            marker = BRepBuilderAPI_MakeVertex(
                gp_Pnt(point_3d.X(), point_3d.Y(), point_3d.Z())
            ).Vertex()

            display.DisplayColoredShape(
                marker, Quantity_Color(1, 0, 1, Quantity_TOC_RGB)
            )  # Magenta

            return mean_curvature, point_3d

    return None, None


if __name__ == "__main__":
    display, start_display, add_menu, add_function_to_menu = init_display()

    # Create the test surface
    torus = BRepPrimAPI_MakeTorus(60, 15).Shape()

    # Calculate curvature at a specific point
    calculate_curvature_at_specific_point(torus, 0.3, 0.7)

    # Visualize curvature distribution
    visualize_curvature_at_points(torus)

    # Finally display the base shape
    display.DisplayShape(torus, transparency=0.7, update=True)
    start_display()
