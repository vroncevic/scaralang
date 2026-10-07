# -*- coding: UTF-8 -*-

'''
Module
    definition_test.py
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
    Unit tests for ReplCommandDefinition class.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main

from scaralang.infrastructure.command.repl.definition import ReplCommandDefinition

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.7'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestReplCommandDefinition(TestCase):
    '''
        Test cases verifying ReplCommandDefinition.

        It defines:

            :methods:
                | test_definition_metadata - Verifies name, help text and options.
    '''

    def test_definition_metadata(self) -> None:
        '''Verifies command properties and options.'''
        cmd_def = ReplCommandDefinition()
        self.assertEqual(cmd_def.name, 'repl')
        self.assertIn('REPL', cmd_def.help_text)
        self.assertEqual(len(cmd_def.options), 2)
        option_names = [opt.name for opt in cmd_def.options]
        self.assertIn('--endpoint', option_names)
        self.assertIn('--dry-run', option_names)
        self.assertTrue(str(cmd_def))


if __name__ == '__main__':
    main()
