# -*- coding: UTF-8 -*-

'''
Module
    definition_test.py
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
    Unit tests for ZoneDefParser implementation.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main

from scaralang.core.model.dsl.ast.command_type import ScaraCommandType
from scaralang.core.model.dsl.ast.instruction import ScaraInstruction
from scaralang.core.model.dsl.ast.instruction_param import ScaraInstructionParam
from scaralang.core.model.dsl.token.token import ScaraToken
from scaralang.core.model.dsl.token.token_type import ScaraTokenType
from scaralang.core.model.exceptions.syntax import ScaraSyntaxError
from scaralang.core.model.trajectory.obstacle.shape import ObstacleShape
from scaralang.core.service.parser.commands.zone.definition import ZoneDefParser
from scaralang.core.service.parser.commands.zone.validator.box_validator import BoxZoneValidator
from scaralang.core.service.parser.commands.zone.validator.circle_validator import CircleZoneValidator

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestZoneDefParser(TestCase):
    '''
        Test cases verifying ZoneDefParser statement parsing.

        It defines:

            :methods:
                | setUp - Prepares ZoneDefParser instance.
                | test_name_property - Verifies name property.
                | test_can_parse - Verifies can_parse matching.
                | test_parse_valid_box - Verifies parsing valid BOX zone.
                | test_parse_valid_circle - Verifies parsing valid CIRCLE zone.
                | test_parse_incomplete_tokens - Verifies incomplete tokens raise syntax error.
                | test_parse_unknown_shape - Verifies unknown shape raises syntax error.
    '''

    def setUp(self) -> None:
        '''
            Prepares ZoneDefParser test fixture.

            :exceptions: None.
        '''
        self._box_validator = BoxZoneValidator()
        self._circle_validator = CircleZoneValidator()
        self._parser = ZoneDefParser(
            box_validator=self._box_validator,
            circle_validator=self._circle_validator,
        )

    def test_name_property(self) -> None:
        '''
            Verifies parser identification name.

            :exceptions: None.
        '''
        self.assertEqual(self._parser.name, ZoneDefParser.NAME)

    def test_can_parse(self) -> None:
        '''
            Verifies command matching logic.

            :exceptions: None.
        '''
        self.assertTrue(self._parser.can_parse(command_name=ScaraCommandType.ZONE_DEF))
        self.assertFalse(self._parser.can_parse(command_name=ScaraCommandType.MOVE_L))

    def test_parse_valid_box(self) -> None:
        '''
            Verifies successful parsing of rectangular obstacle zone statement.

            :exceptions: None.
        '''
        tokens = (
            ScaraToken(
                token_type=ScaraTokenType.IDENTIFIER,
                value='ZONE_DEF',
                line=1,
                column=1,
            ),
            ScaraToken(
                token_type=ScaraTokenType.IDENTIFIER,
                value='WALL',
                line=1,
                column=10,
            ),
            ScaraToken(
                token_type=ScaraTokenType.IDENTIFIER,
                value='BOX',
                line=1,
                column=15,
            ),
            ScaraToken(
                token_type=ScaraTokenType.IDENTIFIER,
                value='X_MIN',
                line=1,
                column=19,
            ),
            ScaraToken(
                token_type=ScaraTokenType.EQUALS,
                value='=',
                line=1,
                column=24,
            ),
            ScaraToken(
                token_type=ScaraTokenType.NUMBER,
                value='10.0',
                line=1,
                column=25,
            ),
            ScaraToken(
                token_type=ScaraTokenType.IDENTIFIER,
                value='X_MAX',
                line=1,
                column=30,
            ),
            ScaraToken(
                token_type=ScaraTokenType.EQUALS,
                value='=',
                line=1,
                column=35,
            ),
            ScaraToken(
                token_type=ScaraTokenType.NUMBER,
                value='50.0',
                line=1,
                column=36,
            ),
            ScaraToken(
                token_type=ScaraTokenType.IDENTIFIER,
                value='Y_MIN',
                line=1,
                column=41,
            ),
            ScaraToken(
                token_type=ScaraTokenType.EQUALS,
                value='=',
                line=1,
                column=46,
            ),
            ScaraToken(
                token_type=ScaraTokenType.NUMBER,
                value='-20.0',
                line=1,
                column=47,
            ),
            ScaraToken(
                token_type=ScaraTokenType.IDENTIFIER,
                value='Y_MAX',
                line=1,
                column=53,
            ),
            ScaraToken(
                token_type=ScaraTokenType.EQUALS,
                value='=',
                line=1,
                column=58,
            ),
            ScaraToken(
                token_type=ScaraTokenType.NUMBER,
                value='30.0',
                line=1,
                column=59,
            ),
        )
        instruction: ScaraInstruction = self._parser.parse(
            tokens=tokens,
            line_num=1,
            raw_text='ZONE_DEF WALL BOX X_MIN=10.0 X_MAX=50.0 Y_MIN=-20.0 Y_MAX=30.0',
        )
        self.assertEqual(instruction.command_type, ScaraCommandType.ZONE_DEF)
        self.assertEqual(instruction.parameters[ScaraInstructionParam.NAME.value], 'WALL')
        self.assertEqual(
            instruction.parameters[ScaraInstructionParam.SHAPE.value],
            ObstacleShape.BOX.value,
        )

    def test_parse_valid_circle(self) -> None:
        '''
            Verifies successful parsing of circular obstacle zone statement.

            :exceptions: None.
        '''
        tokens = (
            ScaraToken(
                token_type=ScaraTokenType.IDENTIFIER,
                value='ZONE_DEF',
                line=1,
                column=1,
            ),
            ScaraToken(
                token_type=ScaraTokenType.IDENTIFIER,
                value='POST',
                line=1,
                column=10,
            ),
            ScaraToken(
                token_type=ScaraTokenType.IDENTIFIER,
                value='CIRCLE',
                line=1,
                column=15,
            ),
            ScaraToken(
                token_type=ScaraTokenType.IDENTIFIER,
                value='X',
                line=1,
                column=22,
            ),
            ScaraToken(
                token_type=ScaraTokenType.EQUALS,
                value='=',
                line=1,
                column=23,
            ),
            ScaraToken(
                token_type=ScaraTokenType.NUMBER,
                value='120.0',
                line=1,
                column=24,
            ),
            ScaraToken(
                token_type=ScaraTokenType.IDENTIFIER,
                value='Y',
                line=1,
                column=30,
            ),
            ScaraToken(
                token_type=ScaraTokenType.EQUALS,
                value='=',
                line=1,
                column=31,
            ),
            ScaraToken(
                token_type=ScaraTokenType.NUMBER,
                value='40.0',
                line=1,
                column=32,
            ),
            ScaraToken(
                token_type=ScaraTokenType.IDENTIFIER,
                value='RADIUS',
                line=1,
                column=37,
            ),
            ScaraToken(
                token_type=ScaraTokenType.EQUALS,
                value='=',
                line=1,
                column=43,
            ),
            ScaraToken(
                token_type=ScaraTokenType.NUMBER,
                value='25.0',
                line=1,
                column=44,
            ),
        )
        instruction: ScaraInstruction = self._parser.parse(
            tokens=tokens,
            line_num=1,
            raw_text='ZONE_DEF POST CIRCLE X=120.0 Y=40.0 RADIUS=25.0',
        )
        self.assertEqual(instruction.command_type, ScaraCommandType.ZONE_DEF)
        self.assertEqual(instruction.parameters[ScaraInstructionParam.NAME.value], 'POST')
        self.assertEqual(
            instruction.parameters[ScaraInstructionParam.SHAPE.value],
            ObstacleShape.CIRCLE.value,
        )

    def test_parse_incomplete_tokens(self) -> None:
        '''
            Verifies incomplete token sequence raises ScaraSyntaxError.

            :exceptions: None.
        '''
        tokens = (
            ScaraToken(
                token_type=ScaraTokenType.IDENTIFIER,
                value='ZONE_DEF',
                line=1,
                column=1,
            ),
            ScaraToken(
                token_type=ScaraTokenType.IDENTIFIER,
                value='POST',
                line=1,
                column=10,
            ),
        )
        with self.assertRaises(ScaraSyntaxError):
            self._parser.parse(
                tokens=tokens,
                line_num=1,
                raw_text='ZONE_DEF POST',
            )

    def test_parse_unknown_shape(self) -> None:
        '''
            Verifies unknown shape string raises ScaraSyntaxError.

            :exceptions: None.
        '''
        tokens = (
            ScaraToken(
                token_type=ScaraTokenType.IDENTIFIER,
                value='ZONE_DEF',
                line=1,
                column=1,
            ),
            ScaraToken(
                token_type=ScaraTokenType.IDENTIFIER,
                value='POLY',
                line=1,
                column=10,
            ),
            ScaraToken(
                token_type=ScaraTokenType.IDENTIFIER,
                value='TRIANGLE',
                line=1,
                column=15,
            ),
        )
        with self.assertRaises(ScaraSyntaxError):
            self._parser.parse(
                tokens=tokens,
                line_num=1,
                raw_text='ZONE_DEF POLY TRIANGLE',
            )


if __name__ == '__main__':
    main()
