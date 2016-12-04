import unittest
import unittest.mock
from fractals.mandelbrot import Mandelbrot

class MandelbrotTest(unittest.TestCase):
    def setUp(self):
        self.mandelbrot = Mandelbrot()

    def test_escape(self):
        self.assertEqual(self.mandelbrot
                         .calculate_point(complex(1.9, 1.9), 50),
                         0)

    def test_iterations(self):
        iterations = 50
        self.assertEqual(self.mandelbrot
                         .calculate_point(complex(0, 0), iterations),
                         iterations)

    def test_coordinates(self):
        iterations = 50

        with unittest.mock.patch.object(Mandelbrot, 'calculate_point',
                                        return_value = 0) as mock_calculate:
            self.mandelbrot = Mandelbrot(x_steps = 2, y_steps = 2)
            self.mandelbrot.calculate(iterations)

        calls = [unittest.mock.call(complex( 1,  1), iterations),
                 unittest.mock.call(complex( 1, -1), iterations),
                 unittest.mock.call(complex(-1,  1), iterations),
                 unittest.mock.call(complex(-1, -1), iterations)]
        mock_calculate.assert_has_calls(calls, any_order = True)
