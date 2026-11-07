
import unittest

from network_explorer.performance import (
    transmission_delay,
    propagation_delay,
    nodal_delay,
)


class PerformanceTests(unittest.TestCase):

    def test_nodal_delay(self):
        result = nodal_delay(0.001, 0.002, 0.003, 0.004)
        self.assertAlmostEqual(result, 0.01)

    def test_nodal_delay_zeros(self):
        result = nodal_delay(0, 0, 0, 0)
        self.assertEqual(result, 0.0)

    def test_nodal_delay_negative(self):
        for index in range(4):
            values = [0.001, 0.002, 0.003, 0.004]
            values[index] = -0.001

            with self.subTest(component=index):
                with self.assertRaises(ValueError):
                    nodal_delay(*values)

    def test_transmission_delay(self):
        result = transmission_delay(8000, 1000000)
        self.assertAlmostEqual(result, 0.008)

    def test_transmission_invalid(self):
        with self.assertRaises(ValueError):
            transmission_delay(-100, 1000000)

        with self.assertRaises(ValueError):
            transmission_delay(8000, 0)

    def test_propagation_delay(self):
        result = propagation_delay(200000)
        self.assertAlmostEqual(result, 0.001)

    def test_propagation_invalid(self):
        with self.assertRaises(ValueError):
            propagation_delay(-100)

        with self.assertRaises(ValueError):
            propagation_delay(100, 0)


if __name__ == "__main__":
    unittest.main()
