#!/usr/bin/env python

##Copyright 2009-2014 Jelle Feringa (jelleferinga@gmail.com)
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

from OCC.Core.gp import gp_Pnt, gp
from OCC.Core.GeomAPI import GeomAPI_ProjectPointOnCurve
from OCC.Core.Geom import Geom_Circle

from OCC.Display.SimpleGui import init_display

display, start_display, add_menu, add_function_to_menu = init_display()


def project_point_on_curve():
    """ """
    point_to_project = gp_Pnt(1.0, 2.0, 3.0)
    radius = 5.0

    # create a circle, centered at origin with a given radius
    circle = Geom_Circle(gp.XOY(), radius)
    display.DisplayShape(circle)
    display.DisplayShape(point_to_project, update=True)
    display.DisplayMessage(point_to_project, "P")

    # project the point P on the circle
    projection = GeomAPI_ProjectPointOnCurve(point_to_project, circle)
    # get the results of the projection
    # the point
    projected_point = projection.NearestPoint()
    # the number of possible results
    nb_results = projection.NbPoints()
    print("NbResults : %i" % nb_results)

    pstring = "N : at Distance : %f" % projection.LowerDistance()
    display.DisplayMessage(projected_point, pstring)

    # there maybe many different possible solutions
    if nb_results > 0:
        for i in range(1, nb_results + 1):
            Q = projection.Point(i)
            distance = projection.Distance(i)
            pstring = "Q%i: at Distance :%f" % (i, distance)
            display.DisplayShape(Q)
            display.DisplayMessage(Q, pstring)


if __name__ == "__main__":
    project_point_on_curve()
    start_display()
