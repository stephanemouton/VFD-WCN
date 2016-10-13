#!/usr/bin/python
# -*- coding: utf8 -*-

# Example for VFD-WCN library for WN VFD
# Basic test; enumerate displays by getting list and dsplaying a number on each.
# Copyright (C) 2016  Stephane MOUTON

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the License.
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>


from vfdpos import *

factory=WincorNixdorfDisplayFactory()

vfds = factory.get_vfd_pos(BA63)

for vfd in vfds:
    vfd.poscur(0, 0)
    index = vfd.get_index()
    label = vfd.get_type_label()
    nb_lines = vfd.get_nb_lines()
    vfd.write_msg("VFD("+str(index)+") of type "+label)
    vfd.poscur(2,1)
    vfd.write_msg(str(nb_lines)+" lines by 20 chars")

input("PRESS ENTER for self test")

for vfd in vfds:
    vfd.selftest()

for vfd in vfds:
    vfd.close()
