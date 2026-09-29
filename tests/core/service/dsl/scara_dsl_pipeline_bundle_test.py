# -*- coding: UTF-8 -*-

'''
Module
    scara_dsl_pipeline_bundle_test.py
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
    Unit tests for ScaraDslPipelineBundle class.
'''

from __future__ import annotations

from dataclasses import FrozenInstanceError
from unittest import TestCase
from unittest import main
from unittest.mock import MagicMock

from scaralang.core.model.kinematics.transmission_parameters import TransmissionParameters
from scaralang.core.service.dsl.scara_dsl_pipeline_bundle import ScaraDslPipelineBundle

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestScaraDslPipelineBundle(TestCase):
    '''
        Test cases verifying ScaraDslPipelineBundle dataclass.

        It defines:

            :methods:
                | test_pipeline_bundle_attributes - Verifies bundle correctly stores injected attributes.
                | test_pipeline_bundle_immutability - Verifies bundle is frozen against attribute mutation.
    '''

    def test_pipeline_bundle_attributes(self) -> None:
        '''
            Verifies bundle stores all injected pipeline references.
        '''
        mock_frame_builder = MagicMock()
        mock_frame_parser = MagicMock()
        mock_payload_unpacker = MagicMock()
        mock_kinematics = MagicMock()
        mock_validator = MagicMock()
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

        self.assertIs(bundle.frame_builder, mock_frame_builder)
        self.assertIs(bundle.frame_parser, mock_frame_parser)
        self.assertIs(bundle.payload_unpacker, mock_payload_unpacker)
        self.assertIs(bundle.kinematics, mock_kinematics)
        self.assertIs(bundle.validator, mock_validator)
        self.assertEqual(bundle.transmission, transmission)

    def test_pipeline_bundle_immutability(self) -> None:
        '''
            Verifies bundle fields cannot be modified after instantiation.
        '''
        transmission = TransmissionParameters(
            gear_ratio_j1=5.0,
            gear_ratio_j2=5.0,
            leadscrew_pitch_z=4.0,
            gear_ratio_j4=1.0,
            microstepping=16.0,
            steps_per_rev=200.0,
        )
        bundle = ScaraDslPipelineBundle(
            frame_builder=MagicMock(),
            frame_parser=MagicMock(),
            payload_unpacker=MagicMock(),
            kinematics=MagicMock(),
            validator=MagicMock(),
            transmission=transmission,
        )
        with self.assertRaises(FrozenInstanceError):
            bundle.frame_builder = MagicMock()  # type: ignore[misc]


if __name__ == '__main__':
    main()
