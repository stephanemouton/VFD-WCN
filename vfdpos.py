#!/usr/bin/python
# -*- coding: utf8 -*-

# VFD PoS library for WN USB using PyUSB
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

import usb.core
import usb.util

# USB ID 0aa7:0200 = BA63-USB (2 lines of 20 characters)
# USB ID 0aa7:0201 = BA66-USB (4 lines of 20 characters)
BA63 = 0x0200
BA66 = 0x0201


class WincorNixdorfDisplayFactory:
    """Allow to create instances of WincorNixdorf(tm) display devices"""

    # defaut init used: nothing to do in constructor

    def get_vfd_pos(self, displayType=BA63):
        index = 0
        vfds = []

        # parameter find_all = True is required to enumerate all devices
        for device in usb.core.find(find_all=True, idVendor=0x0aa7, idProduct=displayType):
            vfd = vfd_pos(device, displayType, index)
            index = index + 1
            vfds.append(vfd)
        return vfds


class vfd_pos:
    def __init__(self, device, displayType, index):
        self.dev = device
        self.index = index
        self.displayType = displayType

        if self.dev is None:
            raise IOError("Error : Connect PoS VFD WincorNixdorf USB")
        try:
            self.dev.detach_kernel_driver(1)
        except:
            pass
        try:
            cfg = self.dev[0]
            ep = cfg[(0, 0)][1]
            assert ep is not None
            if ep.wMaxPacketSize != 32:
                ep = cfg[(1, 0)][1]
            assert ep.wMaxPacketSize == 32
            self.endpoint = ep
        except:
            raise IOError("Error initializing VFD " + str(index))
        self.set_charset(0x31)
        # Disabled for use with API
        #self.clearscreen()
        #self.poscur(0, 0)

    # Utility methods to ease management of multiple VFDs
    def get_index(self):
        return self.index
    def get_type(self):
        return self.displayType
    def get_type_label(self):
        return {
            BA63: "BA63",
            BA66: "BA66"
        }[self.displayType]
    def get_nb_lines(self):
        return {
            BA63: 2,
            BA66: 4
        }[self.displayType]

    # Display methods
    def close(self):
        # Allow consecutive factory creations in the same program
        usb.util.dispose_resources(self.dev)

    def send_buffer(self, buffer):
        self.endpoint.write(buffer)

    def selftest(self):
        buffer = [0x00] * 32
        buffer[1] = 0x10
        self.send_buffer(buffer)

    def reset(self):
        buffer = [0x00] * 32
        buffer[1] = 0x40
        self.send_buffer(buffer)

    def send_ctrl_seq(self, esc_seq):
        buffer = [0x00] * 32
        buffer[0] = 0x02
        len_seq = len(esc_seq)
        buffer[2] = len_seq
        for datx in range(0, len_seq):
            buffer[3 + datx] = esc_seq[datx]
        self.send_buffer(buffer)

    def set_charset(self, chrset):
        self.send_ctrl_seq([0x1B, 0x52, chrset])

    def clearscreen(self):
        self.send_ctrl_seq([0x1B, 0x5B, 0x32, 0x4A])

    def printchr(self, chr):
        self.send_ctrl_seq([chr])

    def poscur(self, line, col):
        seq = []
        seq.append(0x1B)
        seq.append(0x5B)
        assert (0 <= line <= 9)
        seq.append(0x30 + line)
        seq.append(0x3B)
        assert (0 <= col <= 99)
        diz, unit = divmod(col, 10)
        seq.append(0x30 + diz)
        seq.append(0x30 + unit)
        seq.append(0x48)
        self.send_ctrl_seq(seq)

    def write_msg(self, msgu):
        msg = msgu.encode('cp858')
        while msg:
            msg_chr = list(msg)[0:29]
            # removed map(ord, ...) used to handle unknown unicode chars
            self.send_ctrl_seq(msg_chr)
            msg = msg[29:]
