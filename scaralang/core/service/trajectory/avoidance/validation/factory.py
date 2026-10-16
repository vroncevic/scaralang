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
    Factory instantiating ValidationProvides instances.
'''

from __future__ import annotations

from scaralang.core.service.trajectory.avoidance.validation.provides import ValidationProvides
from scaralang.core.service.trajectory.avoidance.validation.validator import DeadZoneValidator

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.9'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ValidationFactory:
    '''
        Factory providing configured ValidationProvides instances.

        It defines:

            :methods:
                | create - Builds and returns a ValidationProvides bundle from radial threshold.
                | get_version - Returns factory version string.
    '''

    @classmethod
    def create(cls, dead_zone_radius: float) -> ValidationProvides:
        '''
            Builds and returns a ValidationProvides instance from radial threshold.

            :param dead_zone_radius: Radial inner dead zone limit in mm.
            :return: Configured ValidationProvides bundle.
            :exceptions: None.
        '''
        validator = DeadZoneValidator(dead_zone_radius=dead_zone_radius)
        return ValidationProvides(validator=validator)

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns the factory component version string representation.

            :return: Version string representation.
            :exceptions: None.
        '''
        return __version__
