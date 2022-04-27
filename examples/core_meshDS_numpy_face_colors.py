"""
Example for the usage of MeshDS_DataSource providing a triangular mesh with vertices and faces from numpy arrays.
Faces are colored by individually by the mean z-value of their vertices (Interleaved between their nodes).

Example provided by Simon Klein (simon.klein@outlook.com) with snippets from other examples by Thomas Paviot
"""

import numpy as np
from scipy.spatial import Delaunay
from matplotlib import cm
from OCC.Core.MeshDS import MeshDS_DataSource
from OCC.Core.MeshVS import MeshVS_DMF_OCCMask, MeshVS_Mesh, MeshVS_ElementalColorPrsBuilder, MeshVS_DA_ShowEdges, MeshVS_DMF_ElementalColorDataPrs, MeshVS_DataMapOfIntegerColor
from OCC.Display.SimpleGui import init_display
from OCC.Core.Quantity import Quantity_Color, Quantity_TOC_RGB


def getMesh(X=100, Y=100):
    # generate some mesh data.
    x = np.linspace(-5, 5, X)
    y = np.linspace(-5, 5, Y)
    xx, yy = np.meshgrid(x, y, sparse=False)
    z = (np.sin(xx**2 + yy**2) / (xx**2 + yy**2))
    xyz = np.column_stack((xx.flatten(), yy.flatten(), z.flatten()))
    tri = Delaunay(xyz[:, :2])
    return xyz, tri.simplices

#get some mesh data
vertices, faces = getMesh()

# generate face values
cmap = cm.get_cmap("viridis")
face_values = np.mean(vertices[faces, 2], axis=-1)
z_min = np.min(vertices[:, 2])
z_ptp = np.ptp(vertices[:, 2])

face_colors = [cmap((value - z_min)/z_ptp)[:3] for value in face_values]

# Create the datasource. Data is taken directly from the numpy arrays. both have to be contiguous and Nx3 (double), Mx3 (int).
mesh_ds = MeshDS_DataSource(vertices, faces)

# Create the visualizer for the datasource
mesh_vs = MeshVS_Mesh()
mesh_vs.SetDataSource(mesh_ds)

# create nodal builder and assign to the mesh
element_builder = MeshVS_ElementalColorPrsBuilder(mesh_vs, MeshVS_DMF_ElementalColorDataPrs | MeshVS_DMF_OCCMask)

# set normalized color intensity to node
for nFace in range(faces.shape[0]):
    color = Quantity_Color(*face_colors[nFace], Quantity_TOC_RGB)
    element_builder.SetColor1(nFace+1, color) #element indices are 1 based

# Add the builder to the visualizer
mesh_vs.AddBuilder(element_builder, True)

# get drawer to switch off edges
mesh_drawer = mesh_vs.GetDrawer()
mesh_drawer.SetBoolean(MeshVS_DA_ShowEdges, False)
mesh_vs.SetDrawer(mesh_drawer)

# Create the display and add visualization
display, start_display, add_menu, add_function_to_menu = init_display()
display.Context.Display(mesh_vs, True)
display.FitAll()
start_display()
