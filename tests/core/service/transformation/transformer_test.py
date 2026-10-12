# -*- coding: UTF-8 -*-

'''
Module
    transformer_test.py
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
    Unit testing for FrameTransformer service.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main

from scaralang.core.model.dsl.macro.work_frame import WorkFrame
from scaralang.core.model.kinematics.point_2d import Point2D
from scaralang.core.service.transformation.itransformer import ITransformer
from scaralang.core.service.transformation.transformer import FrameTransformer

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.8'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TransformerTest(TestCase):
    '''
        Validates FrameTransformer transformations and protocol compliance.
    '''

    def setUp(self) -> None:
        '''
            Sets up test fixture with transformer instance.
        '''
        self.transformer: FrameTransformer = FrameTransformer()

    def test_protocol_compliance(self) -> None:
        '''
            Verifies that transformer satisfies ITransformer protocol.
        '''
        self.assertIsInstance(self.transformer, ITransformer)

    def test_get_version(self) -> None:
        '''
            Verifies transformer get_version method returns semantic version string.
        '''
        self.assertEqual(self.transformer.get_version(), '1.0.8')

    def test_identity_transformation(self) -> None:
        '''
            Tests that a frame at origin with 0 rotation preserves point coordinates exactly.
        '''
        frame = WorkFrame(origin=Point2D(x=0.0, y=0.0), angle_deg=0.0)
        p = Point2D(x=10.0, y=20.0)
        res = self.transformer.transform_point(frame=frame, point=p)
        self.assertEqual(res, p)

    def test_pure_translation(self) -> None:
        '''
            Tests offset application without rotation.
        '''
        frame = WorkFrame(origin=Point2D(x=50.0, y=100.0), angle_deg=0.0)
        p = Point2D(x=10.0, y=20.0)
        res = self.transformer.transform_point(frame=frame, point=p)
        self.assertAlmostEqual(res.x, 60.0)
        self.assertAlmostEqual(res.y, 120.0)

    def test_pure_rotation_90_deg(self) -> None:
        '''
            Tests 90 degree counter-clockwise rotation around origin.
        '''
        frame = WorkFrame(origin=Point2D(x=0.0, y=0.0), angle_deg=90.0)
        p = Point2D(x=10.0, y=0.0)
        res = self.transformer.transform_point(frame=frame, point=p)
        self.assertAlmostEqual(res.x, 0.0)
        self.assertAlmostEqual(res.y, 10.0)

    def test_combined_transformation(self) -> None:
        '''
            Tests combined translation and 90 degree rotation.
        '''
        frame = WorkFrame(origin=Point2D(x=100.0, y=100.0), angle_deg=90.0)
        p = Point2D(x=10.0, y=0.0)
        res = self.transformer.transform_point(frame=frame, point=p)
        self.assertAlmostEqual(res.x, 100.0)
        self.assertAlmostEqual(res.y, 110.0)


if __name__ == '__main__':
    main()
