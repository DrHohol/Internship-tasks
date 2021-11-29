import unittest
import count_vowels


class CountTest(unittest.TestCase):
	def test_count(self):
		text = "Just a little article for some testy"
		result = count_vowels.get_res(text)

		self.assertEqual(result,12)

if __name__ == '__main__':
	unittest.main()