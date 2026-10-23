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
    Unit tests for CompilerFactory.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main
from unittest.mock import MagicMock

from scaralang.core.service.compiler.binary.icompiler import IBinaryCompiler
from scaralang.core.service.compiler.dependencies import CompilerDependencies
from scaralang.core.service.compiler.factory import CompilerFactory
from scaralang.core.service.compiler.icompiler import IScaraCompiler
from scaralang.core.service.compiler.plan.script.icompiler import IScriptPlanCompiler
from scaralang.core.service.compiler.provides import CompilerProvides

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestCompilerFactory(TestCase):
    '''
        Test cases verifying CompilerFactory.

        It defines:

            :methods:
                | test_create - Verifies factory returns CompilerProvides with IScaraCompiler.
                | test_get_version - Verifies factory version string.
    '''

    def test_create(self) -> None:
        '''
            Verifies factory produces CompilerProvides instance with collaborators.
        '''
        mock_plan_compiler = MagicMock(spec=IScriptPlanCompiler)
        mock_binary_compiler = MagicMock(spec=IBinaryCompiler)
        dependencies = CompilerDependencies(
            compiler=mock_plan_compiler,
            binary_compiler=mock_binary_compiler,
        )
        provides: CompilerProvides = CompilerFactory.create(dependencies=dependencies)
        self.assertIsInstance(provides, CompilerProvides)
        self.assertIsInstance(provides.compiler, IScaraCompiler)

    def test_get_version(self) -> None:
        '''
            Verifies factory version string is non-empty.
        '''
        version: str = CompilerFactory.get_version()
        self.assertEqual(version, '1.1.0')


if __name__ == '__main__':
    main()
