# -*- coding: UTF-8 -*-

'''
Module
    scara_dsl_service_factory_test.py
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
    Unit tests for ScaraDslServiceFactory class.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main
from unittest.mock import MagicMock

from scaralang.core.model.kinematics.transmission_parameters import TransmissionParameters
from scaralang.core.service.dsl.iscara_dsl_service import IScaraDslService
from scaralang.core.service.dsl.scara_dsl_pipeline_bundle import ScaraDslPipelineBundle
from scaralang.core.service.dsl.scara_dsl_service_factory import ScaraDslServiceFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestScaraDslServiceFactory(TestCase):
    '''
        Test cases verifying ScaraDslServiceFactory.

        It defines:

            :methods:
                | test_create_from_pipeline - Verifies create with pipeline parameters.
                | test_create_default - Verifies create_default with frame builder and parser.
                | test_get_version - Verifies factory version string.
    '''

    def test_create_from_pipeline(self) -> None:
        '''
            Verifies factory returns IScaraDslService when given pipeline parameters.
        '''
        mock_validator = MagicMock()
        mock_kinematics = MagicMock()
        mock_frame_builder = MagicMock()
        mock_frame_parser = MagicMock()
        mock_payload_unpacker = MagicMock()
        transmission = TransmissionParameters(
            gear_ratio_j1=5.0,
            gear_ratio_j2=5.0,
            leadscrew_pitch_z=4.0,
            gear_ratio_j4=1.0,
            microstepping=16.0,
            steps_per_rev=200.0,
        )
        bundle = ScaraDslPipelineBundle(
            frame_builder=mock_frame_builder,
            frame_parser=mock_frame_parser,
            payload_unpacker=mock_payload_unpacker,
            kinematics=mock_kinematics,
            validator=mock_validator,
            transmission=transmission,
        )
        service = ScaraDslServiceFactory.create(bundle=bundle)
        self.assertIsInstance(service, IScaraDslService)

    def test_create_default(self) -> None:
        '''
            Verifies factory returns IScaraDslService when creating with defaults.
        '''
        mock_frame_builder = MagicMock()
        mock_frame_parser = MagicMock()
        mock_payload_unpacker = MagicMock()
        service = ScaraDslServiceFactory.create_default(
            frame_builder=mock_frame_builder,
            frame_parser=mock_frame_parser,
            payload_unpacker=mock_payload_unpacker,
        )
        self.assertIsInstance(service, IScaraDslService)

    def test_get_version(self) -> None:
        '''
            Verifies factory version returns valid string.
        '''
        self.assertEqual(ScaraDslServiceFactory.get_version(), '1.0.1')


if __name__ == '__main__':
    main()
