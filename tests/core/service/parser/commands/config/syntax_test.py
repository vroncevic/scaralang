# -*- coding: UTF-8 -*-

'''
Module
    syntax_test.py
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
    Unit tests for MotorSyntaxExtractor implementation.
'''

from __future__ import annotations

from unittest import TestCase, main

from scaralang.core.model.dsl.token.token import ScaraToken
from scaralang.core.model.dsl.token.token_type import ScaraTokenType
from scaralang.core.model.exceptions.syntax import ScaraSyntaxError
from scaralang.core.service.parser.commands.config.syntax import MotorSyntaxExtractor

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestMotorSyntaxExtractor(TestCase):
    '''
        Test cases verifying MotorSyntaxExtractor behavior.

        It defines:

            :methods:
                | test_extract_config_motor_three_tokens - Verifies CONFIG MOTOR mode extraction.
                | test_extract_config_motor_four_tokens - Verifies CONFIG MOTOR mode and interface.
                | test_extract_config_insufficient_tokens - Verifies ScaraSyntaxError on short tokens.
                | test_extract_config_unknown_subproperty - Verifies error on unknown subproperty.
                | test_extract_config_motor_prefix_two_tokens - Verifies CONFIG_MOTOR mode extraction.
                | test_extract_config_motor_prefix_three_tokens - Verifies CONFIG_MOTOR with interface.
                | test_extract_motor_mode_prefix - Verifies MOTOR_MODE prefix extraction.
                | test_extract_motor_mode_insufficient_tokens - Verifies error on short MOTOR_MODE.
                | test_extract_unexpected_command - Verifies error on unrecognized command.
    '''

    def test_extract_config_motor_three_tokens(self) -> None:
        '''
            Verifies CONFIG MOTOR mode extraction without interface.
        '''
        tokens = (
            ScaraToken(
                token_type=ScaraTokenType.IDENTIFIER, value='CONFIG', line=1, column=1
            ),
            ScaraToken(
                token_type=ScaraTokenType.IDENTIFIER, value='MOTOR', line=1, column=8
            ),
            ScaraToken(
                token_type=ScaraTokenType.IDENTIFIER,
                value='OPEN_LOOP',
                line=1,
                column=14,
            ),
        )
        mode, iface = MotorSyntaxExtractor.extract(tokens=tokens, line_num=1)
        self.assertEqual(mode, 'OPEN_LOOP')
        self.assertEqual(iface, '')

    def test_extract_config_motor_four_tokens(self) -> None:
        '''
            Verifies CONFIG MOTOR mode and interface extraction.
        '''
        tokens = (
            ScaraToken(
                token_type=ScaraTokenType.IDENTIFIER, value='CONFIG', line=1, column=1
            ),
            ScaraToken(
                token_type=ScaraTokenType.IDENTIFIER, value='MOTOR', line=1, column=8
            ),
            ScaraToken(
                token_type=ScaraTokenType.IDENTIFIER,
                value='CLOSED_LOOP',
                line=1,
                column=14,
            ),
            ScaraToken(
                token_type=ScaraTokenType.IDENTIFIER, value='CAN_BUS', line=1, column=26
            ),
        )
        mode, iface = MotorSyntaxExtractor.extract(tokens=tokens, line_num=1)
        self.assertEqual(mode, 'CLOSED_LOOP')
        self.assertEqual(iface, 'CAN_BUS')

    def test_extract_config_insufficient_tokens(self) -> None:
        '''
            Verifies ScaraSyntaxError when CONFIG has fewer than 3 tokens.
        '''
        tokens = (
            ScaraToken(
                token_type=ScaraTokenType.IDENTIFIER,
                value='CONFIG',
                line=1,
                column=1,
            ),
            ScaraToken(
                token_type=ScaraTokenType.IDENTIFIER,
                value='MOTOR',
                line=1,
                column=8,
            ),
        )
        with self.assertRaises(ScaraSyntaxError):
            MotorSyntaxExtractor.extract(tokens=tokens, line_num=1)

    def test_extract_config_unknown_subproperty(self) -> None:
        '''
            Verifies ScaraSyntaxError when CONFIG property is not MOTOR.
        '''
        tokens = (
            ScaraToken(
                token_type=ScaraTokenType.IDENTIFIER,
                value='CONFIG',
                line=1,
                column=1,
            ),
            ScaraToken(
                token_type=ScaraTokenType.IDENTIFIER,
                value='UNKNOWN',
                line=1,
                column=8,
            ),
            ScaraToken(
                token_type=ScaraTokenType.IDENTIFIER,
                value='OPEN_LOOP',
                line=1,
                column=16,
            ),
        )
        with self.assertRaises(ScaraSyntaxError):
            MotorSyntaxExtractor.extract(tokens=tokens, line_num=1)

    def test_extract_config_motor_prefix_two_tokens(self) -> None:
        '''
            Verifies CONFIG_MOTOR mode extraction without interface.
        '''
        tokens = (
            ScaraToken(
                token_type=ScaraTokenType.IDENTIFIER,
                value='CONFIG_MOTOR',
                line=1,
                column=1,
            ),
            ScaraToken(
                token_type=ScaraTokenType.IDENTIFIER,
                value='OPEN_LOOP',
                line=1,
                column=14,
            ),
        )
        mode, iface = MotorSyntaxExtractor.extract(tokens=tokens, line_num=1)
        self.assertEqual(mode, 'OPEN_LOOP')
        self.assertEqual(iface, '')

    def test_extract_config_motor_prefix_three_tokens(self) -> None:
        '''
            Verifies CONFIG_MOTOR mode and interface extraction.
        '''
        tokens = (
            ScaraToken(
                token_type=ScaraTokenType.IDENTIFIER,
                value='CONFIG_MOTOR',
                line=1,
                column=1,
            ),
            ScaraToken(
                token_type=ScaraTokenType.IDENTIFIER,
                value='CLOSED_LOOP',
                line=1,
                column=14,
            ),
            ScaraToken(
                token_type=ScaraTokenType.IDENTIFIER,
                value='STEP_DIR',
                line=1,
                column=26,
            ),
        )
        mode, iface = MotorSyntaxExtractor.extract(tokens=tokens, line_num=1)
        self.assertEqual(mode, 'CLOSED_LOOP')
        self.assertEqual(iface, 'STEP_DIR')

    def test_extract_motor_mode_prefix(self) -> None:
        '''
            Verifies MOTOR_MODE mode extraction without interface.
        '''
        tokens = (
            ScaraToken(
                token_type=ScaraTokenType.IDENTIFIER,
                value='MOTOR_MODE',
                line=1,
                column=1,
            ),
            ScaraToken(
                token_type=ScaraTokenType.IDENTIFIER,
                value='OPEN_LOOP',
                line=1,
                column=12,
            ),
        )
        mode, iface = MotorSyntaxExtractor.extract(tokens=tokens, line_num=1)
        self.assertEqual(mode, 'OPEN_LOOP')
        self.assertEqual(iface, '')

    def test_extract_motor_mode_insufficient_tokens(self) -> None:
        '''
            Verifies ScaraSyntaxError when MOTOR_MODE has fewer than 2 tokens.
        '''
        tokens = (
            ScaraToken(
                token_type=ScaraTokenType.IDENTIFIER,
                value='MOTOR_MODE',
                line=1,
                column=1,
            ),
        )
        with self.assertRaises(ScaraSyntaxError):
            MotorSyntaxExtractor.extract(tokens=tokens, line_num=1)

    def test_extract_unexpected_command(self) -> None:
        '''
            Verifies ScaraSyntaxError on unrecognized command.
        '''
        tokens = (
            ScaraToken(
                token_type=ScaraTokenType.IDENTIFIER,
                value='UNKNOWN',
                line=1,
                column=1,
            ),
        )
        with self.assertRaises(ScaraSyntaxError):
            MotorSyntaxExtractor.extract(tokens=tokens, line_num=1)

    def test_get_version(self) -> None:
        '''
            Verifies that get_version returns valid version string.
        '''
        version = MotorSyntaxExtractor.get_version()
        self.assertIsInstance(version, str)
        self.assertTrue(len(version) > 0)


if __name__ == '__main__':
    main()
