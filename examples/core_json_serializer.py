##Copyright 2023 Thomas Paviot (tpaviot@gmail.com)
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

import json

from OCC.Core.gp import gp_Pnt

# OCCT provides a DumpJson and InitFromJson methods
# unfortunately DumpJson generates a non conform json string

p_1 = gp_Pnt(1.0, 3.14, -3.0)
dumped_json = p_1.DumpJson()
print(f"Json string: {dumped_json}")

# try to load this string with json
try:
    json.loads(dumped_json)
except json.decoder.JSONDecodeError:
    print("Json decode error")

# so implement our own serializer deserializer


def encode_json_gp_Pnt(p):
    return json.dumps({"type": "gp_Pnt", "x": p.X(), "y": p.Y(), "z": p.Z()})


def decode_json_gp_Pnt(s):
    params = json.loads(s)
    x = float(params["x"])
    y = float(params["y"])
    z = float(params["z"])
    return gp_Pnt(x, y, z)


ss = encode_json_gp_Pnt(p_1)
p_2 = decode_json_gp_Pnt(ss)
