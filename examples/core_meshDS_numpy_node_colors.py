"""
Example for the usage of MeshDS_DataSource providing a triangular mesh with vertices and faces from numpy arrays.
Faces are colored by their Z-Value (Interleaved between their nodes).

Example provided by Simon Klein (simon.klein@outlook.com) with snippets from other examples by Thomas Paviot
"""

import numpy as np
from scipy.spatial import Delaunay
from OCC.Core.MeshDS import MeshDS_DataSource
from OCC.Core.MeshVS import (
    MeshVS_DMF_OCCMask,
    MeshVS_Mesh,
    MeshVS_NodalColorPrsBuilder,
    MeshVS_DA_ShowEdges,
    MeshVS_DMF_NodalColorDataPrs,
)
from OCC.Display.SimpleGui import init_display
from OCC.Core.Aspect import Aspect_SequenceOfColor
from OCC.Core.Quantity import (
    Quantity_NOC_PURPLE,
    Quantity_NOC_ORANGE,
    Quantity_NOC_GREEN,
    Quantity_Color,
    Quantity_NOC_RED,
    Quantity_NOC_BLUE1,
    Quantity_NOC_BLACK,
)
from OCC.Core.TColStd import TColStd_DataMapOfIntegerReal


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

# Create the datasource. Data is taken directly from the numpy arrays. both have to be contiguous and Nx3 (double), Mx3 (int).
mesh_ds = MeshDS_DataSource(vertices, faces)

# Create the visualizer for the datasource
mesh_vs = MeshVS_Mesh()
mesh_vs.SetDataSource(mesh_ds)

# create nodal builder and assign to the mesh
node_builder = MeshVS_NodalColorPrsBuilder(
    mesh_vs, MeshVS_DMF_NodalColorDataPrs | MeshVS_DMF_OCCMask
)
node_builder.UseTexture(True)

# prepare color map
aColorMap = Aspect_SequenceOfColor()
aColorMap.Append(Quantity_Color(Quantity_NOC_PURPLE))
aColorMap.Append(Quantity_Color(Quantity_NOC_BLUE1))
aColorMap.Append(Quantity_Color(Quantity_NOC_GREEN))
aColorMap.Append(Quantity_Color(Quantity_NOC_ORANGE))

# assign color scale map values (0..1) to nodes
aScaleMap = TColStd_DataMapOfIntegerReal()

# set normalized color intensity to node
z_min = np.min(vertices[:, 2])
z_ptp = np.ptp(vertices[:, 2])
for nVert in range(vertices.shape[0]):
    color = (vertices[nVert, 2] - z_min) / z_ptp
    aScaleMap.Bind(nVert + 1, color)  # node indices are 1 based

# pass color map and color scale values to the builder
node_builder.SetColorMap(aColorMap)
node_builder.SetInvalidColor(Quantity_Color(Quantity_NOC_BLACK))
node_builder.SetTextureCoords(aScaleMap)
mesh_vs.AddBuilder(node_builder, True)

# get drawer to switch off edges
mesh_drawer = mesh_vs.GetDrawer()
mesh_drawer.SetBoolean(MeshVS_DA_ShowEdges, False)
mesh_vs.SetDrawer(mesh_drawer)

# Create the display and add visualization
display, start_display, add_menu, add_function_to_menu = init_display()
display.Context.Display(mesh_vs, True)
display.FitAll()
start_display()
