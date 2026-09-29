# -*- coding: UTF-8 -*-

'''
Module
    itrajectory_plan_factory.py
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
    Structural protocol interface for TrajectoryPlan aggregate factory providers.
'''

from __future__ import annotations

from typing import Protocol
from typing import runtime_checkable

from scaralang.core.service.trajectory.plan.itrajectory_plan import ITrajectoryPlan

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class ITrajectoryPlanFactory(Protocol):
    '''
        Protocol defining factory operations for constructing TrajectoryPlan aggregates.

        It defines:

            :attributes:
                | name - Identifier name of the factory.
            :methods:
                | create - Constructs and returns an ITrajectoryPlan aggregate instance.
    '''

    @property
    def name(self) -> str:
        '''
            Gets the trajectory plan factory identifier name.

            :return: Factory name string.
        '''

    def create(self) -> ITrajectoryPlan:
        '''
            Constructs and returns an ITrajectoryPlan aggregate instance.

            :return: Initialized ITrajectoryPlan aggregate instance.
            :exceptions: None.
        '''
