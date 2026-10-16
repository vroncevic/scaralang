# -*- coding: UTF-8 -*-

'''
Module
    extractor.py
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
    Utility service extracting key-value and positional parameters from DSL token slices.
'''

from __future__ import annotations

from collections.abc import Sequence
from typing import ClassVar

from scaralang.core.model.dsl.token.scara_token import ScaraToken
from scaralang.core.model.dsl.token.scara_token_type import ScaraTokenType

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.9'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ParameterExtractor:
    '''
        Helper utility extracting key-value pairs and typed numerical literals from tokens.

        It defines:

            :attributes:
                | _FLAG_DEFAULT_VALUE - Default boolean value assigned to flag parameters.
                | _FLOAT_INDICATORS - String characters indicating floating point notation.
                | _INITIAL_INDEX - Starting token sequence index.
                | _OFFSET_EQUALS - Lookahead offset for equals token.
                | _OFFSET_VALUE - Lookahead offset for parameter value token.
                | _STEP_FLAG - Token index step for standalone flag parameters.
                | _STEP_KEY_EQUALS_VAL - Token index step for key equals value assignments.
                | _STEP_KEY_VAL - Token index step for key value assignments.
                | _VALUE_TOKEN_TYPES - Supported token types representing parameter values.
            :methods:
                | extract_key_values - Parses key=value pairs and positional parameters into dict.
                | parse_token_value - Converts token string literal to typed float, int, or str.
    '''

    _FLAG_DEFAULT_VALUE: ClassVar[bool] = True
    _FLOAT_INDICATORS: ClassVar[tuple[str, ...]] = ('.', 'e', 'E')
    _INITIAL_INDEX: ClassVar[int] = 0
    _OFFSET_EQUALS: ClassVar[int] = 1
    _OFFSET_VALUE: ClassVar[int] = 2
    _STEP_FLAG: ClassVar[int] = 1
    _STEP_KEY_EQUALS_VAL: ClassVar[int] = 3
    _STEP_KEY_VAL: ClassVar[int] = 2
    _VALUE_TOKEN_TYPES: ClassVar[frozenset[ScaraTokenType]] = frozenset({
        ScaraTokenType.NUMBER,
        ScaraTokenType.STRING,
        ScaraTokenType.IDENTIFIER,
    })

    @classmethod
    def extract_key_values(
        cls,
        *,
        tokens: Sequence[ScaraToken],
    ) -> dict[str, object]:
        '''
            Extracts key-value pairs (e.g. X=150.0 Y=80.0) from a sequence of tokens.

            :param tokens: ScaraToken slice following command keyword.
            :return: Dictionary of parsed parameter names and typed values.
        '''
        params: dict[str, object] = {}
        idx: int = cls._INITIAL_INDEX
        n: int = len(tokens)

        while idx < n:
            tok: ScaraToken = tokens[idx]

            if (
                idx + cls._OFFSET_VALUE < n
                and tokens[idx + cls._OFFSET_EQUALS].token_type == ScaraTokenType.EQUALS
            ):
                key: str = tok.value.upper()
                val_tok: ScaraToken = tokens[idx + cls._OFFSET_VALUE]
                params[key] = cls.parse_token_value(token=val_tok)
                idx += cls._STEP_KEY_EQUALS_VAL
            else:
                key = tok.value.upper()
                next_idx: int = idx + cls._OFFSET_EQUALS

                if (
                    next_idx < n
                    and tokens[next_idx].token_type in cls._VALUE_TOKEN_TYPES
                ):
                    params[key] = cls.parse_token_value(token=tokens[next_idx])
                    idx += cls._STEP_KEY_VAL
                else:
                    params[key] = cls._FLAG_DEFAULT_VALUE
                    idx += cls._STEP_FLAG

        return params

    @classmethod
    def parse_token_value(cls, *, token: ScaraToken) -> float | int | str:
        '''
            Converts token string literal to float, int or string.

            :param token: ScaraToken instance.
            :return: Float, int, or string literal.
        '''
        if token.token_type == ScaraTokenType.NUMBER:
            if any(indicator in token.value for indicator in cls._FLOAT_INDICATORS):
                return float(token.value)

            return int(token.value)

        return token.value
