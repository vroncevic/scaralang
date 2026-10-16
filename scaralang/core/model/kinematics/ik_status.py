# -*- coding: UTF-8 -*-

'''
Module
    ik_status.py
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
    Defines IkStatus enumeration for inverse kinematics solution status.
'''

from __future__ import annotations

from enum import StrEnum, unique

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.9'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@unique
class IkStatus(StrEnum):
    '''
        Enumeration of inverse kinematics reachability and calculation statuses.

        It defines:

            :values:
                | SUCCESS - Target coordinates are reachable and kinematics solved.
                | OUT_OF_REACH - Target is outside the maximum radial reach of arm links.
                | INNER_DEADZONE - Target is inside the inner minimum radial deadzone.
                | Z_LIMIT_EXCEEDED - Vertical Z coordinate exceeds vertical travel bounds.
                | JOINT_LIMIT_EXCEEDED - Calculated joint angle exceeds mechanical limits.
                | SINGULARITY - Arm is in a singular configuration.
    '''

    SUCCESS = 'SUCCESS'
    OUT_OF_REACH = 'OUT_OF_REACH'
    INNER_DEADZONE = 'INNER_DEADZONE'
    Z_LIMIT_EXCEEDED = 'Z_LIMIT_EXCEEDED'
    JOINT_LIMIT_EXCEEDED = 'JOINT_LIMIT_EXCEEDED'
    SINGULARITY = 'SINGULARITY'
