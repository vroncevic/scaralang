# -*- coding: UTF-8 -*-

'''
Module
    icompiler_test.py
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
    Unit tests for IScriptPlanCompiler protocol contract.
'''

from __future__ import annotations

from typing import Protocol
from unittest import TestCase, main

from scaralang.core.service.compiler.plan.script.icompiler import (
    IScriptPlanCompiler,
)

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.8'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestIScriptPlanCompiler(TestCase):
    '''
        Test cases verifying IScriptPlanCompiler protocol contract.

        It defines:

            :methods:
                | test_protocol_definition - Verifies protocol methods.
    '''

    def test_protocol_definition(self) -> None:
        '''
            Verifies IScriptPlanCompiler defines required methods and satisfies ISP.
        '''
        self.assertTrue(issubclass(IScriptPlanCompiler, Protocol))
        self.assertTrue(hasattr(IScriptPlanCompiler, 'compile'))
        self.assertTrue(hasattr(IScriptPlanCompiler, 'compile_script'))
        self.assertTrue(hasattr(IScriptPlanCompiler, 'compile_program'))
        self.assertTrue(hasattr(IScriptPlanCompiler, 'get_version'))
        self.assertFalse(hasattr(IScriptPlanCompiler, 'lint'))


if __name__ == '__main__':
    main()
