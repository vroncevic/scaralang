# -*- coding: UTF-8 -*-

'''
Module
    iinstruction_line_parser_test.py
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
    Unit tests for IInstructionLineParser protocol compliance.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main

from scaralang.core.service.parser.instruction.iinstruction_line_parser import IInstructionLineParser
from scaralang.core.service.parser.instruction.instruction_line_parser import InstructionLineParser

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestIInstructionLineParser(TestCase):
    '''
        Test cases verifying IInstructionLineParser structural subtyping.

        It defines:

            :methods:
                | test_structural_compliance - Verifies InstructionLineParser satisfies protocol.
                | test_properties - Verifies name and handlers properties.
    '''

    def test_structural_compliance(self) -> None:
        '''
            Verifies that InstructionLineParser satisfies IInstructionLineParser.
        '''
        parser = InstructionLineParser(handlers=())
        self.assertIsInstance(parser, IInstructionLineParser)

    def test_properties(self) -> None:
        '''
            Verifies that properties return expected values.
        '''
        parser = InstructionLineParser(handlers=())
        self.assertEqual(parser.name, 'instruction_line_parser')
        self.assertEqual(parser.handlers, ())


if __name__ == '__main__':
    main()
