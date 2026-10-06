# -*- coding: UTF-8 -*-

'''
Module
    iscara_exporter_test.py
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
    Unit tests for IScaraExporter protocol and ScaraExporter class.
'''

from __future__ import annotations

from typing import Protocol
from unittest import TestCase
from unittest import main

from scaralang.core.model.dsl.exporter.export_format import ExportFormat
from scaralang.core.service.exporter.iscara_exporter import IScaraExporter
from scaralang.core.service.exporter.scara_exporter import ScaraExporter
from scaralang.core.service.exporter.scara_exporter_factory import ScaraExporterFactory
from scaralang.core.service.trajectory.plan.itrajectory_plan import ITrajectoryPlan

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.6'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class DummyExporter:
    '''Dummy exporter satisfying IScaraExporter protocol.'''

    def export(
        self, *, plan: ITrajectoryPlan, target_format: ExportFormat
    ) -> str:
        '''Dummy export implementation.'''
        _ = plan
        return target_format.value

    def supported_formats(self) -> tuple[ExportFormat, ...]:
        '''Dummy supported formats implementation.'''
        return (ExportFormat.SCARA,)

    def get_version(self) -> str:
        '''Dummy get_version implementation.'''
        return '1.0.6'


class TestIScaraExporter(TestCase):
    '''
        Test cases verifying IScaraExporter protocol contract.

        It defines:

            :methods:
                | test_protocol_conformance - Verifies dummy class satisfies protocol.
                | test_factory_production - Verifies factory produces conforming instance.
                | test_get_version - Verifies factory and instance version retrieval.
    '''

    def test_protocol_conformance(self) -> None:
        '''Verifies structural protocol definition and dummy satisfaction.'''
        self.assertTrue(issubclass(IScaraExporter, Protocol))
        self.assertTrue(hasattr(IScaraExporter, 'export'))
        self.assertTrue(hasattr(IScaraExporter, 'supported_formats'))
        self.assertTrue(hasattr(IScaraExporter, 'get_version'))
        self.assertIsInstance(DummyExporter(), IScaraExporter)

    def test_factory_production(self) -> None:
        '''Verifies factory creates conforming ScaraExporter instance.'''
        exporter: ScaraExporter = ScaraExporterFactory.create_default()
        self.assertIsInstance(exporter, IScaraExporter)
        self.assertIn(ExportFormat.SCARA, exporter.supported_formats())

    def test_get_version(self) -> None:
        '''Verifies version string from factory and instance.'''
        self.assertEqual(ScaraExporterFactory.get_version(), '1.0.6')
        exporter = ScaraExporterFactory.create_default()
        self.assertEqual(exporter.get_version(), '1.0.6')


if __name__ == '__main__':
    main()
