import unittest
from type2fuzzy.membership.type1fuzzyvariable import Type1FuzzyVariable


class TestType1FuzzyVariable(unittest.TestCase):

	def test_init(self):
		var = Type1FuzzyVariable(0, 100 , 100)

		self.assertEqual(var._min_val, 0)
		self.assertEqual(var._max_val, 100)
		self.assertEqual(var._res, 100)

	def test_name_property(self):
		var = Type1FuzzyVariable(0, 100 , 100, 'test')
		self.assertEqual('test', var.name)
