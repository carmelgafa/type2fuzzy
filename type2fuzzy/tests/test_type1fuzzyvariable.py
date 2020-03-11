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

	def test_get_set(self):

		var = Type1FuzzyVariable(0,100,100)

		new_set = var.add_triangular('test_set', 0,50,100)
		ret_set = var.get_set('test_set')

		# check is carried out on string representation 
		# of the sets - should be enough
		self.assertEqual(str(new_set), str(ret_set))