# -*- coding: UTF-8 -*-

'''
Module
    dependencies_test.py
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
    Unit tests for InstructionDependencies dataclass.
'''

from __future__ import annotations

from unittest import TestCase, main

from scaralang.core.service.compiler.instruction.dependencies import InstructionDependencies
from scaralang.core.service.compiler.macro.repeat.factory import RepeatFactory
from scaralang.core.service.compiler.macro.subroutine.factory import SubroutineFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestInstructionDependencies(TestCase):
    '''
        Test cases verifying InstructionDependencies parameter bundle.

        It defines:

            :methods:
                | test_initialization - Verifies initialization and properties.
    '''

    def test_initialization(self) -> None:
        '''
            Verifies InstructionDependencies holds expanders and compilers.

            :exceptions: None.
        '''
        subroutine_expander = SubroutineFactory.create().expander
        repeat_expander = RepeatFactory.create().expander
        deps = InstructionDependencies(
            subroutine_expander=subroutine_expander,
            repeat_expander=repeat_expander,
            macro_expanders=(),
            primitive_compilers=(),
        )
        self.assertIs(deps.subroutine_expander, subroutine_expander)
        self.assertIs(deps.repeat_expander, repeat_expander)
        self.assertEqual(deps.macro_expanders, ())
        self.assertEqual(deps.primitive_compilers, ())


if __name__ == '__main__':
    main()
