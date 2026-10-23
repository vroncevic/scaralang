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
    Unit tests for AstPlanCompilerFactory.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main

from scaralang.core.service.compiler.plan.ast.factory import AstPlanCompilerFactory
from scaralang.core.service.compiler.plan.ast.icompiler import IAstPlanCompiler
from scaralang.infrastructure.trajectory.validation.factory import DefaultValidationFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestAstPlanCompilerFactory(TestCase):
    '''
        Test cases verifying AstPlanCompilerFactory.

        It defines:

            :methods:
                | setUp - Prepares validator fixture.
                | test_create - Verifies factory returns IAstPlanCompiler.
                | test_get_version - Verifies factory version string.
    '''

    def setUp(self) -> None:
        '''
            Sets up validator fixture.
        '''
        self.validator = DefaultValidationFactory.create().plan

    def test_create(self) -> None:
        '''
            Verifies factory produces IAstPlanCompiler instance.
        '''
        compiler: IAstPlanCompiler = AstPlanCompilerFactory.create(
            validator=self.validator
        )
        self.assertIsInstance(compiler, IAstPlanCompiler)

    def test_get_version(self) -> None:
        '''
            Verifies factory version string is non-empty.
        '''
        version: str = AstPlanCompilerFactory.get_version()
        self.assertTrue(bool(version))


if __name__ == '__main__':
    main()
