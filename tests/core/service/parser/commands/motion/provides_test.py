# -*- coding: UTF-8 -*-

'''
Module
    provides_test.py
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
    Unit tests for MotionProvides container.
'''

from __future__ import annotations

from dataclasses import FrozenInstanceError
from unittest import TestCase, main

from scaralang.core.service.parser.commands.icommand_parser import ICommandParser
from scaralang.core.service.parser.commands.motion.approach import ApproachParser
from scaralang.core.service.parser.commands.motion.arc import ArcParser
from scaralang.core.service.parser.commands.motion.home import HomeParser
from scaralang.core.service.parser.commands.motion.jog_axis import JogAxisParser
from scaralang.core.service.parser.commands.motion.jog_joint import JogJointParser
from scaralang.core.service.parser.commands.motion.joint import JointParser
from scaralang.core.service.parser.commands.motion.linear import LinearParser
from scaralang.core.service.parser.commands.motion.probe import ProbeParser
from scaralang.core.service.parser.commands.motion.provides import MotionProvides
from scaralang.core.service.parser.commands.motion.retract import RetractParser

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.9'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestMotionProvides(TestCase):
    '''
        Test cases verifying MotionProvides container properties and immutability.

        It defines:

            :methods:
                | test_provides_encapsulation - Verifies attributes and protocol types.
                | test_immutability - Verifies frozen container raises FrozenInstanceError.
    '''

    def test_provides_encapsulation(self) -> None:
        '''
            Verifies attributes and protocol conformance of provided parsers.
        '''
        approach_parser = ApproachParser()
        arc_parser = ArcParser()
        home_parser = HomeParser()
        jog_axis_parser = JogAxisParser()
        jog_joint_parser = JogJointParser()
        joint_parser = JointParser()
        linear_parser = LinearParser()
        probe_parser = ProbeParser()
        retract_parser = RetractParser()
        provides = MotionProvides(
            approach_parser=approach_parser,
            arc_parser=arc_parser,
            home_parser=home_parser,
            jog_axis_parser=jog_axis_parser,
            jog_joint_parser=jog_joint_parser,
            joint_parser=joint_parser,
            linear_parser=linear_parser,
            probe_parser=probe_parser,
            retract_parser=retract_parser,
            parsers=(
                linear_parser,
                joint_parser,
                home_parser,
                arc_parser,
                approach_parser,
                retract_parser,
                jog_axis_parser,
                jog_joint_parser,
                probe_parser,
            ),
        )
        self.assertIs(provides.approach_parser, approach_parser)
        self.assertIs(provides.arc_parser, arc_parser)
        self.assertIs(provides.home_parser, home_parser)
        self.assertIs(provides.jog_axis_parser, jog_axis_parser)
        self.assertIs(provides.jog_joint_parser, jog_joint_parser)
        self.assertIs(provides.joint_parser, joint_parser)
        self.assertIs(provides.linear_parser, linear_parser)
        self.assertIs(provides.probe_parser, probe_parser)
        self.assertIs(provides.retract_parser, retract_parser)
        self.assertEqual(len(provides.parsers), 9)
        for parser in provides.parsers:
            self.assertIsInstance(parser, ICommandParser)

    def test_immutability(self) -> None:
        '''
            Verifies container immutability on attribute reassignment.
        '''
        approach_parser = ApproachParser()
        arc_parser = ArcParser()
        home_parser = HomeParser()
        jog_axis_parser = JogAxisParser()
        jog_joint_parser = JogJointParser()
        joint_parser = JointParser()
        linear_parser = LinearParser()
        probe_parser = ProbeParser()
        retract_parser = RetractParser()
        provides = MotionProvides(
            approach_parser=approach_parser,
            arc_parser=arc_parser,
            home_parser=home_parser,
            jog_axis_parser=jog_axis_parser,
            jog_joint_parser=jog_joint_parser,
            joint_parser=joint_parser,
            linear_parser=linear_parser,
            probe_parser=probe_parser,
            retract_parser=retract_parser,
            parsers=(
                linear_parser,
                joint_parser,
                home_parser,
                arc_parser,
                approach_parser,
                retract_parser,
                jog_axis_parser,
                jog_joint_parser,
                probe_parser,
            ),
        )
        with self.assertRaises(FrozenInstanceError):
            setattr(provides, 'approach_parser', approach_parser)


if __name__ == '__main__':
    main()
