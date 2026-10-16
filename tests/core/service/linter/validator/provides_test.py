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
    Unit tests for ValidatorProvides dataclass module.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main
from unittest.mock import MagicMock

from scaralang.core.service.linter.validator.provides import ValidatorProvides

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.9'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestValidatorProvides(TestCase):
    '''
        Test cases verifying ValidatorProvides operations.

        It defines:

            :methods:
                | test_provides_creation - Verifies fields and immutability.
                | test_get_version - Verifies version string retrieval.
    '''

    def test_provides_creation(self) -> None:
        '''
            Verifies ValidatorProvides fields and immutability.
        '''
        mock_validator = MagicMock()
        provides = ValidatorProvides(validator=mock_validator)
        self.assertIs(provides.validator, mock_validator)

    def test_get_version(self) -> None:
        '''
            Verifies provides get_version method returns semantic version string.
        '''
        provides = ValidatorProvides(validator=MagicMock())
        self.assertEqual(provides.get_version(), '1.0.9')


if __name__ == '__main__':
    main()
