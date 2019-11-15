import unittest
from type2fuzzy.membership.type1fuzzyset import Type1FuzzySet


class TestType1FuzzySet(unittest.TestCase):

	def test_from_representation(self):

		set_representation = '''0.100/1.000 + 0.200/2.000
				+ 0.300/3.000 + 0.400/4.000'''
		t1fs = Type1FuzzySet.from_representation(set_representation)

		self.assertEqual(t1fs[1], 0.1)
		self.assertEqual(t1fs[2], 0.2)
		self.assertEqual(t1fs[3], 0.3)
		self.assertEqual(t1fs[4], 0.4)

	def test_to_representation(self):

		set_representation = '0.100/1.000 + 0.200/2.000 + 0.300/3.000 + 0.400/4.000'

		t1fs = Type1FuzzySet.from_representation(set_representation)

		rep_result = t1fs.__str__()

		self.assertEqual(rep_result, set_representation)


	def test_domain_limits(self):

		set_representation = '''0.100/1.000 + 0.200/2.000
				+ 0.300/3.000 + 0.400/4.000'''
		t1fs = Type1FuzzySet.from_representation(set_representation)

		domain_limits = t1fs.domain_limits()

		self.assertEqual(domain_limits.left, 1.0)
		self.assertEqual(domain_limits.right, 4.0)