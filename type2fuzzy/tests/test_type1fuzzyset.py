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


	def test_create_triangular(self):

		primary_domain = list(range(0,11))

		set_1 = Type1FuzzySet.create_triangular(primary_domain, 0,0,5)

		self.assertEqual(set_1[0], 1)
		self.assertEqual(set_1[1], 0.8)
		self.assertEqual(set_1[2], 0.6)
		self.assertEqual(set_1[3], 0.4)
		self.assertEqual(set_1[4], 0.2)
		self.assertEqual(set_1[5], 0)
		self.assertEqual(set_1[6], 0)
		self.assertEqual(set_1[7], 0)
		self.assertEqual(set_1[8], 0)
		self.assertEqual(set_1[9], 0)
		self.assertEqual(set_1[10], 0)
		
	def test_domain_limits(self):

		set_representation = '''0.000/1.000 + 0.200/2.000
				+ 0.300/3.000 + 0.400/4.000'''
		t1fs = Type1FuzzySet.from_representation(set_representation)

		domain_limits = t1fs.domain_limits()

		self.assertEqual(domain_limits.left, 1.0)
		self.assertEqual(domain_limits.right, 4.0)