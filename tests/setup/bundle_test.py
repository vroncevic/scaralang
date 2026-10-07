# -*- coding: UTF-8 -*-

'''
Module
    bundle_test.py
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
    Unit tests for ScaralangBundle dataclass.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main

from scaralang.setup.bundle import ScaralangBundle
from scaralang.setup.factory import ScaralangBundleFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.7'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestScaralangBundle(TestCase):
    '''
        Test cases verifying ScaralangBundle.

        It defines:

            :methods:
                | test_bundle_creation - Verifies creating bundle and to_dict method.
    '''

    def test_bundle_creation(self) -> None:
        '''
            Verifies bundle creation and conversion to dict.
        '''
        bundle = ScaralangBundleFactory.create_bundle()
        self.assertIsInstance(bundle, ScaralangBundle)
        bundle_dict = bundle.to_dict()
        self.assertIsInstance(bundle_dict, dict)
        self.assertIn('base', bundle_dict)
        self.assertIn('cli', bundle_dict)


if __name__ == '__main__':
    main()
