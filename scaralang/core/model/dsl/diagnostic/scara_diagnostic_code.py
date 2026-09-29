# -*- coding: UTF-8 -*-

'''
Module
    scara_diagnostic_code.py
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
    Defines ScaraDiagnosticCode enumeration representing diagnostic rule codes.
'''

from __future__ import annotations

from enum import StrEnum, unique

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@unique
class ScaraDiagnosticCode(StrEnum):
    '''
        Enumeration of all diagnostic finding codes produced by SCARA static analysis.

        It defines:

            :attributes:
                | EMPTY_PROGRAM - DSL program has no executable instructions.
                | UNCALIBRATED_MOTION - Motion occurs before homing or calibration.
                | DUPLICATE_MOTION - Consecutive motion to identical target coordinates.
                | TOOL_IN_FLYBY - Actuator toggled during blending flyby motion.
                | REDUNDANT_TOOL_CMD - Actuator set to its current existing state.
                | PNEUMATIC_CONFLICT - Pump and valve actuated simultaneously.
                | INVALID_ZONE_MODE - Unrecognized corner rounding mode.
                | INVALID_ZONE_RADIUS - Non-positive corner rounding radius.
                | DEAD_WAIT - Redundant or zero-duration dwell delay.
                | INVALID_MOTOR_MODE - Unrecognized motor drive mode.
                | REDUNDANT_MOTOR_CONFIG - Redundant motor drive mode configuration.
    '''

    EMPTY_PROGRAM = 'EMPTY_PROGRAM'
    UNCALIBRATED_MOTION = 'UNCALIBRATED_MOTION'
    DUPLICATE_MOTION = 'DUPLICATE_MOTION'
    TOOL_IN_FLYBY = 'TOOL_IN_FLYBY'
    REDUNDANT_TOOL_CMD = 'REDUNDANT_TOOL_CMD'
    PNEUMATIC_CONFLICT = 'PNEUMATIC_CONFLICT'
    INVALID_ZONE_MODE = 'INVALID_ZONE_MODE'
    INVALID_ZONE_RADIUS = 'INVALID_ZONE_RADIUS'
    DEAD_WAIT = 'DEAD_WAIT'
    INVALID_MOTOR_MODE = 'INVALID_MOTOR_MODE'
    REDUNDANT_MOTOR_CONFIG = 'REDUNDANT_MOTOR_CONFIG'
