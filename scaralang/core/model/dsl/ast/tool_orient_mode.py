# -*- coding: UTF-8 -*-

'''
Module
    tool_orient_mode.py
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
    Defines ToolOrientMode enumeration for 4th axis tool orientation modes.
'''

from __future__ import annotations

from enum import StrEnum, unique

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.5'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@unique
class ToolOrientMode(StrEnum):
    '''
        Enumeration of wrist 4th-axis tool orientation modes.

        It defines:

            :attributes:
                | FIXED - Tool angle remains fixed at a specified constant angle.
                | TANGENTIAL - Tool angle dynamically tracks path tangent direction.
                | JOINT_LOCKED - Tool axis is locked relative to the distal forearm joint.
    '''

    FIXED = 'FIXED'
    TANGENTIAL = 'TANGENTIAL'
    JOINT_LOCKED = 'JOINT_LOCKED'
