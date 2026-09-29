# -*- coding: UTF-8 -*-

'''
Module
    export_command_definition_test.py
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
    Unit tests for ExportCommandDefinition class.
'''

from __future__ import annotations

from unittest import TestCase, main

from scaralang.infrastructure.command.export.export_command_definition import ExportCommandDefinition

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestExportCommandDefinition(TestCase):
    '''
        Test cases verifying ExportCommandDefinition.

        It defines:

            :methods:
                | test_definition_metadata - Verifies name, help text and options.
    '''

    def test_definition_metadata(self) -> None:
        '''Verifies command properties and options.'''
        cmd_def = ExportCommandDefinition()
        self.assertEqual(cmd_def.name, 'export')
        self.assertIn('G-code', cmd_def.help_text)
        self.assertEqual(len(cmd_def.options), 3)
        option_names = [opt.name for opt in cmd_def.options]
        self.assertIn('--script', option_names)
        self.assertIn('--format', option_names)
        self.assertIn('--output', option_names)
        self.assertTrue(str(cmd_def))


if __name__ == '__main__':
    main()
