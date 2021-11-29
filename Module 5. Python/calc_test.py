import unittest
import calculator

Calculator = calculator.Calculator()


class calctest(unittest.TestCase):
    def test_add(self):
        a,b = 1,2
        result = Calculator.add(a,b)

        self.assertEqual(result,3)

    def test_subtract(self):
        a,b = 5,1
        result = Calculator.subtract(a,b)

        self.assertEqual(result,4)

    def test_multiply(self):
        a,b = 2,2
        result = Calculator.multiply(a,b)

        self.assertEqual(result,4)

    def test_divide(self):
        a,b = 10,2
        result = Calculator.divide(a,b)

        self.assertEqual(result,5)

if __name__ == '__main__':
    unittest.main()