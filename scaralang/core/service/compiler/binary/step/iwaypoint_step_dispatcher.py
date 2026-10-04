# -*- coding: UTF-8 -*-

'''
Module
    iwaypoint_step_dispatcher.py
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
    Defines IWaypointStepDispatcher Protocol for dispatching waypoints to binary steps.
'''

from __future__ import annotations

from collections.abc import Sequence
from typing import Protocol, runtime_checkable

from scaralang.core.model.dsl.binary.step import Step
from scaralang.core.model.trajectory.waypoint import Waypoint

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class IWaypointStepDispatcher(Protocol):
    '''
        Structural protocol defining contracts for dispatching waypoints to binary steps.

        It defines:

            :methods:
                | dispatch_steps - Dispatches waypoints sequence into binary steps tuple.
                | get_version - Gets implementation version string.
    '''

    def dispatch_steps(
        self, *, waypoints: Sequence[Waypoint]
    ) -> tuple[Step, ...]:
        '''
            Dispatches sequence of domain waypoints into compiled binary steps.

            :param waypoints: Sequence of domain Waypoint instances.
            :return: Tuple of compiled Step instances.
        '''

    def get_version(self) -> str:
        '''
            Gets implementation version string.

            :return: Version string.
        '''
