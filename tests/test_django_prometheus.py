#!/usr/bin/env python
from django_prometheus.utils import PowersOf, LabelGauge, CallbackLabelGauge
import unittest


class DjangoPrometheusTest(unittest.TestCase):
    def testPowersOf(self):
        """Tests utils.PowersOf."""
        self.assertEqual(
            [0, 1, 2, 4, 8],
            PowersOf(2, 4))
        self.assertEqual(
            [0, 3, 9, 27, 81, 243],
            PowersOf(3, 5, lower=1))
        self.assertEqual(
            [1, 2, 4, 8],
            PowersOf(2, 4, include_zero=False))
        self.assertEqual(
            [4, 8, 16, 32, 64, 128],
            PowersOf(2, 6, lower=2, include_zero=False))


class LabelGaugeTest(unittest.TestCase):
    def testSetGet(self):
        lg = LabelGauge('test', 'test LabelGauge', ['x', 'y'])
        samples = [
            (u'', {'x': 'a', 'y': 'a'}, 1.0),
            (u'', {'x': 'a', 'y': 'b'}, 2.0),
        ]
        lg.set_samples(samples)
        self.assertEqual(samples, lg.get_samples())
        samples2 = [
            (u'', {'x': 'b', 'y': 'a'}, 3.0),
            (u'', {'x': 'a', 'y': 'b'}, 4.0),
        ]
        lg.set_samples(samples2)
        self.assertEqual(samples2, lg.get_samples())


class CallbackLabelGaugeTest(unittest.TestCase):
    def testCallback(self):
        samples = [
            (u'', {'x': 'a', 'y': 'a'}, 1.0),
            (u'', {'x': 'a', 'y': 'b'}, 2.0),
        ]

        clg = CallbackLabelGauge('test', 'test CallbackLabelGauge',
                                 ['x', 'y'], lambda: samples)
        self.assertEqual(samples, clg.get_samples())


if __name__ == 'main':
    unittest.main()
