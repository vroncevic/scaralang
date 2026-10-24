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
    Unit tests for LintFactory factory class.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main

from scaralang.infrastructure.command.idefinition import ICommandDefinition
from scaralang.infrastructure.command.iexecutor import ICommandExecutor
from scaralang.infrastructure.command.lint.factory import LintFactory
from scaralang.infrastructure.command.lint.provides import LintProvides

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestLintFactory(TestCase):
    '''
        Test cases verifying LintFactory construction and version reporting.

        It defines:

            :methods:
                | test_create - Verifies factory returns configured LintProvides.
                | test_get_version - Verifies factory version string.
    '''

    def test_create(self) -> None:
        '''Verifies factory returns fully wired LintProvides container.'''
        provides = LintFactory.create()
        self.assertIsInstance(provides, LintProvides)
        self.assertIsInstance(provides.executor, ICommandExecutor)
        self.assertIsInstance(provides.definition, ICommandDefinition)

    def test_get_version(self) -> None:
        '''Verifies factory version returns valid string.'''
        self.assertEqual(LintFactory.get_version(), '1.1.1')


if __name__ == '__main__':
    main()
