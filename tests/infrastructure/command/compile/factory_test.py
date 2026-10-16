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
    Unit tests for CompileFactory.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main

from scaralang.infrastructure.command.compile.factory import CompileFactory
from scaralang.infrastructure.command.compile.provides import CompileProvides
from scaralang.infrastructure.command.idefinition import ICommandDefinition
from scaralang.infrastructure.command.iexecutor import ICommandExecutor

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.9'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestCompileFactory(TestCase):
    '''Test suite verifying CompileFactory creation and versioning.'''

    def test_create(self) -> None:
        '''Verifies create returns properly configured CompileProvides.'''
        provides: CompileProvides = CompileFactory.create()
        self.assertIsInstance(provides, CompileProvides)
        self.assertTrue(isinstance(provides.executor, ICommandExecutor))
        self.assertTrue(isinstance(provides.definition, ICommandDefinition))

    def test_get_version(self) -> None:
        '''Verifies get_version returns valid semantic version.'''
        self.assertEqual(CompileFactory.get_version(), '1.0.9')


if __name__ == '__main__':
    main()
