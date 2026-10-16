# -*- coding: UTF-8 -*-

'''
Module
    dependencies_test.py
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
    Unit tests for DisassemblerDependencies dataclass.
'''

from __future__ import annotations

from dataclasses import FrozenInstanceError
from unittest import TestCase
from unittest import main
from unittest.mock import MagicMock

from scaralang.core.service.disassembler.dependencies import DisassemblerDependencies
from scaralang.core.service.disassembler.frame.iframe import IFrameDetailDecoder
from scaralang.core.service.protocol.ibinary_frame_parser import IBinaryFrameParser

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.9'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestDisassemblerDependencies(TestCase):
    '''
        Test cases verifying DisassemblerDependencies dataclass.

        It defines:

            :methods:
                | test_initialization - Verifies attributes are preserved.
                | test_immutability - Verifies frozen immutability constraint.
    '''

    def test_initialization(self) -> None:
        '''
            Verifies DisassemblerDependencies fields are properly assigned.
        '''
        mock_parser = MagicMock(spec=IBinaryFrameParser)
        mock_decoder = MagicMock(spec=IFrameDetailDecoder)
        deps = DisassemblerDependencies(
            parser=mock_parser,
            detail_decoder=mock_decoder,
        )
        self.assertIs(deps.parser, mock_parser)
        self.assertIs(deps.detail_decoder, mock_decoder)

    def test_immutability(self) -> None:
        '''
            Verifies that modifying attributes raises FrozenInstanceError.
        '''
        mock_parser = MagicMock(spec=IBinaryFrameParser)
        mock_decoder = MagicMock(spec=IFrameDetailDecoder)
        deps = DisassemblerDependencies(
            parser=mock_parser,
            detail_decoder=mock_decoder,
        )
        with self.assertRaises(FrozenInstanceError):
            deps.parser = mock_parser  # type: ignore[misc]


if __name__ == '__main__':
    main()
