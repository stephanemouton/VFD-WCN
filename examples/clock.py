#!/usr/bin/python
# -*- coding: utf8 -*-

# Example for VFDPoS library for WN VFD
# Displays date and time
# Copyright (C) 2015  Antoine FERRON
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
import time

factory = WincorNixdorfDisplayFactory()

vfds = factory.get_vfd_pos()

print("PRESS CTRL+C TO QUIT")


def printdate(onepos, present_time):
    onepos.poscur(1, 1)
    date = time.strftime("%a %d %b %Y", present_time).center(20)
    onepos.write_msg(date)
    hour = time.strftime("%H:%M", present_time).center(20)
    onepos.poscur(2, 1)
    onepos.write_msg(hour)


try:
    while True:
        present_time = time.localtime()
        remaining = 60 - present_time.tm_sec
        for wnpos in vfds:
            printdate(wnpos, present_time)
    time.sleep(remaining)

except KeyboardInterrupt:
    pass
for wnpos in vfds:
    wnpos.close()
