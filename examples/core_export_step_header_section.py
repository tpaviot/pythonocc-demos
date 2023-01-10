##Copyright 2022 Thomas Paviot (tpaviot@gmail.com)
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

from datetime import datetime

from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeBox

from OCC.Core.STEPControl import STEPControl_Writer, STEPControl_AsIs
from OCC.Core.Interface import Interface_Static_SetCVal
from OCC.Core.IFSelect import IFSelect_RetDone

from OCC.Core.Interface import Interface_HArray1OfHAsciiString
from OCC.Core.APIHeaderSection import APIHeaderSection_MakeHeader
from OCC.Core.TCollection import TCollection_HAsciiString

# creates a basic shape
box_s = BRepPrimAPI_MakeBox(10, 20, 30).Shape()

# initialize the STEP exporter
step_writer = STEPControl_Writer()
dd = step_writer.WS().TransferWriter().FinderProcess()

Interface_Static_SetCVal("write.step.schema", "AP203")

# transfer shapes and write file
Interface_Static_SetCVal("write.step.product.name", "Box")
step_writer.Transfer(box_s, STEPControl_AsIs)

#
# Set STEP header
#
model = step_writer.Model()
model.ClearHeader()

hs = APIHeaderSection_MakeHeader()
hs.SetName(TCollection_HAsciiString("model name"))
hs.SetAuthorValue(1, TCollection_HAsciiString("My name"))
hs.SetAuthorisation(TCollection_HAsciiString("authorization"))

descr = Interface_HArray1OfHAsciiString(1, 3)
descr.SetValue(1, TCollection_HAsciiString("a description"))
descr.SetValue(2, TCollection_HAsciiString("split into"))
descr.SetValue(3, TCollection_HAsciiString("three items"))
hs.SetDescription(descr)

org = Interface_HArray1OfHAsciiString(1, 1)
org.SetValue(1, TCollection_HAsciiString("pythonocc organization"))
hs.SetOrganization(org)

hs.SetOriginatingSystem(TCollection_HAsciiString("pythonocc originating system"))
hs.SetImplementationLevel(TCollection_HAsciiString("implementation level"))

identifiers = Interface_HArray1OfHAsciiString(1, 1)
identifiers.SetValue(1, TCollection_HAsciiString("a schema identifier"))
hs.SetSchemaIdentifiers(identifiers)

hs.SetPreprocessorVersion(TCollection_HAsciiString("preprocessor version"))
hs.SetTimeStamp(TCollection_HAsciiString(f"Time stamp: {datetime.now()}"))

model.AddHeaderEntity(hs.FnValue())
model.AddHeaderEntity(hs.FsValue())
model.AddHeaderEntity(hs.FdValue())

# finally write file
status = step_writer.Write("box_header.stp")

if status != IFSelect_RetDone:
    raise AssertionError("load failed")
