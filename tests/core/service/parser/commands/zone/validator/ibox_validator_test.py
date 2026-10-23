# -*- coding: UTF-8 -*-

'''
Module
    ibox_validator_test.py
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
    Unit tests for IBoxZoneValidator structural protocol interface.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main

from scaralang.core.service.parser.commands.zone.validator.box_validator import BoxZoneValidator
from scaralang.core.service.parser.commands.zone.validator.ibox_validator import IBoxZoneValidator

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestIBoxZoneValidator(TestCase):
    '''
        Test cases verifying IBoxZoneValidator protocol structural conformance.

        It defines:

            :methods:
                | test_conforming_instance - Verifies conforming instance passes isinstance.
                | test_non_conforming_instance - Verifies non-conforming instance fails isinstance.
    '''

    def test_conforming_instance(self) -> None:
        '''
            Verifies conforming instance passes structural typing check.

            :exceptions: None.
        '''
        validator = BoxZoneValidator()
        self.assertIsInstance(validator, IBoxZoneValidator)

    def test_non_conforming_instance(self) -> None:
        '''
            Verifies non-conforming instance fails structural typing check.

            :exceptions: None.
        '''
        dummy = object()
        self.assertNotIsInstance(dummy, IBoxZoneValidator)


if __name__ == '__main__':
    main()
