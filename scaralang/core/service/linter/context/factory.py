# -*- coding: UTF-8 -*-

'''
Module
    factory.py
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
    Factory instantiating initialized LintContext instances.
'''

from __future__ import annotations

from typing import ClassVar

from scaralang.core.model.dsl.ast.zone_mode import ZoneMode
from scaralang.core.model.dsl.linter.context import LintContext
from scaralang.core.model.dsl.linter.tool_state import LintToolState
from scaralang.core.model.motor.mode import MotorDriveMode

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class LintContextFactory:
    '''
        Factory providing initialized LintContext instances.

        It defines:

            :attributes:
                | DEFAULT_ZONE_RADIUS - Initial corner blending radius in mm.
            :methods:
                | create - Creates an initialized LintContext instance.
                | get_version - Returns factory version string.
    '''

    DEFAULT_ZONE_RADIUS: ClassVar[float] = 0.0

    @classmethod
    def create(cls) -> LintContext:
        '''
            Creates an initialized LintContext instance.

            :return: Initialized LintContext instance.
            :exceptions: None.
        '''
        return LintContext(
            is_homed=False,
            motion_occurred=False,
            tool_state=LintToolState(pump_on=False, valve_on=False),
            zone_mode=ZoneMode.FINE,
            zone_radius=cls.DEFAULT_ZONE_RADIUS,
            last_coords=(),
            motor_drive_mode=MotorDriveMode.OPEN_LOOP,
        )

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns the factory version string representation.

            :return: Factory version string.
            :exceptions: None.
        '''
        return __version__
