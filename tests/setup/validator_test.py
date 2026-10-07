# -*- coding: UTF-8 -*-

'''
Module
    validator_test.py
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
    Unit tests for ScaralangBundleValidator class.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main

from scaralang.setup.factory import ScaralangBundleFactory
from scaralang.setup.validator import ScaralangBundleValidator

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.7'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestScaralangBundleValidator(TestCase):
    '''
        Test cases verifying ScaralangBundleValidator.

        It defines:

            :methods:
                | test_is_valid_success - Verifies validation of a properly built bundle.
                | test_is_valid_failure - Verifies validation fails for invalid types.
    '''

    def test_is_valid_success(self) -> None:
        '''
            Verifies valid bundle returns True.
        '''
        bundle = ScaralangBundleFactory.create_bundle()
        self.assertTrue(ScaralangBundleValidator.is_valid(bundle))

    def test_is_valid_failure(self) -> None:
        '''
            Verifies non-bundle object returns False.
        '''
        self.assertFalse(ScaralangBundleValidator.is_valid(None))
        self.assertFalse(ScaralangBundleValidator.is_valid('invalid'))


if __name__ == '__main__':
    main()
