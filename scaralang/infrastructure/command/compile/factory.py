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
    Factory instantiating and wiring compile command subsystem components.
'''

from __future__ import annotations

from scaralang.infrastructure.command.compile.definition import CompileCommandDefinition
from scaralang.infrastructure.command.compile.dependencies import CompileDependencies
from scaralang.infrastructure.command.compile.error.factory import ErrorFactory
from scaralang.infrastructure.command.compile.error.provides import ErrorProvides
from scaralang.infrastructure.command.compile.executor import CompileCommandExecutor
from scaralang.infrastructure.command.compile.inspection.presentation.factory import PresentationFactory
from scaralang.infrastructure.command.compile.inspection.presentation.provides import PresentationProvides
from scaralang.infrastructure.command.compile.provides import CompileProvides
from scaralang.infrastructure.command.compile.telemetry.factory import TelemetryFactory
from scaralang.infrastructure.command.compile.telemetry.provides import TelemetryProvides
from scaralang.infrastructure.compiler.factory import DefaultCompilerFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class CompileFactory:
    '''
        Factory providing Compile command subsystem instances.

        It defines:

            :methods:
                | create - Constructs and wires CompileProvides container.
                | get_version - Returns factory version string.
    '''

    @classmethod
    def create(cls) -> CompileProvides:
        '''
            Constructs and wires CompileProvides container with configured collaborators.

            :return: Fully configured CompileProvides container.
            :exceptions: None.
        '''
        definition: CompileCommandDefinition = CompileCommandDefinition()
        telemetry: TelemetryProvides = TelemetryFactory.create()
        error_provides: ErrorProvides = ErrorFactory.create()
        presentation_provides: PresentationProvides = PresentationFactory.create()
        deps: CompileDependencies = CompileDependencies(
            compiler=DefaultCompilerFactory.create(),
            inspection_presenter=presentation_provides.presenter,
            telemetry_formatter=telemetry.formatter,
            error_handler=error_provides.handler,
        )
        executor: CompileCommandExecutor = CompileCommandExecutor(
            definition=definition,
            dependencies=deps,
        )

        return CompileProvides(
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
