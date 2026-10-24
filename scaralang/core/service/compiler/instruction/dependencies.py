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
    Parameter bundle dataclass for instruction subsystem dependencies.
'''

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass

from scaralang.core.service.compiler.macro.iexpander import IMacroExpander
from scaralang.core.service.compiler.macro.repeat.iexpander import IRepeatExpander
from scaralang.core.service.compiler.macro.subroutine.iexpander import ISubroutineExpander
from scaralang.core.service.compiler.primitive.icompiler import IPrimitiveCompiler

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@dataclass(frozen=True, slots=True)
class InstructionDependencies:
    '''
        Parameter bundle encapsulating instruction subsystem inbound dependencies.

        It defines:

            :attributes:
                | subroutine_expander - Injected ISubroutineExpander component.
                | repeat_expander - Injected IRepeatExpander component.
                | macro_expanders - Sequence of registered IMacroExpander components.
                | primitive_compilers - Sequence of registered IPrimitiveCompiler components.
    '''

    subroutine_expander: ISubroutineExpander
    repeat_expander: IRepeatExpander
    macro_expanders: Sequence[IMacroExpander]
    primitive_compilers: Sequence[IPrimitiveCompiler]
