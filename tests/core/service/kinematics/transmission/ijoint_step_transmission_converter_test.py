# -*- coding: UTF-8 -*-

'''
Module
    ijoint_step_transmission_converter_test.py
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
    Unit tests for IJointStepTransmissionConverter protocol definition.
'''

from __future__ import annotations

from typing import Protocol
from unittest import TestCase
from unittest import main

from scaralang.core.service.kinematics.transmission.ijoint_step_transmission_converter import IJointStepTransmissionConverter

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestIJointStepTransmissionConverter(TestCase):
    '''
        Test cases verifying IJointStepTransmissionConverter structural protocol contract.

        It defines:

            :methods:
                | test_protocol_definition - Verifies protocol methods and runtime checkability.
    '''

    def test_protocol_definition(self) -> None:
        '''
            Verifies that IJointStepTransmissionConverter defines required methods.
        '''
        self.assertTrue(issubclass(IJointStepTransmissionConverter, Protocol))
        expected_methods: set[str] = {
            'angles_to_steps',
            'steps_to_angles',
            'steps_per_rad',
            'steps_per_mm_z'
        }
        for method_name in expected_methods:
            self.assertTrue(
                hasattr(IJointStepTransmissionConverter, method_name),
                f'Protocol missing method {method_name}'
            )


if __name__ == '__main__':
    main()
