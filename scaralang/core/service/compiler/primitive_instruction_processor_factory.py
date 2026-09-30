# -*- coding: UTF-8 -*-

'''
Module
    primitive_instruction_processor_factory.py
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
    Factory service for creating IPrimitiveInstructionProcessor instances.
'''

from __future__ import annotations

from collections.abc import Sequence

from scaralang.core.service.compiler.iprimitive_instruction_processor import IPrimitiveInstructionProcessor
from scaralang.core.service.compiler.primitive.iprimitive_compiler import IPrimitiveCompiler
from scaralang.core.service.compiler.primitive_instruction_processor import PrimitiveInstructionProcessor

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class PrimitiveInstructionProcessorFactory:
    '''
        Factory providing configured IPrimitiveInstructionProcessor instances.

        It defines:

            :methods:
                | create - Instantiates a new IPrimitiveInstructionProcessor.
                | get_version - Returns factory version string.
    '''

    @classmethod
    def create(
        cls,
        *,
        primitive_compilers: Sequence[IPrimitiveCompiler],
    ) -> IPrimitiveInstructionProcessor:
        '''
            Instantiates a new IPrimitiveInstructionProcessor instance.

            :param primitive_compilers: Sequence of IPrimitiveCompiler components.
            :return: Configured IPrimitiveInstructionProcessor instance.
            :exceptions: None.
        '''
        return PrimitiveInstructionProcessor(
            primitive_compilers=primitive_compilers
        )

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns the factory version string.

            :return: Factory version string.
            :exceptions: None.
        '''
        return __version__
