import unittest
import os
import numpy as np
from type2fuzzy.membership.generaltype2fuzzyset import GeneralType2FuzzySet
from type2fuzzy.membership.intervaltype2fuzzyset import IntervalType2FuzzySet
from type2fuzzy.membership.secondarymf import SecondaryMembershipFunction
from type2fuzzy.membership.crispset import CrispSet

class TestIntervalType2FuzzySet(unittest.TestCase):

	def test_from_general_type2_set(self):

		gt2fs = GeneralType2FuzzySet.from_representation('''(0.90 / 0.00 + 0.50 / 0.20 + 0.20 / 0.40 + 0.35 / 0.61 + 0.10 / 0.80) / 1.00 
												+ (0.50 / 0.00 + 0.35 / 0.20 + 0.35 / 0.40 + 0.20 / 0.60 + 0.50 / 0.80) / 2.00 
												+ (0.35 / 0.60 + 0.35 / 0.80) / 3.00 
												+ (0.10 / 0.00 + 0.35 / 0.20 + 0.50 / 0.40 + 0.10 / 0.60 + 0.35 / 0.80 + 0.25 / 1.00) / 4.00 
												+ (0.35 / 0.00 + 0.50 / 0.20 + 0.10 / 0.40 + 0.20 / 0.60 + 0.20 / 0.80) / 5.00''')

		it2fs = IntervalType2FuzzySet.from_general_type2_set(gt2fs)

		self.assertEqual(it2fs[1.00].left, 0.00)
		self.assertEqual(it2fs[1.00].right, 0.80)

		self.assertEqual(it2fs[2.00].left, 0.00)
		self.assertEqual(it2fs[2.00].right, 0.80)

		self.assertEqual(it2fs[3.00].left, 0.60)
		self.assertEqual(it2fs[3.00].right, 0.80)

		self.assertEqual(it2fs[4.00].left, 0.00)
		self.assertEqual(it2fs[4.00].right, 1.00)

		self.assertEqual(it2fs[5.00].left, 0.00)
		self.assertEqual(it2fs[5.00].right, 0.80)
