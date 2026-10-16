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
    Unit tests for IAstPlanCompiler protocol contract.
'''

from __future__ import annotations

from typing import Protocol
from unittest import TestCase, main

from scaralang.core.service.compiler.plan.ast.icompiler import IAstPlanCompiler

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.9'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestIAstPlanCompiler(TestCase):
    '''
        Test cases verifying IAstPlanCompiler protocol contract.

        It defines:

            :methods:
                | test_protocol_definition - Verifies protocol methods.
    '''

    def test_protocol_definition(self) -> None:
        '''
            Verifies that IAstPlanCompiler defines required compile and get_version.
        '''
        self.assertTrue(issubclass(IAstPlanCompiler, Protocol))
        self.assertTrue(hasattr(IAstPlanCompiler, 'compile'))
        self.assertTrue(hasattr(IAstPlanCompiler, 'get_version'))
        self.assertFalse(hasattr(IAstPlanCompiler, 'lint'))


if __name__ == '__main__':
    main()
