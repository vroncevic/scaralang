# -*- coding: UTF-8 -*-

'''
Module
    factory.py
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
    Factory instantiating lint command subsystem components.
'''

from __future__ import annotations

from scaralang.core.service.linter.diagnostic.factory import DiagnosticFactory
from scaralang.infrastructure.command.lint.definition import LintCommandDefinition
from scaralang.infrastructure.command.lint.dependencies import LintDependencies
from scaralang.infrastructure.command.lint.error.factory import ErrorFactory
from scaralang.infrastructure.command.lint.error.provides import ErrorProvides
from scaralang.infrastructure.command.lint.executor import LintCommandExecutor
from scaralang.infrastructure.command.lint.provides import LintProvides
from scaralang.infrastructure.linter.script.factory import DefaultScriptLinterFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.8'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class LintFactory:
    '''
        Factory providing Lint command subsystem instances.

        It defines:

            :methods:
                | create - Constructs and wires LintProvides container.
                | get_version - Returns factory version string.
    '''

    @classmethod
    def create(cls) -> LintProvides:
        '''
            Constructs and wires LintProvides container with configured collaborators.

            :return: Fully configured LintProvides container.
            :exceptions: None.
        '''
        definition: LintCommandDefinition = LintCommandDefinition()
        error_provides: ErrorProvides = ErrorFactory.create()
        deps: LintDependencies = LintDependencies(
            service=DefaultScriptLinterFactory.create().linter,
            diagnostic_formatter=DiagnosticFactory.create().formatter,
            error_handler=error_provides.handler,
        )
        executor: LintCommandExecutor = LintCommandExecutor(
            definition=definition,
            dependencies=deps,
        )

        return LintProvides(
            executor=executor,
            definition=definition,
        )

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns the factory version string.

            :return: Semantic version string.
            :exceptions: None.
        '''
        return __version__
