#!/usr/bin/env python

##Copyright 2009-2015 Jelle Feringa (jelleferinga@gmail.com)
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

import time
import sys
import multiprocessing

from OCC.Core.BRep import BRep_Builder
from OCC.Core.BRepTools import breptools_Read
from OCC.Core.TopoDS import TopoDS_Shape
from OCC.Core.gp import gp_Pln, gp_Dir, gp_Pnt
from OCC.Core.BRepAlgoAPI import BRepAlgoAPI_Section
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeFace

from OCC.Display.SimpleGui import init_display

from OCC.Extend.ShapeFactory import get_aligned_boundingbox


def drange(start, stop, step):
    ''' mimic numpy arange method for float lists
    '''
    float_list = []
    r = start
    while r < stop-step:
        float_list.append(r)
        r += step
    return float_list


def get_brep():
    cylinder_head = TopoDS_Shape()
    builder = BRep_Builder()
    breptools_Read(cylinder_head, '../assets/models/cylinder_head.brep', builder)
    return cylinder_head


def vectorized_slicer(li):
    # Create Plane defined by a point and the perpendicular direction
    z_values, shape = li
    _slices = []
    for z in z_values:
        #print 'slicing index:', z, 'sliced by process:', os.getpid()
        plane = gp_Pln(gp_Pnt(0., 0., z), gp_Dir(0., 0., 1.))
        face = BRepBuilderAPI_MakeFace(plane).Shape()
        # Computes Shape/Plane intersection
        section = BRepAlgoAPI_Section(shape, face)
        section.Build()
        if section.IsDone():
            _slices.append(section.Shape())
    return _slices


def run(n_procs, compare_by_number_of_processors=False):
    shape = get_brep()
    center, [dx, dy, dz], box_shp = get_aligned_boundingbox(shape)
    z_min = center.Z() - dz / 2
    z_max = center.Z() + dz / 2

    init_time = time.time()  # for total time computation

    def get_z_coords_for_n_procs(n_slices, n_procs):
        z_slices = drange(z_min, z_max, dz/n_slices)

        slices = []
        n = len(z_slices) // n_procs
        print('number of slices:', len(z_slices))

        _str_slices = []
        for i in range(1, n_procs+1):
            if i == 1:
                slices.append(z_slices[:i*n])
                _str_slices.append(':'+str(i*n)+' ')
            elif i == n_procs:
                # does a little extra work if the number of slices
                # isnt divisible by n_procs
                slices.append(z_slices[(i-1)*n:])
                _str_slices.append(str((i-1)*n)+': ')
                print('last slice', len(z_slices[(i-1)*n:]))
            else:
                slices.append(z_slices[(i-1)*n:i*n])
                _str_slices.append(' %s:%s ' % ((i-1)*n, i*n))
        print('the z-index array is sliced over %s processors like this: \n %s' % (n_procs, _str_slices))
        return slices

    def arguments(n_slices, n_procs):
        _tmp = []
        slices = get_z_coords_for_n_procs(n_slices, n_procs)
        for i in slices:
            _tmp.append([i, shape])
        return _tmp

    n_slice = 50

    if not compare_by_number_of_processors:
        _results = []
        P = multiprocessing.Pool(n_procs)
        _results = P.map(vectorized_slicer, arguments(n_slice, n_procs))

    else:
        # run a few tests from 1 to 9 processors
        for i in range(1, 9):
            tA = time.time()
            _results = []
            if i == 1:
                _results = vectorized_slicer([drange(z_min, z_max, dz/n_slice), shape])
            else:
                P = multiprocessing.Pool(n_procs)
                _results = P.map(vectorized_slicer, arguments(n_slice, i))
            print('slicing took %s seconds for %s processors' % (time.time() - tA, i))
        sys.exit()

    print('\n\n\n done slicing on %i cores \n\n\n' % nprocs)

    # Display result
    display, start_display, add_menu, add_function_to_menu = init_display()
    print('displaying original shape')
    display.DisplayShape(shape, update=True)
    for n, result_shp in enumerate(_results):
        print('displaying results from process {0}'.format(n))
        display.DisplayShape(result_shp, update=True)

    # update viewer when all is added:
    display.Repaint()
    total_time = time.time() - init_time
    print("%s necessary to perform slice with %s processor(s)." % (total_time, n_procs))
    start_display()

if __name__ == '__main__':
    # use compare_by_number_of_processors=True to see speed up
    # per number of processor added
    try:
        nprocs = multiprocessing.cpu_count()
    except Exception as ex:  # travis fails to run cpu_count
        print(ex)
        nprocs = 1
    except SystemExit:
        pass
    run(nprocs, compare_by_number_of_processors=False)
