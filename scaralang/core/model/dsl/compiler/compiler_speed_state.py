# -*- coding: UTF-8 -*-

'''
Module
    compiler_speed_state.py
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
    Stateful domain model tracking feedrates, accelerations, and overrides during compilation.
'''

from __future__ import annotations

from dataclasses import dataclass

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@dataclass(slots=True, kw_only=True)
class CompilerSpeedState:
    '''
        Stateful model tracking feedrates, accelerations, and overrides during compilation.

        It defines:

            :attributes:
                | speed_rapid - Default rapid feedrate in mm/s.
                | speed_work - Default work feedrate in mm/s.
                | current_speed - Active motion feedrate in mm/s.
                | active_accel - Active path acceleration in mm/s^2.
                | speed_override_pct - Global velocity scaling percentage (1-100).
    '''

    speed_rapid: float = 150.0
    speed_work: float = 40.0
    current_speed: float = 40.0
    active_accel: float = 300.0
    speed_override_pct: float = 100.0
