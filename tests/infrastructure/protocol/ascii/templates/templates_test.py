# -*- coding: UTF-8 -*-

'''
Module
    templates_test.py
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
    Unit tests for CommandTemplates ASCII template catalog.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main

from scaralang.infrastructure.protocol.ascii.templates.itemplates import ICommandTemplates
from scaralang.infrastructure.protocol.ascii.templates.templates import CommandTemplates

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.9'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestCommandTemplates(TestCase):
    '''
        Unit test cases verifying CommandTemplates template lookup and listing.

        It defines:

            :methods:
                | test_constants - Verifies standard command template strings.
                | test_get_template - Verifies retrieval by action key.
                | test_list_actions - Verifies enumeration of actions.
                | test_structural_typing - Verifies instance satisfies ICommandTemplates.
                | test_get_version - Verifies version string retrieval.
    '''

    def test_constants(self) -> None:
        '''
            Verifies basic firmware command constants.
        '''
        self.assertEqual(CommandTemplates.ENABLE, '<CMD:ENABLE>')
        self.assertEqual(CommandTemplates.DISABLE, '<CMD:DISABLE>')
        self.assertEqual(CommandTemplates.ESTOP, '<CMD:ESTOP>')
        self.assertEqual(CommandTemplates.HOME, '<CMD:HOME>')

    def test_get_template(self) -> None:
        '''
            Verifies get_template returns correct template for valid and invalid keys.
        '''
        tpl: str = CommandTemplates.get_template('MOVE')
        self.assertTrue(tpl.startswith('<pt#'))
        empty_tpl: str = CommandTemplates.get_template('NON_EXISTENT')
        self.assertEqual(empty_tpl, '')

    def test_list_actions(self) -> None:
        '''
            Verifies list_actions returns non-empty tuple of supported action keys.
        '''
        actions: tuple[str, ...] = CommandTemplates.list_actions()
        self.assertGreater(len(actions), 10)
        self.assertIn('ENABLE', actions)
        self.assertIn('MOVE', actions)
        self.assertIn('HOME', actions)

    def test_structural_typing(self) -> None:
        '''
            Verifies CommandTemplates instance satisfies ICommandTemplates.
        '''
        instance = CommandTemplates()
        self.assertIsInstance(instance, ICommandTemplates)

    def test_get_version(self) -> None:
        '''
            Verifies get_version returns a valid version string.
        '''
        version: str = CommandTemplates.get_version()
        self.assertIsInstance(version, str)
        self.assertGreater(len(version), 0)


if __name__ == '__main__':
    main()
