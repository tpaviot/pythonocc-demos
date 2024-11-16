from OCC.Core.gp import gp_Pnt, gp_Ax2, gp_Dir
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeBox, BRepPrimAPI_MakeCylinder
from OCC.Core.BRepAlgoAPI import BRepAlgoAPI_Fuse
from OCC.Core.BRepTools import BRepTools_History
from OCC.Core.TopAbs import TopAbs_FACE
from OCC.Core.TopExp import TopExp_Explorer
from OCC.Core.TopTools import TopTools_ListIteratorOfListOfShape

# Create the first shape: a box
box = BRepPrimAPI_MakeBox(100, 100, 100).Shape()

# Create the second shape: a cylinder
cylinder = BRepPrimAPI_MakeCylinder(
    gp_Ax2(gp_Pnt(50, 50, 0), gp_Dir(0, 0, 1)), 50, 150
).Shape()

# Perform the merge operation
fuse = BRepAlgoAPI_Fuse(box, cylinder)
fuse.Build()

# Get the resulting shape
merged_shape = fuse.Shape()

# Create a history object to track the operation
history = BRepTools_History()
history.Merge(fuse.History())


def iter_type(shp, type=TopAbs_FACE):
    exp = TopExp_Explorer(shp, type)
    while exp.More():
        res = exp.Current()
        yield res
        exp.Next()


def iter_list_of_shape(list_of_shape):
    occ_iterator = TopTools_ListIteratorOfListOfShape(list_of_shape)
    while occ_iterator.More():
        yield occ_iterator.Value()
        occ_iterator.Next()


# Print out the history of the merge operation
print("History of the merge operation:")
for fi, face in enumerate(iter_type(box)):
    for i in range(history.Generated(face).Size()):
        print(
            f"Generated from box face no {fi}: {list(iter_list_of_shape(history.Generated(face)))}"
        )
for fi, face in enumerate(iter_type(cylinder)):
    for i in range(history.Generated(face).Size()):
        print(
            f"Generated from cylinder face no {fi}: {list(iter_list_of_shape(history.Generated(face)))}"
        )
