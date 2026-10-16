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
    Factory coordinating inspection presentation subsystem components.
'''

from __future__ import annotations

from scaralang.infrastructure.command.compile.inspection.framing.factory import FramingFactory
from scaralang.infrastructure.command.compile.inspection.framing.provides import FramingProvides
from scaralang.infrastructure.command.compile.inspection.hex.factory import HexFactory
from scaralang.infrastructure.command.compile.inspection.hex.provides import HexProvides
from scaralang.infrastructure.command.compile.inspection.payload.factory import PayloadFactory
from scaralang.infrastructure.command.compile.inspection.payload.provides import PayloadProvides
from scaralang.infrastructure.command.compile.inspection.presentation.provides import PresentationProvides
from scaralang.infrastructure.command.compile.inspection.presentation.program.factory import ProgramFactory
from scaralang.infrastructure.command.compile.inspection.presentation.program.provides import ProgramProvides
from scaralang.infrastructure.command.compile.inspection.presentation.step.dependencies import StepDependencies
from scaralang.infrastructure.command.compile.inspection.presentation.step.factory import StepFactory
from scaralang.infrastructure.command.compile.inspection.presentation.step.provides import StepProvides

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.9'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class PresentationFactory:
    '''
        Factory providing Presentation inspection service instances.

        It defines:

            :methods:
                | create - Constructs and wires PresentationProvides container.
                | get_version - Returns factory version string.
    '''

    @classmethod
    def create(cls) -> PresentationProvides:
        '''
            Constructs and wires PresentationProvides container from collaborating sub-factories.

            :return: Fully configured PresentationProvides container.
            :exceptions: None.
        '''
        framing_provides: FramingProvides = FramingFactory.create()
        hex_provides: HexProvides = HexFactory.create()
        payload_provides: PayloadProvides = PayloadFactory.create()
        step_deps: StepDependencies = StepDependencies(
            header_formatter=framing_provides.header_formatter,
            payload_formatter=payload_provides.formatter,
            trailer_formatter=framing_provides.trailer_formatter,
            hex_formatter=hex_provides.formatter,
        )
        step_provides: StepProvides = StepFactory.create(dependencies=step_deps)
        program_provides: ProgramProvides = ProgramFactory.create(
            step_presenter=step_provides.presenter
        )
        return PresentationProvides(
            presenter=program_provides.presenter,
            step_presenter=step_provides.presenter,
        )

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns the factory version string.

            :return: Semantic version string.
            :exceptions: None.
        '''
        return __version__
