# -*- coding: UTF-8 -*-

'''
Module
    decompile_command_executor_factory_test.py
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
    Unit tests for DecompileCommandExecutorFactory class.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main

from scaralang.core.service.decompiler.scara_decompiler_factory import ScaraDecompilerFactory
from scaralang.infrastructure.command.decompile.decompile_command_definition import DecompileCommandDefinition
from scaralang.infrastructure.command.decompile.decompile_command_executor import DecompileCommandExecutor
from scaralang.infrastructure.command.decompile.decompile_command_executor_factory import DecompileCommandExecutorFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestDecompileCommandExecutorFactory(TestCase):
    '''
        Test cases verifying DecompileCommandExecutorFactory.

        It defines:

            :methods:
                | test_create_default - Verifies factory returns default DecompileCommandExecutor.
                | test_create_with_collaborators - Verifies factory builds with injected collaborators.
                | test_get_version - Verifies factory version string.
    '''

    def test_create_default(self) -> None:
        '''Verifies factory returns default DecompileCommandExecutor instance.'''
        executor = DecompileCommandExecutorFactory.create_default()
        self.assertIsInstance(executor, DecompileCommandExecutor)

    def test_create_with_collaborators(self) -> None:
        '''Verifies factory builds DecompileCommandExecutor with explicit collaborators.'''
        definition = DecompileCommandDefinition()
        service = ScaraDecompilerFactory.create_default()
        executor = DecompileCommandExecutorFactory.create(
            definition=definition,
            service=service,
        )
        self.assertIsInstance(executor, DecompileCommandExecutor)
        self.assertEqual(executor.get_definition().name, definition.name)

    def test_get_version(self) -> None:
        '''Verifies factory version returns valid string.'''
        self.assertEqual(DecompileCommandExecutorFactory.get_version(), '1.0.3')


if __name__ == '__main__':
    main()
