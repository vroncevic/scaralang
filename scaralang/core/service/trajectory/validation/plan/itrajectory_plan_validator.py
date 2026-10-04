# -*- coding: UTF-8 -*-

'''
Module
    itrajectory_plan_validator.py
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
    Defines structural protocol ITrajectoryPlanValidator for plan validation.
'''

from __future__ import annotations

from typing import Protocol, runtime_checkable

from scaralang.core.service.trajectory.plan.itrajectory_read_only import ITrajectoryReadOnly

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class ITrajectoryPlanValidator(Protocol):
    '''
        Protocol defining trajectory plan validation contract.

        It defines:

            :attributes:
                | name - Identifier name of the trajectory plan validator.
            :methods:
                | validate_plan - Validates entire trajectory plan against bounds.
    '''

    @property
    def name(self) -> str:
        '''
            Gets the trajectory plan validator identifier name.

            :return: Validator name string.
        '''

    def validate_plan(self, plan: ITrajectoryReadOnly) -> tuple[bool, list[str]]:
        '''
            Validates entire trajectory plan against kinematic and feedrate bounds.

            :param plan: ITrajectoryReadOnly instance to validate.
            :return: Tuple of (is_valid, messages_list).
        '''
