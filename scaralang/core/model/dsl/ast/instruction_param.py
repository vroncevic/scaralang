# -*- coding: UTF-8 -*-

'''
Module
    instruction_param.py
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
    Defines InstructionParam enumeration representing standardized AST parameter keys.
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
class InstructionParam(StrEnum):
    '''
        Enumeration of standardized parameter keys used in ScaraInstruction parameter dictionaries.

        It defines:

            :attributes:
                | X - Target Cartesian X coordinate.
                | Y - Target Cartesian Y coordinate.
                | Z - Target Cartesian vertical Z coordinate.
                | PHI - Wrist heading orientation angle in degrees.
                | RZ - Rotation angle around Z axis.
                | I - Arc center X offset.
                | J - Arc center Y offset.
                | R - Corner rounding or arc radius.
                | RADIUS - Corner rounding or arc radius alias.
                | SPEED - Motion feedrate speed.
                | ACCEL - Path acceleration.
                | MODE - Operation mode setting (speed, zone, or tool orientation).
                | MOTOR_MODE - Stepper motor actuation drive mode setting.
                | INTERFACE - Actuator communication interface setting.
                | AXIS_MASK - Bitmask of target joints or axes.
                | ELBOW - Arm kinematic elbow configuration.
                | STATE - Actuator or end-effector binary position/state.
                | MS - Time duration in milliseconds.
                | PERCENT - Override percentage value.
                | AXIS - Cartesian jog axis identifier.
                | STEP - Distance or step increment.
                | JOINT - Robotic joint index.
                | DEG - Joint rotation angle in degrees.
                | ROWS - Pallet matrix row count.
                | COLS - Pallet matrix column count.
                | ROW_PITCH - Distance between pallet rows.
                | COL_PITCH - Distance between pallet columns.
                | NAME - Named identifier reference.
                | INDEX - Linear item index in pallet.
                | ROW - Zero-based pallet row index.
                | COL - Zero-based pallet column index.
                | APPROACH_Z - Relative vertical approach height.
                | RETRACT_Z - Relative vertical retract height.
                | CLEARANCE - Safe transit clearance height.
                | ARCH_HEIGHT - Parabolic arch travel height.
                | TIMEOUT - Maximum wait duration before timeout.
    '''

    X = 'X'
    Y = 'Y'
    Z = 'Z'
    PHI = 'PHI'
    RZ = 'RZ'
    I = 'I'
    J = 'J'
    R = 'R'
    RADIUS = 'RADIUS'
    SPEED = 'SPEED'
    ACCEL = 'ACCEL'
    MODE = 'MODE'
    MOTOR_MODE = 'MOTOR_MODE'
    INTERFACE = 'INTERFACE'
    AXIS_MASK = 'AXIS_MASK'
    ELBOW = 'ELBOW'
    STATE = 'STATE'
    MS = 'MS'
    PERCENT = 'PERCENT'
    AXIS = 'AXIS'
    STEP = 'STEP'
    JOINT = 'JOINT'
    DEG = 'DEG'
    ROWS = 'ROWS'
    COLS = 'COLS'
    ROW_PITCH = 'ROW_PITCH'
    COL_PITCH = 'COL_PITCH'
    NAME = 'NAME'
    INDEX = 'INDEX'
    ROW = 'ROW'
    COL = 'COL'
    APPROACH_Z = 'APPROACH_Z'
    RETRACT_Z = 'RETRACT_Z'
    CLEARANCE = 'CLEARANCE'
    ARCH_HEIGHT = 'ARCH_HEIGHT'
    ARCH = 'ARCH'
    TIMEOUT = 'TIMEOUT'
    DIST = 'DIST'
    ANGLE = 'ANGLE'
    DX = 'DX'
    DY = 'DY'
    START_X = 'START_X'
    START_Y = 'START_Y'
    Z_UP = 'Z_UP'
    Z_DOWN = 'Z_DOWN'
