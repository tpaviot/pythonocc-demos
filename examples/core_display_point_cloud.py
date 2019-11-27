#!/usr/bin/env python

##Copyright 2016 Thomas Paviot (tpaviot@gmail.com)
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

import os
import random
import struct

from OCC.Core.Graphic3d import Graphic3d_ArrayOfPoints
from OCC.Core.AIS import AIS_PointCloud
from OCC.Core.Quantity import Quantity_Color, Quantity_TOC_RGB
from OCC.Core.gp import gp_Pnt

from OCC.Display.SimpleGui import init_display
display, start_display, add_menu, add_function_to_menu = init_display()

def pcd_get_number_of_vertices(pcd_filename):
    """ open the PCD file, read header and get number of vertices.
    Header looks like:
    # .PCD v.5 - Point Cloud Data file format
    VERSION .5
    FIELDS x y z
    SIZE 4 4 4
    TYPE F F F
    COUNT 1 1 1
    WIDTH 397
    HEIGHT 1
    POINTS 397
    DATA ascii
    """
    f = open(pcd_filename, 'r')
    # read 8 lines
    for i in range(8):
        f.readline()
    # the 9th line holds the number of points
    number_of_points = int(f.readline().split()[1])
    f.close()
    return number_of_points

def random_points(event=None):
    n_points = 500000
    # first, create a set of 1000 points
    points_3d = Graphic3d_ArrayOfPoints(n_points)
    for idx in range(n_points):
        x = random.uniform(-50, 50)
        y = random.uniform(-50, 50)
        z = random.uniform(-50, 50)
        points_3d.AddVertex(x, y, z)

    # then build the point cloud
    point_cloud = AIS_PointCloud()
    point_cloud.SetPoints(points_3d)

    # display
    ais_context = display.GetContext()
    ais_context.Display(point_cloud, True)
    display.View_Iso()
    display.FitAll()

def bunny(event=None):
    pcd_file_name = os.path.join('..', 'assets', 'models', 'bunny.pcd')
    # compute number of lines
    nbr_of_vertices = pcd_get_number_of_vertices(pcd_file_name)
    print("Number of vertices :", nbr_of_vertices)
    # create the point_cloud
    pc = Graphic3d_ArrayOfPoints(nbr_of_vertices)
    # fedd it with vertices
    fp = open(pcd_file_name, 'r')
    # read 11 lines to skip header
    for i in range(10):
        fp.readline()
    for i in range(nbr_of_vertices):
        line = fp.readline()
        x, y, z = map(float, line.split())
        pc.AddVertex(x, y, z)
    point_cloud = AIS_PointCloud()
    point_cloud.SetPoints(pc)
    ais_context = display.GetContext()
    ais_context.Display(point_cloud, True)
    display.View_Iso()
    display.FitAll()

def tabletop(event=None):
    pcd_file = open(os.path.join('..', 'assets', 'models', 'tabletop.pcd'), 'r').readlines()[11:]
    # create the point_cloud
    pc = Graphic3d_ArrayOfPoints(len(pcd_file), True)
    for line in pcd_file:
        x, y, z, rgb = map(float, line.split())
        r, g, b = unpackRGB(rgb)
        color = Quantity_Color(r/float(255), g/float(255), b/float(255), Quantity_TOC_RGB)
        pc.AddVertex(gp_Pnt(x, y, z), color)

    # then build the point cloud
    point_cloud = AIS_PointCloud()
    point_cloud.SetPoints(pc)
    # display
    ais_context = display.GetContext()
    ais_context.Display(point_cloud, True)
    display.DisableAntiAliasing()
    display.View_Iso()
    display.FitAll()

def unpackRGB(rgb):
    """
    Unpack PCL RGB data into r/g/b
    reference:
        http://docs.pointclouds.org/trunk/structpcl_1_1_point_x_y_z_r_g_b.html
    :param rgb: float
    :return:    unsigned integer [0 - 255]
    """
    # reinterpret from float to unsigned integer
    rgb = struct.unpack('I', struct.pack('f', rgb))[0]
    # unpack rgb into r/g/b
    r = (rgb >> 16) & 0x0000ff
    g = (rgb >> 8)  & 0x0000ff
    b = (rgb)       & 0x0000ff
    return r, g, b


if __name__ == '__main__':
    add_menu('pointcloud')
    add_function_to_menu('pointcloud', random_points)
    add_function_to_menu('pointcloud', bunny)
    add_function_to_menu('pointcloud', tabletop)
    start_display()
