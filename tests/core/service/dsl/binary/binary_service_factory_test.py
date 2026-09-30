# -*- coding: UTF-8 -*-

'''
Module
    binary_service_factory_test.py
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
    Unit tests for BinaryServiceFactory class.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main
from unittest.mock import MagicMock

from scaralang.core.service.dsl.binary.binary_service_factory import BinaryServiceFactory
from scaralang.core.service.dsl.binary.ibinary_service import IBinaryService
from scaralang.core.service.dsl.scara_dsl_pipeline_bundle import ScaraDslPipelineBundle
from scaralang.core.service.kinematics.default_scara_profile import DefaultScaraProfile

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestBinaryServiceFactory(TestCase):
    '''
        Test cases verifying BinaryServiceFactory operations.

        It defines:

            :methods:
                | test_create - Verifies factory returns IBinaryService instance.
                | test_create_default - Verifies default pipeline construction.
                | test_get_version - Verifies factory version string.
    '''

    def test_create(self) -> None:
        '''
            Verifies create returns an operational IBinaryService instance.
        '''
        mock_compiler = MagicMock()
        mock_disassembler = MagicMock()
        service = BinaryServiceFactory.create(
            compiler=mock_compiler,
            disassembler=mock_disassembler,
        )
        self.assertIsInstance(service, IBinaryService)

    def test_create_default(self) -> None:
        '''
            Verifies create_default returns an operational IBinaryService instance.
        '''
        bundle = ScaraDslPipelineBundle(
            frame_builder=MagicMock(),
            frame_parser=MagicMock(),
            payload_unpacker=MagicMock(),
            kinematics=MagicMock(),
            validator=MagicMock(),
            transmission=DefaultScaraProfile.create_transmission(),
        )
        service = BinaryServiceFactory.create_default(bundle=bundle)
        self.assertIsInstance(service, IBinaryService)

    def test_get_version(self) -> None:
        '''
            Verifies factory version returns valid string.
        '''
        self.assertEqual(BinaryServiceFactory.get_version(), '1.0.2')


if __name__ == '__main__':
    main()
