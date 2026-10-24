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

from unittest import TestCase, main

from scaralang.core.model.dsl.macro.frame import WorkFrame
from scaralang.core.model.kinematics.pose.point_3d import Point3D
from scaralang.core.service.transformation.itransformer import ITransformer
from scaralang.core.service.transformation.transformer import FrameTransformer

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.1'
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
        self.assertEqual(self.transformer.get_version(), '1.1.1')

    def test_identity_transformation(self) -> None:
        '''
            Tests that a frame at origin with 0 rotation preserves point coordinates exactly.
        '''
        frame = WorkFrame(origin=Point3D(x=0.0, y=0.0, z=0.0), angle_deg=0.0)
        p = Point3D(x=10.0, y=20.0, z=5.0)
        res = self.transformer.transform_point(frame=frame, point=p)
        self.assertEqual(res, p)
        inv = self.transformer.inverse_transform_point(frame=frame, point=p)
        self.assertEqual(inv, p)

    def test_pure_translation(self) -> None:
        '''
            Tests offset application without rotation.
        '''
        frame = WorkFrame(origin=Point3D(x=50.0, y=100.0, z=15.0), angle_deg=0.0)
        p = Point3D(x=10.0, y=20.0, z=5.0)
        res = self.transformer.transform_point(frame=frame, point=p)
        self.assertAlmostEqual(res.x, 60.0)
        self.assertAlmostEqual(res.y, 120.0)
        self.assertAlmostEqual(res.z, 20.0)
        inv = self.transformer.inverse_transform_point(frame=frame, point=res)
        self.assertAlmostEqual(inv.x, 10.0)
        self.assertAlmostEqual(inv.y, 20.0)
        self.assertAlmostEqual(inv.z, 5.0)

    def test_pure_rotation_90_deg(self) -> None:
        '''
            Tests 90 degree counter-clockwise rotation around origin.
        '''
        frame = WorkFrame(origin=Point3D(x=0.0, y=0.0, z=0.0), angle_deg=90.0)
        p = Point3D(x=10.0, y=0.0, z=7.5)
        res = self.transformer.transform_point(frame=frame, point=p)
        self.assertAlmostEqual(res.x, 0.0)
        self.assertAlmostEqual(res.y, 10.0)
        self.assertAlmostEqual(res.z, 7.5)
        inv = self.transformer.inverse_transform_point(frame=frame, point=res)
        self.assertAlmostEqual(inv.x, 10.0)
        self.assertAlmostEqual(inv.y, 0.0)
        self.assertAlmostEqual(inv.z, 7.5)

    def test_combined_transformation(self) -> None:
        '''
            Tests combined translation and 90 degree rotation.
        '''
        frame = WorkFrame(origin=Point3D(x=100.0, y=100.0, z=25.0), angle_deg=90.0)
        p = Point3D(x=10.0, y=0.0, z=12.0)
        res = self.transformer.transform_point(frame=frame, point=p)
        self.assertAlmostEqual(res.x, 100.0)
        self.assertAlmostEqual(res.y, 110.0)
        self.assertAlmostEqual(res.z, 37.0)
        inv = self.transformer.inverse_transform_point(frame=frame, point=res)
        self.assertAlmostEqual(inv.x, 10.0)
        self.assertAlmostEqual(inv.y, 0.0)
        self.assertAlmostEqual(inv.z, 12.0)

    def test_bidirectional_roundtrip(self) -> None:
        '''
            Tests bidirectional consistency across arbitrary frame angle and origin.
        '''
        frame = WorkFrame(origin=Point3D(x=35.5, y=-22.8, z=14.2), angle_deg=37.5)
        local_point = Point3D(x=12.4, y=48.2, z=-8.6)
        global_point = self.transformer.transform_point(frame=frame, point=local_point)
        recovered_local = self.transformer.inverse_transform_point(
            frame=frame, point=global_point
        )
        self.assertAlmostEqual(recovered_local.x, local_point.x, places=5)
        self.assertAlmostEqual(recovered_local.y, local_point.y, places=5)
        self.assertAlmostEqual(recovered_local.z, local_point.z, places=5)


if __name__ == '__main__':
    main()
