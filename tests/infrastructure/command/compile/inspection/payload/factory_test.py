# -*- coding: UTF-8 -*-

'''
Module
    factory_test.py
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
    Unit tests for PayloadFactory coordinating operations.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main

from scaralang.infrastructure.command.compile.inspection.payload.dispatch.formatter import PayloadDispatcherFormatter
from scaralang.infrastructure.command.compile.inspection.payload.dispatch.iformatter import IPayloadDispatcherFormatter
from scaralang.infrastructure.command.compile.inspection.payload.factory import PayloadFactory
from scaralang.infrastructure.command.compile.inspection.payload.joint.formatter import JointStepsPayloadFormatter
from scaralang.infrastructure.command.compile.inspection.payload.joint.iformatter import IJointStepsPayloadFormatter
from scaralang.infrastructure.command.compile.inspection.payload.provides import PayloadProvides
from scaralang.infrastructure.command.compile.inspection.payload.tool.formatter import ToolCommandPayloadFormatter
from scaralang.infrastructure.command.compile.inspection.payload.tool.iformatter import IToolCommandPayloadFormatter

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.9'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestPayloadFactory(TestCase):
    '''
        Test cases verifying PayloadFactory coordinating operations.

        It defines:

            :methods:
                | test_create_returns_provides - Verifies create returns PayloadProvides.
                | test_get_version - Verifies factory version string.
    '''

    def test_create_returns_provides(self) -> None:
        '''
            Verifies factory creates PayloadProvides containing all payload formatters.
        '''
        provides = PayloadFactory.create()
        self.assertIsInstance(provides, PayloadProvides)
        self.assertIsInstance(provides.formatter, IPayloadDispatcherFormatter)
        self.assertIsInstance(provides.formatter, PayloadDispatcherFormatter)
        self.assertIsInstance(provides.joint_formatter, IJointStepsPayloadFormatter)
        self.assertIsInstance(provides.joint_formatter, JointStepsPayloadFormatter)
        self.assertIsInstance(provides.tool_formatter, IToolCommandPayloadFormatter)
        self.assertIsInstance(provides.tool_formatter, ToolCommandPayloadFormatter)

    def test_get_version(self) -> None:
        '''
            Verifies factory returns correct version string.
        '''
        self.assertEqual(PayloadFactory.get_version(), '1.0.9')


if __name__ == '__main__':
    main()
