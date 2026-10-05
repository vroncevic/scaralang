# -*- coding: UTF-8 -*-

'''
Module
    iscara_dsl_linter.py
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
    Defines role interface IScaraDslLinter for static analysis linting of SCARA DSL scripts.
'''

from __future__ import annotations

from typing import Protocol, runtime_checkable

from scaralang.core.model.dsl.diagnostic.scara_diagnostic import ScaraDiagnostic

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.5'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class IScaraDslLinter(Protocol):
    '''
        Role interface protocol for SCARA DSL script static analysis linting.

        It defines:

            :methods:
                | lint_script - Performs static analysis checks on DSL script string.
                | get_version - Returns the linter version string representation.
    '''

    def lint_script(self, *, source: str) -> tuple[ScaraDiagnostic, ...]:
        '''
            Performs static analysis checks on a DSL script string.

            :param source: Raw .scara script text.
            :return: Tuple of ScaraDiagnostic findings.
            :exceptions: None.
        '''

    def get_version(self) -> str:
        '''
            Returns the linter version string representation.

            :return: Semantic version string.
        '''
