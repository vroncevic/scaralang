# -*- coding: UTF-8 -*-

'''
Module
    iexport_target_dispatcher.py
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
    Defines IExportTargetDispatcher Protocol for dispatching export requests.
'''

from __future__ import annotations

from typing import Protocol
from typing import runtime_checkable

from scaralang.core.model.dsl.exporter.export_format import ExportFormat
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
class IExportTargetDispatcher(Protocol):
    '''
        Structural protocol defining contracts for dispatching trajectory exports.

        It defines:

            :methods:
                | export - Dispatches trajectory plan export to selected target format.
                | supported_formats - Returns collection of supported export format enums.
    '''

    def export(
        self, *, plan: ITrajectoryPlan, target_format: ExportFormat
    ) -> str:
        '''
            Serializes trajectory plan into selected target export format string.

            :param plan: Validated ITrajectoryPlan protocol instance.
            :param target_format: Target format enum identifier.
            :return: Formatted export string.
        '''

    def supported_formats(self) -> tuple[ExportFormat, ...]:
        '''
            Returns collection of all export formats supported by dispatcher.

            :return: Tuple of supported ExportFormat enum values.
        '''
