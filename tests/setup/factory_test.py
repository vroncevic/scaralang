# -*- coding: UTF-8 -*-

'''
Module
    factory_test.py
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
    Unit tests for ScaralangBundleFactory class.
'''

from __future__ import annotations

from os.path import abspath
from os.path import dirname
from os.path import join
from unittest import TestCase
from unittest import main

from scaralang.setup.bundle import ScaralangBundle
from scaralang.setup.factory import ScaralangBundleFactory
from scaralang.setup.options import ScaralangBundleOptions

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestScaralangBundleFactory(TestCase):
    '''
        Test cases verifying ScaralangBundleFactory.

        It defines:

            :methods:
                | test_create_bundle - Verifies creating initialized bundle.
                | test_create_bundle_with_options - Verifies bundle creation with options.
                | test_get_version - Verifies factory version string.
    '''

    def test_create_bundle(self) -> None:
        '''
            Verifies bundle creation.
        '''
        bundle = ScaralangBundleFactory.create_bundle()
        self.assertIsInstance(bundle, ScaralangBundle)

    def test_get_version(self) -> None:
        '''
            Verifies factory version returns valid string.
        '''
        version = ScaralangBundleFactory.get_version()
        self.assertEqual(version, '1.0.4')

    def test_create_bundle_with_options(self) -> None:
        '''
            Verifies bundle creation with explicit options.
        '''
        cfg_path: str = join(
            dirname(dirname(dirname(abspath(__file__)))),
            'scaralang', 'infrastructure', 'config', 'scaralang.cfg'
        )
        bundle = ScaralangBundleFactory.create_bundle(
            options=ScaralangBundleOptions(
                info_file=cfg_path,
                verbose=True,
            )
        )
        self.assertIsInstance(bundle, ScaralangBundle)


if __name__ == '__main__':
    main()
