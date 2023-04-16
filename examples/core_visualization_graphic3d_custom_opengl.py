from __future__ import print_function

import random
import warnings

from OCC.Core.Aspect import Aspect_TOL_SOLID
from OCC.Display.SimpleGui import init_display
from OCC.Core.Graphic3d import Graphic3d_ArrayOfPolylines, Graphic3d_AspectLine3d
from OCC.Core.Prs3d import Prs3d_Root_CurrentGroup
from OCC.Core.Quantity import Quantity_NOC_BLACK, Quantity_Color
from OCC.Core.gp import gp_Pnt
from OCC.Core.Graphic3d import Graphic3d_Structure


def create_ogl_group(display):
    """
    create a group that will store an OpenGL buffer
    """
    aStructure = Graphic3d_Structure(display._struc_mgr)
    group = Prs3d_Root_CurrentGroup(aStructure)
    return aStructure, group


def generate_points(spread, n):
    try:
        import numpy as np

        yield from np.random.uniform(-spread / 2.0, spread / 2.0, (n, 3))
    except ImportError:
        n_ = n / 100
        warnings.warn(
            f"Numpy could not be imported... this example will run very SLOWdrawing {n_} rather than {n} lines"
        )
        for _ in range(n_):
            a = random.uniform(-spread / 2.0, spread / 2.0)
            b = random.uniform(-spread / 2.0, spread / 2.0)
            c = random.uniform(-spread / 2.0, spread / 2.0)
            yield (a, b, c)


def draw_lines(pnt_list, nr_of_points, display):
    """

    rendering a large number of points through the usual way of:

        display.DisplayShape( make_vertex( gp_Pnt() ) )

    is fine for TopoDS_Shapes but certainly not for large number of points.
    in comparison, drawing all the voxel samples takes 18sec using the approach above, but negigable when using this function
    its about 2 orders of Magnitude faster, so worth the extra hassle

    here we use a more close-to-the-metal approach of drawing directly in OpenGL

    see [1] for a more detailed / elegant way to perform this task

    [1] http://www.opencascade.org/org/forum/thread_21732/?forum=3

    Parameters
    ----------

    pnt_list: list of (x,y,z) tuples
        vertex list

    display: qtViewer3d

    """

    a_presentation, group = create_ogl_group(display)
    black = Quantity_Color(Quantity_NOC_BLACK)
    asp = Graphic3d_AspectLine3d(black, Aspect_TOL_SOLID, 1)

    gg = Graphic3d_ArrayOfPolylines(
        nr_of_points * 2, nr_of_points * 2, 0, False, True  # maxEdges  # hasVColors
    )

    try:
        while 1:
            pnt = gp_Pnt(*next(pnt_list))
            gg.AddVertex(pnt)
            pnt = gp_Pnt(*next(pnt_list))
            gg.AddVertex(pnt)
            # create the line, with a random color
            gg.AddBound(2, random.random(), random.random(), random.random())

    except StopIteration:
        pass

    group.SetPrimitivesAspect(asp)
    group.AddPrimitiveArray(gg)
    a_presentation.Display()


display, start_display, add_menu, add_function_to_menu = init_display()
nr_of_points = 100000
spread = 100
draw_lines(generate_points(spread, nr_of_points), nr_of_points, display)
start_display()
