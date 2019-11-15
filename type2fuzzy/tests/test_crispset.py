import unittest
import os
import numpy as np
from type2fuzzy.membership.generaltype2fuzzyset import GeneralType2FuzzySet
from type2fuzzy.membership.secondarymf import SecondaryMembershipFunction
from type2fuzzy.membership.crispset import CrispSet

class TestCrispSet(unittest.TestCase):

	def test_crisp_set(self):
		with self.assertRaises(Exception) : CrispSet(6, 5)

		# assert empty set
		crisp_set = CrispSet()
		self.assertTrue(crisp_set._empty)

		# create a set
		crisp_set = CrispSet(5, 6)
		self.assertFalse(crisp_set.empty)
		self.assertEqual(crisp_set.left, 5)
		self.assertEqual(crisp_set.right, 6)

		# set an invalid left value
		with self.assertRaises(Exception) : crisp_set.left = 7

		# change left value
		crisp_set.left = 3
		self.assertEqual(crisp_set .left, 3)

		crisp_set.right = 7
		self.assertEqual(crisp_set.right, 7)

		# mid value test
		self.assertEqual(crisp_set.mid, 5)

		crisp_set.left = None
		with self.assertRaises(Exception) : crisp_set.mid

		crisp_set.right = None
		self.assertTrue(crisp_set.empty)
