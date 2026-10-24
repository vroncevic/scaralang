# -*- coding: UTF-8 -*-

'''
Module
    payload_size.py
Copyright
    Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>
    scaralang is free software: you can redistribute it and/or modify it
    under the terms of the GNU General Public License as published by the
    Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
    scaralang is distributed in the hope that it will be useful, but
    WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
    See the GNU General Public License for more details.
    You should have received a copy of the GNU General Public License along
    with this program. If not, see <http://www.gnu.org/licenses/>.
Info
    Defines BinaryPayloadSize enumeration for canonical binary wire payload byte lengths.
'''

from __future__ import annotations

from enum import IntEnum

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class BinaryPayloadSize(IntEnum):
    '''
        Canonical byte lengths of binary protocol wire payloads.

        It defines:

            :attributes:
                | OVERRIDE - Speed override command payload length (1).
                | TOOL_CMD - Tool actuation command payload length (2).
                | CONFIG_MOTOR - Motor configuration command payload length (2).
                | ACK - Positive acknowledgment payload length (2).
                | NACK - Negative rejection payload length (2).
                | WAIT - Delay duration payload length (4).
                | JOG_SHORT - Abbreviated joint jog command payload length (5).
                | MOVE_EVENT - Motion execution event payload length (5).
                | FAULT_EVENT - System fault event payload length (6).
                | JOG_FULL - Full joint jog command payload length (9).
                | STATUS - Consolidated robot status payload length (19).
                | JOINT_STEPS - Joint step target move payload length (22).
                | DIAGNOSTICS - Extended diagnostics report payload length (56).
    '''

    OVERRIDE = 1
    TOOL_CMD = 2
    CONFIG_MOTOR = 2
    ACK = 2
    NACK = 2
    WAIT = 4
    JOG_SHORT = 5
    MOVE_EVENT = 5
    FAULT_EVENT = 6
    JOG_FULL = 9
    STATUS = 19
    JOINT_STEPS = 22
    DIAGNOSTICS = 56
