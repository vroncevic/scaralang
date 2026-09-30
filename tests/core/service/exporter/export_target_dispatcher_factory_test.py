# -*- coding: UTF-8 -*-

'''
Module
    export_target_dispatcher_factory_test.py
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
    Unit tests for ExportTargetDispatcherFactory class.
'''

from __future__ import annotations

from unittest import TestCase, main
from unittest.mock import MagicMock

from scaralang.core.service.exporter.export_dispatcher_bundle import ExportDispatcherBundle
from scaralang.core.service.exporter.export_target_dispatcher_factory import ExportTargetDispatcherFactory
from scaralang.core.service.exporter.iexport_target_dispatcher import IExportTargetDispatcher

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestExportTargetDispatcherFactory(TestCase):
    '''
        Test cases verifying ExportTargetDispatcherFactory.

        It defines:

            :methods:
                | test_create - Verifies factory returns IExportTargetDispatcher with bundle.
                | test_create_default - Verifies factory returns default IExportTargetDispatcher.
                | test_get_version - Verifies factory version string.
    '''

    def test_create(self) -> None:
        '''Verifies factory returns IExportTargetDispatcher instance with bundle.'''
        bundle = ExportDispatcherBundle(
            gcode_exporter=MagicMock(),
            csv_exporter=MagicMock(),
            json_exporter=MagicMock(),
            svg_exporter=MagicMock(),
            scara_exporter=MagicMock(),
        )
        dispatcher = ExportTargetDispatcherFactory.create(bundle=bundle)
        self.assertIsInstance(dispatcher, IExportTargetDispatcher)

    def test_create_default(self) -> None:
        '''Verifies factory returns default IExportTargetDispatcher instance.'''
        dispatcher = ExportTargetDispatcherFactory.create_default()
        self.assertIsInstance(dispatcher, IExportTargetDispatcher)

    def test_get_version(self) -> None:
        '''Verifies factory version returns valid string.'''
        self.assertEqual(
            ExportTargetDispatcherFactory.get_version(), '1.0.2'
        )


if __name__ == '__main__':
    main()
