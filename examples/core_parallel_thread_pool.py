##Copyright 2026 Thomas Paviot (tpaviot@gmail.com)
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

"""Set the number of threads used by the parallel algorithms of OCCT
(boolean operations with SetRunParallel(True), BRepMesh_IncrementalMesh in
parallel mode, ...). They run their jobs in the default OSD_ThreadPool, which
uses all the logical processors unless it is initialized with another number
of threads, e.g. to leave some cores to the rest of the application.

If OCCT is built with TBB, OSD_Parallel.SetUseOcctThreads(True) makes the
parallel algorithms use the OSD_ThreadPool instead of TBB."""

import time

from OCC.Core.BRepAlgoAPI import BRepAlgoAPI_Fuse
from OCC.Core.BRepMesh import BRepMesh_IncrementalMesh
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeBox, BRepPrimAPI_MakeSphere
from OCC.Core.gp import gp_Pnt
from OCC.Core.OSD import OSD_Parallel, OSD_ThreadPool
from OCC.Core.TopTools import TopTools_ListOfShape

print(f"Logical processors: {OSD_Parallel.NbLogicalProcessors()}")
print(f"OCCT threads used (not TBB): {OSD_Parallel.ToUseOcctThreads()}")

# a plate with 10x10 bumps, each bump is a face to mesh
arguments = TopTools_ListOfShape()
arguments.Append(BRepPrimAPI_MakeBox(gp_Pnt(-5, -5, -5), 100, 100, 10).Shape())
tools = TopTools_ListOfShape()
for i in range(10):
    for j in range(10):
        tools.Append(BRepPrimAPI_MakeSphere(gp_Pnt(i * 10, j * 10, 5), 4).Shape())

pool = OSD_ThreadPool.DefaultPool()
default_nb_threads = pool.NbThreads()

for nb_threads in sorted({1, 2, default_nb_threads}):
    pool.Init(nb_threads)
    fuse = BRepAlgoAPI_Fuse()
    fuse.SetArguments(arguments)
    fuse.SetTools(tools)
    fuse.SetRunParallel(True)
    fuse.Build()
    shape = fuse.Shape()
    start = time.perf_counter()
    BRepMesh_IncrementalMesh(shape, 0.02, False, 0.1, True)  # in parallel
    elapsed = time.perf_counter() - start
    print(f"{pool.NbThreads():2d} thread(s): parallel mesh in {elapsed:.2f}s")

# back to the default number of threads
pool.Init(default_nb_threads)
