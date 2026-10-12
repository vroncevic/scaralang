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
    Unit tests for FlowProvides container.
'''

from __future__ import annotations

from dataclasses import FrozenInstanceError
from unittest import TestCase, main

from scaralang.core.service.parser.commands.flow.disable import DisableParser
from scaralang.core.service.parser.commands.flow.enable import EnableParser
from scaralang.core.service.parser.commands.flow.estop import EstopParser
from scaralang.core.service.parser.commands.flow.hold import HoldParser
from scaralang.core.service.parser.commands.flow.provides import FlowProvides
from scaralang.core.service.parser.commands.flow.resume import ResumeParser
from scaralang.core.service.parser.commands.flow.sync import SyncParser
from scaralang.core.service.parser.commands.flow.wait import WaitParser
from scaralang.core.service.parser.commands.icommand_parser import ICommandParser

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.8'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestFlowProvides(TestCase):
    '''
        Test cases verifying FlowProvides container properties and immutability.

        It defines:

            :methods:
                | test_provides_encapsulation - Verifies attributes and protocol types.
                | test_immutability - Verifies frozen container raises FrozenInstanceError.
    '''

    def test_provides_encapsulation(self) -> None:
        '''
            Verifies attributes and protocol conformance of provided parsers.
        '''
        disable_parser = DisableParser()
        enable_parser = EnableParser()
        estop_parser = EstopParser()
        hold_parser = HoldParser()
        resume_parser = ResumeParser()
        sync_parser = SyncParser()
        wait_parser = WaitParser()
        provides = FlowProvides(
            disable_parser=disable_parser,
            enable_parser=enable_parser,
            estop_parser=estop_parser,
            hold_parser=hold_parser,
            resume_parser=resume_parser,
            sync_parser=sync_parser,
            wait_parser=wait_parser,
            parsers=(
                wait_parser,
                sync_parser,
                hold_parser,
                resume_parser,
                enable_parser,
                disable_parser,
                estop_parser,
            ),
        )
        self.assertIs(provides.disable_parser, disable_parser)
        self.assertIs(provides.enable_parser, enable_parser)
        self.assertIs(provides.estop_parser, estop_parser)
        self.assertIs(provides.hold_parser, hold_parser)
        self.assertIs(provides.resume_parser, resume_parser)
        self.assertIs(provides.sync_parser, sync_parser)
        self.assertIs(provides.wait_parser, wait_parser)
        self.assertEqual(len(provides.parsers), 7)
        for parser in provides.parsers:
            self.assertIsInstance(parser, ICommandParser)

    def test_immutability(self) -> None:
        '''
            Verifies container immutability on attribute reassignment.
        '''
        disable_parser = DisableParser()
        enable_parser = EnableParser()
        estop_parser = EstopParser()
        hold_parser = HoldParser()
        resume_parser = ResumeParser()
        sync_parser = SyncParser()
        wait_parser = WaitParser()
        provides = FlowProvides(
            disable_parser=disable_parser,
            enable_parser=enable_parser,
            estop_parser=estop_parser,
            hold_parser=hold_parser,
            resume_parser=resume_parser,
            sync_parser=sync_parser,
            wait_parser=wait_parser,
            parsers=(
                wait_parser,
                sync_parser,
                hold_parser,
                resume_parser,
                enable_parser,
                disable_parser,
                estop_parser,
            ),
        )
        with self.assertRaises(FrozenInstanceError):
            setattr(provides, 'disable_parser', disable_parser)


if __name__ == '__main__':
    main()
