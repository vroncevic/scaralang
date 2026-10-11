# -*- coding: UTF-8 -*-

'''
Module
    factory.py
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
    Factory instantiating and wiring motion command parser components.
'''

from __future__ import annotations

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
__version__ = '1.0.8'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class MotionFactory:
    '''
        Factory providing configured MotionProvides subsystem instances.

        It defines:

            :methods:
                | create - Constructs and wires MotionProvides container.
                | get_version - Returns factory version string.
    '''

    @classmethod
    def create(cls) -> MotionProvides:
        '''
            Constructs and wires MotionProvides container with command parsers.

            :return: Fully configured MotionProvides container.
            :exceptions: None.
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
        return MotionProvides(
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

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns the factory version string.

            :return: Factory version string.
            :exceptions: None.
        '''
        return __version__
