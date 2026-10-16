# -*- coding: UTF-8 -*-

'''
Module
    provides_test.py
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
    Unit tests for FrameProvides container.
'''

from __future__ import annotations

from dataclasses import FrozenInstanceError
from unittest import TestCase, main

from scaralang.core.service.parser.commands.frame.provides import FrameProvides
from scaralang.core.service.parser.commands.frame.reset import FrameResetParser
from scaralang.core.service.parser.commands.frame.set import FrameSetParser
from scaralang.core.service.parser.commands.icommand_parser import ICommandParser

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.9'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestFrameProvides(TestCase):
    '''
        Test cases verifying FrameProvides container properties and immutability.

        It defines:

            :methods:
                | test_provides_encapsulation - Verifies attributes and protocol types.
                | test_immutability - Verifies frozen container raises FrozenInstanceError.
    '''

    def test_provides_encapsulation(self) -> None:
        '''
            Verifies attributes and protocol conformance of provided parsers.
        '''
        reset_parser = FrameResetParser()
        set_parser = FrameSetParser()
        provides = FrameProvides(
            reset_parser=reset_parser,
            set_parser=set_parser,
            parsers=(reset_parser, set_parser),
        )
        self.assertIs(provides.reset_parser, reset_parser)
        self.assertIs(provides.set_parser, set_parser)
        self.assertEqual(len(provides.parsers), 2)
        for parser in provides.parsers:
            self.assertIsInstance(parser, ICommandParser)

    def test_immutability(self) -> None:
        '''
            Verifies container immutability on attribute reassignment.
        '''
        reset_parser = FrameResetParser()
        set_parser = FrameSetParser()
        provides = FrameProvides(
            reset_parser=reset_parser,
            set_parser=set_parser,
            parsers=(reset_parser, set_parser),
        )
        with self.assertRaises(FrozenInstanceError):
            setattr(provides, 'reset_parser', reset_parser)


if __name__ == '__main__':
    main()
