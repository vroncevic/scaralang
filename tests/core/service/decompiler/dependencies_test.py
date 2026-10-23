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
    Unit tests for DecompilerDependencies dataclass.
'''

from __future__ import annotations

from dataclasses import FrozenInstanceError
from unittest import TestCase
from unittest import main
from unittest.mock import MagicMock

from scaralang.core.service.decompiler.dependencies import DecompilerDependencies
from scaralang.core.service.decompiler.frame.iframe import IFrameDecompiler
from scaralang.core.service.protocol.iparser import IBinaryFrameParser

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestDecompilerDependencies(TestCase):
    '''
        Test cases verifying DecompilerDependencies dataclass.

        It defines:

            :methods:
                | test_initialization - Verifies attributes are preserved.
                | test_immutability - Verifies frozen immutability constraint.
    '''

    def test_initialization(self) -> None:
        '''
            Verifies DecompilerDependencies fields are properly assigned.
        '''
        mock_parser = MagicMock(spec=IBinaryFrameParser)
        mock_frame_decompiler = MagicMock(spec=IFrameDecompiler)
        deps = DecompilerDependencies(
            parser=mock_parser,
            frame_decompiler=mock_frame_decompiler,
        )
        self.assertIs(deps.parser, mock_parser)
        self.assertIs(deps.frame_decompiler, mock_frame_decompiler)

    def test_immutability(self) -> None:
        '''
            Verifies that modifying attributes raises FrozenInstanceError.
        '''
        mock_parser = MagicMock(spec=IBinaryFrameParser)
        mock_frame_decompiler = MagicMock(spec=IFrameDecompiler)
        deps = DecompilerDependencies(
            parser=mock_parser,
            frame_decompiler=mock_frame_decompiler,
        )
        with self.assertRaises(FrozenInstanceError):
            deps.parser = mock_parser  # type: ignore[misc]


if __name__ == '__main__':
    main()
