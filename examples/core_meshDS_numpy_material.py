"""
Example for the usage of MeshDS_DataSource providing a triangular mesh with vertices and faces from numpy arrays.

Example provided by Simon Klein (simon.klein@outlook.com) with snippets from other examples by Thomas Paviot
"""

import numpy as np
from scipy.spatial import Delaunay
from OCC.Core.MeshDS import MeshDS_DataSource
from OCC.Core.MeshVS import *
from OCC.Display.SimpleGui import init_display
from OCC.Core.Quantity import (
    Quantity_NOC_GREEN,
    Quantity_Color,
)

from OCC.Core.Graphic3d import (
    Graphic3d_MaterialAspect,
    Graphic3d_PBRMaterial,
    Graphic3d_NOM_STEEL,
)


def getMesh(X=100, Y=100):
    # generate some mesh data.
    x = np.linspace(-5, 5, X)
    y = np.linspace(-5, 5, Y)
    xx, yy = np.meshgrid(x, y, sparse=False)
    z = np.sin(xx ** 2 + yy ** 2) / (xx ** 2 + yy ** 2)
    xyz = np.column_stack((xx.flatten(), yy.flatten(), z.flatten()))
    tri = Delaunay(xyz[:, :2])
    return xyz, tri.simplices


# get some mesh data
vertices, faces = getMesh()

mesh_ds = MeshDS_DataSource(vertices, faces)

# Create the visualizer for the datasource
mesh_vs = MeshVS_Mesh()
mesh_vs.SetDataSource(mesh_ds)

# Create a new presentation builder and add it to the visualizer
prs_builder = MeshVS_MeshPrsBuilder(mesh_vs)

# Create a material
color = Quantity_Color(Quantity_NOC_GREEN)

pbr_mat = Graphic3d_PBRMaterial()
mat = Graphic3d_MaterialAspect(Graphic3d_NOM_STEEL)
mat.SetPBRMaterial(pbr_mat)
mat.SetColor(color)

# Set visuals
drawer = prs_builder.GetDrawer()
drawer.SetBoolean(MeshVS_DA_ShowEdges, False)
drawer.SetBoolean(MeshVS_DA_DisplayNodes, False)
drawer.SetMaterial(MeshVS_DA_FrontMaterial, mat)
prs_builder.SetDrawer(drawer)

# Add the builder to the visualizer
mesh_vs.AddBuilder(prs_builder, True)
mesh_vs.SetDisplayMode(MeshVS_DMF_Shading)

# Create the display and add visualization
display, start_display, add_menu, add_function_to_menu = init_display()
display.Context.Display(mesh_vs, True)
display.FitAll()
start_display()
