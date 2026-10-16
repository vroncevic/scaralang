# -*- coding: UTF-8 -*-

'''
Module
    dependencies.py
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
    Defines parameter bundle dataclass ScriptDependencies for ScriptPlanCompiler.
'''

from __future__ import annotations

from dataclasses import dataclass

from scaralang.core.service.compiler.plan.ast.icompiler import IAstPlanCompiler
from scaralang.core.service.linter.ilinter import ILinter
from scaralang.core.service.parser.iparser import IScaraParser

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.9'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@dataclass(frozen=True, slots=True)
class ScriptDependencies:
    '''
        Immutable dependency bundle required by ScriptPlanCompiler.

        It defines:

            :attributes:
                | parser - Injected AST parser protocol instance.
                | compiler - Injected AST plan compiler protocol instance.
                | linter - Injected static analysis linter protocol instance.
    '''

    parser: IScaraParser
    compiler: IAstPlanCompiler
    linter: ILinter
