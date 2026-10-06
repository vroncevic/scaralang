# -*- coding: UTF-8 -*-

'''
Module
    joint_angle_bounds.py
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
    Defines JointAngleBounds domain value object for SCARA angular bounds.
'''

from __future__ import annotations

from dataclasses import dataclass

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.6'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@dataclass(frozen=True, slots=True, kw_only=True)
class JointAngleBounds:
    '''
        Domain Value Object encapsulating SCARA joint angular range bounds.

        It defines:

            :attributes:
                | j1_min_rad - Joint 1 (Shoulder) minimum angle in radians.
                | j1_max_rad - Joint 1 (Shoulder) maximum angle in radians.
                | j2_min_rad - Joint 2 (Elbow) minimum angle in radians.
                | j2_max_rad - Joint 2 (Elbow) maximum angle in radians.
    '''

    j1_min_rad: float
    j1_max_rad: float
    j2_min_rad: float
    j2_max_rad: float
