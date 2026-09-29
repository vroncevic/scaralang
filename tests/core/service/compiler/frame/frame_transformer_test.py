# -*- coding: UTF-8 -*-

'''
Module
    frame_transformer_test.py
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
    Unit testing for FrameTransformer service and factory.
'''

from __future__ import annotations

from unittest import TestCase, main

from scaralang.core.model.dsl.macro.work_frame import WorkFrame
from scaralang.core.service.compiler.frame.frame_transformer import FrameTransformer
from scaralang.core.service.compiler.frame.frame_transformer_factory import FrameTransformerFactory
from scaralang.core.service.compiler.frame.iframe_transformer import IFrameTransformer

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class FrameTransformerTest(TestCase):
    '''
        Validates FrameTransformer transformations, protocol compliance, and factory creation.
    '''

    def setUp(self) -> None:
        '''
            Sets up test fixture with transformer instance.
        '''
        self.transformer: IFrameTransformer = FrameTransformerFactory.create()

    def test_factory_and_protocol(self) -> None:
        '''
            Verifies that factory returns an instance satisfying IFrameTransformer protocol.
        '''
        self.assertIsInstance(self.transformer, IFrameTransformer)
        self.assertIsInstance(self.transformer, FrameTransformer)
        self.assertEqual(FrameTransformerFactory.get_version(), '1.0.0')

    def test_identity_transformation(self) -> None:
        '''
            Verifies that origin frame transforms local coordinates without changes.
        '''
        frame = WorkFrame(x=0.0, y=0.0, angle_deg=0.0)
        gx, gy = self.transformer.transform_point(frame=frame, x=25.0, y=75.0)
        self.assertAlmostEqual(gx, 25.0)
        self.assertAlmostEqual(gy, 75.0)

    def test_translation_transformation(self) -> None:
        '''
            Verifies pure linear coordinate translation.
        '''
        frame = WorkFrame(x=50.0, y=100.0, angle_deg=0.0)
        gx, gy = self.transformer.transform_point(frame=frame, x=10.0, y=20.0)
        self.assertAlmostEqual(gx, 60.0)
        self.assertAlmostEqual(gy, 120.0)

    def test_rotation_transformation(self) -> None:
        '''
            Verifies coordinate rotation around origin.
        '''
        frame = WorkFrame(x=0.0, y=0.0, angle_deg=90.0)
        gx, gy = self.transformer.transform_point(frame=frame, x=10.0, y=0.0)
        self.assertAlmostEqual(gx, 0.0)
        self.assertAlmostEqual(gy, 10.0)

    def test_combined_transformation(self) -> None:
        '''
            Verifies translation plus rotation transformation.
        '''
        frame = WorkFrame(x=100.0, y=100.0, angle_deg=90.0)
        gx, gy = self.transformer.transform_point(frame=frame, x=10.0, y=20.0)
        # x' = 100 + (10 * 0 - 20 * 1) = 80
        # y' = 100 + (10 * 1 + 20 * 0) = 110
        self.assertAlmostEqual(gx, 80.0)
        self.assertAlmostEqual(gy, 110.0)


if __name__ == '__main__':
    main()
