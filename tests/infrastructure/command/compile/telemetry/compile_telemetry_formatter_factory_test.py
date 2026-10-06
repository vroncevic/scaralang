# -*- coding: UTF-8 -*-

'''
Module
    compile_telemetry_formatter_factory_test.py
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
    Unit tests for CompileTelemetryFormatterFactory.
'''

from __future__ import annotations

from unittest import TestCase, main

from scaralang.infrastructure.command.compile.telemetry.compile_telemetry_formatter import CompileTelemetryFormatter
from scaralang.infrastructure.command.compile.telemetry.compile_telemetry_formatter_factory import CompileTelemetryFormatterFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.6'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestCompileTelemetryFormatterFactory(TestCase):
    '''Test cases verifying CompileTelemetryFormatterFactory creation.'''

    def test_create(self) -> None:
        '''Verifies create returns a CompileTelemetryFormatter instance.'''
        formatter = CompileTelemetryFormatterFactory.create()
        self.assertIsInstance(formatter, CompileTelemetryFormatter)

    def test_create_default(self) -> None:
        '''Verifies create_default returns a CompileTelemetryFormatter instance.'''
        formatter = CompileTelemetryFormatterFactory.create_default()
        self.assertIsInstance(formatter, CompileTelemetryFormatter)


if __name__ == '__main__':
    main()
