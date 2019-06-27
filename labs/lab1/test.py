#!/usr/bin/env python3

import os
import lab
import unittest

TEST_DIRECTORY = os.path.dirname(__file__)


class TestImage(unittest.TestCase):
    def test_load(self):
        result = lab.Image.load('test_images/centered_pixel.png')
        expected = lab.Image(11, 11,
                             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                              0, 0, 0, 0, 0, 255, 0, 0, 0, 0, 0,
                              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        self.assertEqual(result, expected)


class TestInverted(unittest.TestCase):
    def test_inverted_1(self):
        im = lab.Image.load('test_images/centered_pixel.png')
        result = im.inverted()
        expected = lab.Image(11, 11,
                             [255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
                              255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
                              255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
                              255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
                              255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
                              255, 255, 255, 255, 255, 0, 255, 255, 255, 255, 255,
                              255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
                              255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
                              255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
                              255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
                              255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255])
        self.assertEqual(result,  expected)

    def test_inverted_2(self):
        im = lab.Image(4, 1, [24, 93, 140, 197])
        result = im.inverted()
        expected = lab.Image(4, 1, [231, 162, 115, 58])
        self.assertEqual(result, expected)

    def test_inverted_images(self):
        for fname in ('mushroom', 'twocats', 'chess'):
            with self.subTest(f=fname):
                inpfile = os.path.join(TEST_DIRECTORY, 'test_images', '%s.png' % fname)
                expfile = os.path.join(TEST_DIRECTORY, 'test_results', '%s_invert.png' % fname)
                result = lab.Image.load(inpfile).inverted()
                expected = lab.Image.load(expfile)
                self.assertEqual(result,  expected)


class TestPixels(unittest.TestCase):
    def test_get_unbounded_pixel(self):
        im = lab.Image(3, 3, [21, 57, 167, 215, 32, 209, 2, 98, 182])
        data = (((-2, -1), 21), ((1, -2), 57), ((4, -3), 167),
                ((-1, 1), 215), ((1, 1), 32), ((5, 1), 209),
                ((-3, 3), 2), ((1, 4), 98), ((5, 3), 182))
        for coordinates, value in data:
            with self.subTest(c=coordinates):
                x, y = coordinates
                result = im.get_unbounded_pixel(x, y)
                self.assertEqual(result, value)


class TestCorrelation(unittest.TestCase):
    def test_correlate(self):
        identity = ((0, 0, 0),
                    (0, 1, 0),
                    (0, 0, 0))
        translation = ((0, 0, 0, 0, 0),
                       (0, 0, 0, 0, 0),
                       (1, 0, 0, 0, 0),
                       (0, 0, 0, 0, 0),
                       (0, 0, 0, 0, 0))
        average = ((0.0, 0.2, 0.0),
                   (0.2, 0.2, 0.2),
                   (0.0, 0.2, 0.0))
        kernels = {"identity": identity, "translation": translation, "average": average}
        img = lab.Image.load("test_images/centered_pixel.png")
        img_copy = lab.Image(img.width, img.height, img.pixels)
        for kernel_name in ("identity", "translation", "average"):
            with self.subTest(k=kernel_name):
                expfile = os.path.join(TEST_DIRECTORY, "test_results", f"{kernel_name}_pixel.png")
                result = img.correlate(kernels[kernel_name])
                expected = lab.Image.load(expfile)
                self.assertEqual(img, img_copy, "Be careful not to modify theo original image!")
                self.assertEqual(result, expected)


class TestFilters(unittest.TestCase):
    def test_blurred(self):
        for kernsize in (1, 3, 7):
            for fname in ('mushroom', 'twocats', 'chess'):
                with self.subTest(k=kernsize, f=fname):
                    inpfile = os.path.join(TEST_DIRECTORY, 'test_images', '%s.png' % fname)
                    expfile = os.path.join(TEST_DIRECTORY, 'test_results', '%s_blur_%02d.png' % (fname, kernsize))
                    input_img = lab.Image.load(inpfile)
                    input_img_copy = lab.Image(input_img.width, input_img.height, input_img.pixels)
                    result = input_img.blurred(kernsize)
                    expected = lab.Image.load(expfile)
                    self.assertEqual(input_img, input_img_copy, "Be careful not to modify the original image!")
                    self.assertEqual(result,  expected)

    def test_sharpened(self):
        for kernsize in (1, 3, 9):
            for fname in ('mushroom', 'twocats', 'chess'):
                with self.subTest(k=kernsize, f=fname):
                    inpfile = os.path.join(TEST_DIRECTORY, 'test_images', '%s.png' % fname)
                    expfile = os.path.join(TEST_DIRECTORY, 'test_results', '%s_sharp_%02d.png' % (fname, kernsize))
                    input_img = lab.Image.load(inpfile)
                    input_img_copy = lab.Image(input_img.width, input_img.height, input_img.pixels)
                    result = input_img.sharpened(kernsize)
                    expected = lab.Image.load(expfile)
                    self.assertEqual(input_img, input_img_copy, "Be careful not to modify the original image!")
                    self.assertEqual(result,  expected)

    def test_edges(self):
        for fname in ('mushroom', 'twocats', 'chess'):
            with self.subTest(f=fname):
                inpfile = os.path.join(TEST_DIRECTORY, 'test_images', '%s.png' % fname)
                expfile = os.path.join(TEST_DIRECTORY, 'test_results', '%s_edges.png' % fname)
                input_img = lab.Image.load(inpfile)
                input_img_copy = lab.Image(input_img.width, input_img.height, input_img.pixels)
                result = input_img.edges()
                expected = lab.Image.load(expfile)
                self.assertEqual(input_img, input_img_copy, "Be careful not to modify the original image!")
                self.assertEqual(result,  expected)


if __name__ == '__main__':
    res = unittest.main(verbosity=3, exit=False)
