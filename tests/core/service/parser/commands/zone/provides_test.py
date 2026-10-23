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
    Unit tests for ZoneProvides container.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main

from scaralang.core.service.parser.commands.zone.definition import ZoneDefParser
from scaralang.core.service.parser.commands.zone.provides import ZoneProvides
from scaralang.core.service.parser.commands.zone.validator.box_validator import BoxZoneValidator
from scaralang.core.service.parser.commands.zone.validator.circle_validator import CircleZoneValidator

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestZoneProvides(TestCase):
    '''
        Test cases verifying ZoneProvides container behavior.

        It defines:

            :methods:
                | test_parsers_tuple - Verifies parsers sequence in container.
                | test_get_version - Verifies get_version returns semantic version.
    '''

    def test_parsers_tuple(self) -> None:
        '''
            Verifies parsers collection is correctly held in container.

            :exceptions: None.
        '''
        parser = ZoneDefParser(
            box_validator=BoxZoneValidator(),
            circle_validator=CircleZoneValidator(),
        )
        provides = ZoneProvides(parsers=(parser,))
        self.assertEqual(len(provides.parsers), 1)
        self.assertIs(provides.parsers[0], parser)

    def test_get_version(self) -> None:
        '''
            Verifies get_version returns implementation version string.

            :exceptions: None.
        '''
        provides = ZoneProvides(parsers=())
        self.assertEqual(provides.get_version(), __version__)


if __name__ == '__main__':
    main()
