"""
Example for the usage of MeshDS_DataSource providing a triangular mesh with vertices and faces from numpy arrays.

Example provided by Simon Klein (simon.klein@outlook.com) with snippets from other examples by Thomas Paviot
"""

import numpy as np
from scipy.spatial import Delaunay
from OCC.Core.MeshDS import MeshDS_DataSource
from OCC.Core.MeshVS import *
from OCC.Display.SimpleGui import init_display


def getMesh(X=100, Y=100):
    # generate some mesh data.
    x = np.linspace(-5, 5, X)
    y = np.linspace(-5, 5, Y)
    xx, yy = np.meshgrid(x, y, sparse=False)
    z = np.sin(xx**2 + yy**2) / (xx**2 + yy**2)
    xyz = np.column_stack((xx.flatten(), yy.flatten(), z.flatten()))
    tri = Delaunay(xyz[:, :2])
    return xyz, tri.simplices


# get some mesh data
vertices, faces = getMesh()

# Create the datasource. Data is taken directly from the numpy arrays. both have to be contiguous.
mesh_ds = MeshDS_DataSource(vertices, faces)

# Create the visualizer for the datasource
mesh_vs = MeshVS_Mesh()
mesh_vs.SetDataSource(mesh_ds)

# Create a new presentation builder and add it to the visualizer
prs_builder = MeshVS_MeshPrsBuilder(mesh_vs)

# mesh_vs.SetDisplayMode(AIS_DisplayMode.AIS_Shaded)
mesh_vs.AddBuilder(prs_builder, True)

# Create the display and add visualization
display, start_display, add_menu, add_function_to_menu = init_display()
display.Context.Display(mesh_vs, True)
display.FitAll()
start_display()
