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
    Unit tests for PlanFactory.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main
from unittest.mock import MagicMock

from scaralang.core.service.compiler.plan.ast.icompiler import IAstPlanCompiler
from scaralang.core.service.compiler.plan.dependencies import PlanDependencies
from scaralang.core.service.compiler.plan.factory import PlanFactory
from scaralang.core.service.compiler.plan.provides import PlanProvides
from scaralang.core.service.compiler.plan.script.icompiler import IScriptPlanCompiler
from scaralang.infrastructure.trajectory.validation.factory import DefaultValidationFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestPlanFactory(TestCase):
    '''
        Test cases verifying PlanFactory assembly and creation.

        It defines:

            :methods:
                | setUp - Initializes test dependencies fixture.
                | test_create - Verifies factory returns PlanProvides.
                | test_get_version - Verifies factory version string.
    '''

    def setUp(self) -> None:
        '''
            Sets up dependencies fixture with validator, parser, and linter.
        '''
        validator = DefaultValidationFactory.create().plan
        self.dependencies = PlanDependencies(
            validator=validator,
            parser=MagicMock(),
            linter=MagicMock(),
        )

    def test_create(self) -> None:
        '''
            Verifies factory produces PlanProvides containing valid compilers.
        '''
        provides: PlanProvides = PlanFactory.create(
            dependencies=self.dependencies
        )
        self.assertIsInstance(provides, PlanProvides)
        self.assertIsInstance(provides.ast_compiler, IAstPlanCompiler)
        self.assertIsInstance(provides.script_compiler, IScriptPlanCompiler)

    def test_get_version(self) -> None:
        '''
            Verifies factory version string is non-empty.
        '''
        version: str = PlanFactory.get_version()
        self.assertTrue(bool(version))


if __name__ == '__main__':
    main()
