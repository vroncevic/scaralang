# -*- coding: UTF-8 -*-

'''
Module
    dependencies.py
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
    Inbound dependencies bundle for default shape avoidance infrastructure factory.
'''

from __future__ import annotations

from dataclasses import dataclass
from math import pi

from scaralang.core.model.kinematics.scara_bounds import ScaraBounds

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.9'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@dataclass(frozen=True, slots=True)
class DefaultShapeDependencies:
    '''
        Inbound parameters for default shape avoidance factory.

        It defines:

            :attributes:
                | bounds - Manipulator kinematic workspace bounds.
                | safety_margin_mm - Clearance distance added to deadzone radius.
                | angular_step_rad - Discretization angle for detour arc in radians.
    '''

    bounds: ScaraBounds
    safety_margin_mm: float = 5.0
    angular_step_rad: float = pi / 12.0
