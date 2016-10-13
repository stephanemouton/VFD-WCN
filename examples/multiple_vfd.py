#!/usr/bin/python
# -*- coding: utf8 -*-

# Example for VFDPoS library for WN VFD
# cyvle message on multiple displays
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

import time
from vfdpos import *

factory=WincorNixdorfDisplayFactory()

vfds = factory.get_vfd_pos()

print("PRESS CTRL+C TO QUIT")

try:
    while True:
        for vfd in vfds:
            vfd.poscur(1+vfd.get_index()%2,8)
            vfd.write_msg("Ping")
            time.sleep(1)
            vfd.clearscreen()

except KeyboardInterrupt:
    pass
for wnpos in vfds:
    wnpos.close()
