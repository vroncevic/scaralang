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
    Subsystem factory wiring instruction pipeline and instruction processor.
'''

from __future__ import annotations

from scaralang.core.service.compiler.instruction.dependencies import InstructionDependencies
from scaralang.core.service.compiler.instruction.pipeline.dependencies import PipelineDependencies
from scaralang.core.service.compiler.instruction.pipeline.factory import PipelineFactory
from scaralang.core.service.compiler.instruction.pipeline.ipipeline import IInstructionPipeline
from scaralang.core.service.compiler.instruction.processor.dependencies import ProcessorDependencies
from scaralang.core.service.compiler.instruction.processor.factory import ProcessorFactory
from scaralang.core.service.compiler.instruction.processor.iprocessor import IPrimitiveInstructionProcessor
from scaralang.core.service.compiler.instruction.provides import InstructionProvides

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.8'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class InstructionFactory:
    '''
        Subsystem factory assembling and providing instruction execution services.

        It defines:

            :methods:
                | create - Assembles processor and pipeline, returning InstructionProvides.
                | get_version - Returns factory version string.
    '''

    @classmethod
    def create(
        cls,
        *,
        dependencies: InstructionDependencies,
    ) -> InstructionProvides:
        '''
            Assembles instruction processor and pipeline components.

            :param dependencies: Parameter bundle with expanders and compilers.
            :return: InstructionProvides bundle with wired interfaces.
            :exceptions: None.
        '''
        processor: IPrimitiveInstructionProcessor = ProcessorFactory.create(
            dependencies=ProcessorDependencies(
                compilers=dependencies.primitive_compilers
            )
        )
        pipeline: IInstructionPipeline = PipelineFactory.create(
            dependencies=PipelineDependencies(
                macro_expanders=dependencies.macro_expanders,
                processor=processor,
            )
        )
        return InstructionProvides(pipeline=pipeline, processor=processor)

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns the factory version string.

            :return: Factory version string.
            :exceptions: None.
        '''
        return __version__
