# -*- coding: UTF-8 -*-

'''
Module
    command_bundle_factory_test.py
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
    Unit tests for CommandBundleFactory infrastructure component.
'''

from __future__ import annotations

from unittest import TestCase

from scaralang.infrastructure.command.command_bundle import CommandBundle
from scaralang.infrastructure.command.command_bundle_factory import CommandBundleFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.6'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class CommandBundleFactoryTest(TestCase):
    '''
        Tests for CommandBundleFactory command list instantiation and wiring.
    '''

    def test_create_commands(self) -> None:
        '''Verifies all 7 CLI CommandBundle instances are created and wired.'''
        commands = CommandBundleFactory.create_commands()
        self.assertEqual(len(commands), 7)
        for cmd in commands:
            self.assertIsInstance(cmd, CommandBundle)
            self.assertIsNotNone(cmd.definition)
            self.assertIsNotNone(cmd.executor)

    def test_get_version(self) -> None:
        '''Verifies factory version reporting.'''
        self.assertEqual(CommandBundleFactory.get_version(), '1.0.6')
