# -*- coding: UTF-8 -*-

'''
Module
    iexport_target_dispatcher_test.py
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
    Unit tests for IExportTargetDispatcher protocol contract.
'''

from __future__ import annotations

from unittest import TestCase, main

from scaralang.core.model.dsl.exporter.export_format import ExportFormat
from scaralang.core.service.exporter.iexport_target_dispatcher import IExportTargetDispatcher
from scaralang.core.service.trajectory.plan.itrajectory_plan import ITrajectoryPlan

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class DummyDispatcher:
    '''Dummy dispatcher for protocol runtime check verification.'''

    def export(
        self, *, plan: ITrajectoryPlan, target_format: ExportFormat
    ) -> str:
        '''Dummy export implementation.'''
        _ = plan
        return target_format.value

    def supported_formats(self) -> tuple[ExportFormat, ...]:
        '''Dummy supported formats implementation.'''
        return (ExportFormat.GCODE,)


class TestIExportTargetDispatcher(TestCase):
    '''
        Test cases verifying IExportTargetDispatcher protocol contract.

        It defines:

            :methods:
                | test_protocol_conformance - Verifies dummy class satisfies protocol.
                | test_protocol_methods - Verifies protocol methods callable on instance.
    '''

    def test_protocol_conformance(self) -> None:
        '''Verifies structural typing conformance without inheritance.'''
        dispatcher = DummyDispatcher()
        self.assertIsInstance(dispatcher, IExportTargetDispatcher)

    def test_protocol_methods(self) -> None:
        '''Verifies protocol methods return valid types.'''
        dispatcher: IExportTargetDispatcher = DummyDispatcher()
        self.assertEqual(dispatcher.supported_formats(), (ExportFormat.GCODE,))


if __name__ == '__main__':
    main()
