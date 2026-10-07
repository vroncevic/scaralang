# -*- coding: UTF-8 -*-

'''
Module
    instruction_pipeline_factory.py
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
    Factory service providing wired InstructionPipeline instances.
'''

from __future__ import annotations

from collections.abc import Sequence

from scaralang.core.service.compiler.iinstruction_pipeline import IInstructionPipeline
from scaralang.core.service.compiler.instruction_pipeline import InstructionPipeline
from scaralang.core.service.compiler.iprimitive_instruction_processor import IPrimitiveInstructionProcessor
from scaralang.core.service.compiler.macro.imacro_expander import IMacroExpander
from scaralang.core.service.compiler.primitive.iprimitive_compiler import IPrimitiveCompiler
from scaralang.core.service.compiler.primitive_instruction_processor_factory import PrimitiveInstructionProcessorFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.7'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class InstructionPipelineFactory:
    '''
        Factory providing wired InstructionPipeline instances.

        It defines:

            :methods:
                | create - Instantiates a new InstructionPipeline with default processor.
                | create_with_collaborators - Instantiates with injected processor.
                | get_version - Returns factory version string.
    '''

    @classmethod
    def create(
        cls,
        *,
        macro_expanders: Sequence[IMacroExpander],
        primitive_compilers: Sequence[IPrimitiveCompiler],
    ) -> IInstructionPipeline:
        '''
            Instantiates a new InstructionPipeline with wired processor.

            :param macro_expanders: Sequence of IMacroExpander components.
            :param primitive_compilers: Sequence of IPrimitiveCompiler components.
            :return: Wired IInstructionPipeline instance.
            :exceptions: None.
        '''
        processor: IPrimitiveInstructionProcessor = (
            PrimitiveInstructionProcessorFactory.create(
                primitive_compilers=primitive_compilers
            )
        )
        return InstructionPipeline(macro_expanders=macro_expanders, processor=processor)

    @classmethod
    def create_with_collaborators(
        cls,
        *,
        macro_expanders: Sequence[IMacroExpander],
        processor: IPrimitiveInstructionProcessor,
    ) -> IInstructionPipeline:
        '''
            Instantiates InstructionPipeline with injected collaborators.

            :param macro_expanders: Sequence of IMacroExpander components.
            :param processor: Injected IPrimitiveInstructionProcessor instance.
            :return: Configured IInstructionPipeline instance.
            :exceptions: None.
        '''
        return InstructionPipeline(macro_expanders=macro_expanders, processor=processor)

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns the factory version string.

            :return: Factory version string.
            :exceptions: None.
        '''
        return __version__
