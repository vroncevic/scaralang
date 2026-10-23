# -*- coding: UTF-8 -*-

'''
Module
    envelope.py
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
    Implementation of manipulator workspace envelope geometry and operational reach calculation.
'''

from __future__ import annotations

from typing import Final

from scaralang.core.model.kinematics.profile.bounds import ScaraBounds

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class WorkspaceEnvelope:
    '''
        Calculates physical manipulator workspace envelope and reach radii.

        It defines:

            :attributes:
                | _bounds - Robot ScaraBounds containing link lengths, limits, and margins.
            :methods:
                | __init__ - Initializes envelope with robot bounds model.
                | bounds - Returns active robot bounds model.
                | r_min - Returns minimum reach radius in mm.
                | r_max - Returns maximum reach radius in mm.
                | safe_r_max - Returns safe maximum reach radius considering margin in mm.
                | get_version - Returns envelope component version string.
    '''

    _bounds: ScaraBounds

    def __init__(self, bounds: ScaraBounds) -> None:
        '''
            Initializes workspace envelope calculator with robot bounds.

            :param bounds: Injected ScaraBounds model instance.
            :exceptions: None.
        '''
        self._bounds: Final[ScaraBounds] = bounds

    @property
    def bounds(self) -> ScaraBounds:
        '''
            Returns the active robot geometry and limits model.

            :return: ScaraBounds instance.
            :exceptions: None.
        '''
        return self._bounds

    @property
    def r_min(self) -> float:
        '''
            Returns the minimum annular workspace reach radius in mm.

            :return: Minimum reach radius float value.
            :exceptions: None.
        '''
        return max(
            abs(self._bounds.links.l1 - self._bounds.links.l2),
            self._bounds.singularity.deadzone_r_min,
        )

    @property
    def r_max(self) -> float:
        '''
            Returns the maximum annular workspace reach radius in mm.

            :return: Maximum reach radius float value.
            :exceptions: None.
        '''
        return self._bounds.links.l1 + self._bounds.links.l2

    @property
    def safe_r_max(self) -> float:
        '''
            Returns the maximum safe reach radius considering outer singularity margin in mm.

            :return: Safe maximum reach radius float value.
            :exceptions: None.
        '''
        return (
            self._bounds.links.l1
            + self._bounds.links.l2
            - self._bounds.singularity.singularity_outer_margin_mm
        )

    def get_version(self) -> str:
        '''
            Returns envelope component version string representation.

            :return: Semantic version string.
            :exceptions: None.
        '''
        return __version__
