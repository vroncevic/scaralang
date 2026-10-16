# -*- coding: UTF-8 -*-

'''
Module
    bypass_arc_geometry.py
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
    Defines immutable data structure BypassArcGeometry encapsulating
    geometric parameters for dead zone avoidance detour arc.
'''

from __future__ import annotations

from dataclasses import dataclass

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.9'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@dataclass(slots=True, frozen=True, kw_only=True)
class BypassArcGeometry:
    '''
        Immutable data model encapsulating geometric parameters for dead zone bypass arc.

        It defines:

            :attributes:
                | phi_entry - Tangential entry angle on safe boundary in radians.
                | phi_exit - Tangential exit angle on safe boundary in radians.
                | step_sign - Direction indicator for angular sweep (+1.0 CCW, -1.0 CW).
                | arc_sweep - Absolute angular sweep of detour arc in radians.
                | safe_radius - Radius of the safe clearance circle boundary in mm.
    '''

    phi_entry: float
    phi_exit: float
    step_sign: float
    arc_sweep: float
    safe_radius: float
