# -*- coding: UTF-8 -*-

'''
Module
    repl_single_command_compiler_factory_test.py
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
    Unit tests for ReplSingleCommandCompilerFactory class.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main

from scaralang.core.service.dsl.iscara_dsl_service import IScaraDslService
from scaralang.infrastructure.cli.repl.compiler.irepl_single_command_compiler import IReplSingleCommandCompiler
from scaralang.infrastructure.cli.repl.compiler.repl_single_command_compiler import ReplSingleCommandCompiler
from scaralang.infrastructure.cli.repl.compiler.repl_single_command_compiler_factory import ReplSingleCommandCompilerFactory
from scaralang.setup.factory import ScaralangBundleFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestReplSingleCommandCompilerFactory(TestCase):
    '''
        Test cases verifying ReplSingleCommandCompilerFactory.

        It defines:

            :methods:
                | test_create - Verifies factory instantiates compiler correctly.
                | test_get_version - Verifies factory returns version string.
    '''

    def test_create(self) -> None:
        '''Verifies factory builds ReplSingleCommandCompiler instance.'''
        service: IScaraDslService = ScaralangBundleFactory.create_bundle().service
        compiler = ReplSingleCommandCompilerFactory.create(service=service)
        self.assertIsInstance(compiler, ReplSingleCommandCompiler)
        self.assertIsInstance(compiler, IReplSingleCommandCompiler)

    def test_get_version(self) -> None:
        '''Verifies factory returns a valid semantic version string.'''
        version: str = ReplSingleCommandCompilerFactory.get_version()
        self.assertIsInstance(version, str)
        self.assertTrue(len(version) > 0)


if __name__ == '__main__':
    main()
