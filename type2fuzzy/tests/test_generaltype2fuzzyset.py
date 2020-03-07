import unittest
import os
import numpy as np
from type2fuzzy.membership.generaltype2fuzzyset import GeneralType2FuzzySet
from type2fuzzy.membership.secondarymf import SecondaryMembershipFunction
from type2fuzzy.membership.crispset import CrispSet

class TestGeneralType2FuzzySet(unittest.TestCase):

	def test_load_representation(self):

		# should raise an exception with an empty or None representation
		with self.assertRaises(Exception) : GeneralType2FuzzySet.from_representation(None)
		with self.assertRaises(Exception) : GeneralType2FuzzySet.from_representation('')

		gt2fs = GeneralType2FuzzySet.from_representation('''(0.90 / 0.00 + 0.50 / 0.20 + 0.20 / 0.40 + 0.35 / 0.61 + 0.10 / 0.80) / 1.00 
														+ (0.50 / 0.00 + 0.35 / 0.20 + 0.35 / 0.40 + 0.20 / 0.60 + 0.50 / 0.80) / 2.00 
														+ (0.35 / 0.60 + 0.35 / 0.80) / 3.00 
														+ (0.10 / 0.00 + 0.35 / 0.20 + 0.50 / 0.40 + 0.10 / 0.60 + 0.35 / 0.80 + 0.25 / 1.00) / 4.00 
														+ (0.35 / 0.00 + 0.50 / 0.20 + 0.10 / 0.40 + 0.20 / 0.60 + 0.20 / 0.80) / 5.00''')

		# check correct set creation
		self.assertDictEqual(gt2fs[1.00].elements(), {0.00:0.90, 0.20:0.50, 0.40:0.20, 0.61:0.35, 0.80:0.10})
		self.assertDictEqual(gt2fs[2.00].elements(), {0.00:0.50, 0.20:0.35, 0.40:0.35, 0.60:0.20, 0.80:0.50})
		self.assertDictEqual(gt2fs[3.00].elements(), {0.60:0.35, 0.80:0.35})
		self.assertDictEqual(gt2fs[4.00].elements(), {0.00:0.10, 0.20:0.35, 0.40:0.50, 0.60:0.10, 0.80:0.35, 1.00:0.25})
		self.assertDictEqual(gt2fs[5.00].elements(), {0.00:0.35, 0.20:0.50, 0.40:0.10, 0.60:0.20, 0.80:0.20})

		# chech exception with invalid represenation
		invalid_set_representation = '''(0.90  0.00 + 0.50 / 0.20 + 0.20 / 0.40 + 0.35 / 0.61 + 0.10 / 0.80) / 1.00 
										+ (0.50 / 0.00 + 0.35 / 0.20 + 0.35 / 0.40 + 0.20 / 0.60 + 0.50 / 0.80) / 2.00 
										+ (0.35 / 0.60 + 0.35 / 0.80) / 3.00 
										+ (0.10 / 0.00 + 0.35 / 0.20 + 0.50 / 0.40 + 0.10 / 0.60 + 0.35 / 0.80 s 0.25 / 1.00) / 4.00 
										+ (0.35 / 0.00 + 0.50 / 0.20 + 0.10 / 0.40 + 0.20 / 0.60 + 0.20 / 0.80) / 5.00'''

		with self.assertRaises(Exception) : GeneralType2FuzzySet.from_representation(invalid_set_representation)

	def test_load_file(self):

		__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

		with self.assertRaises(Exception) : GeneralType2FuzzySet.from_representation(None)
		with self.assertRaises(Exception) : GeneralType2FuzzySet.from_representation(os.path.join(__location__, ''))
		with self.assertRaises(Exception) : GeneralType2FuzzySet.from_representation(os.path.join(__location__,'abc.txt'))
		with self.assertRaises(Exception) : GeneralType2FuzzySet.from_representation(os.path.join(__location__,'test_set_empty.txt'))

		gt2fs = GeneralType2FuzzySet.load_file(os.path.join(__location__,'test_set.txt'))
		# check correct set creation
		self.assertDictEqual(gt2fs[1.00].elements(), {0.00:0.90, 0.20:0.50, 0.40:0.20, 0.61:0.35, 0.80:0.10})
		self.assertDictEqual(gt2fs[2.00].elements(), {0.00:0.50, 0.20:0.35, 0.40:0.35, 0.60:0.20, 0.80:0.50})
		self.assertDictEqual(gt2fs[3.00].elements(), {0.60:0.35, 0.80:0.35})
		self.assertDictEqual(gt2fs[4.00].elements(), {0.00:0.10, 0.20:0.35, 0.40:0.50, 0.60:0.10, 0.80:0.35, 1.00:0.25})
		self.assertDictEqual(gt2fs[5.00].elements(), {0.00:0.35, 0.20:0.50, 0.40:0.10, 0.60:0.20, 0.80:0.20})

	def test_load_array(self):
		
		#test that it works
		primary_domain = [1, 2, 3]
		secondary_domain = [0, 0.5, 0.9]
		set_array =[[0.9, 0.0, 0.0],
					[0.5, 1.0, 0.0],
					[0.3, 0.6, 1.0]]
		
		gt2fs = GeneralType2FuzzySet.from_array(primary_domain, secondary_domain, set_array)

		self.assertDictEqual(gt2fs[1.00].elements(), {0.00:0.90, 0.50:0.50, 0.90:0.30})
		self.assertDictEqual(gt2fs[2.00].elements(), {0.00:0.00, 0.50:1.00, 0.90:0.6})
		self.assertDictEqual(gt2fs[3.00].elements(), {0.00:0.00, 0.50:0.00, 0.90:1.00})

		#mismatch tests
		primary_domain = [1, 2, 3, 4]
		with self.assertRaises(Exception) : GeneralType2FuzzySet.from_array(set_array, primary_domain, secondary_domain)

		primary_domain = [1, 2, 3]
		secondary_domain = [0.5, 0.9]
		with self.assertRaises(Exception) : GeneralType2FuzzySet.from_array(set_array, primary_domain, secondary_domain)

		primary_domain = [1, 2, 3]
		secondary_domain = [0, 0.5, 0.9]
		set_array =[[0.9, 0.0, 0.0],
					[0.5, 1.0],
					[0.3, 0.6, 1.0]]
		with self.assertRaises(Exception) : GeneralType2FuzzySet.from_array(set_array, primary_domain, secondary_domain)

	def test_to_representation(self):

		# this is tested before
		primary_domain = [1, 2, 3]
		secondary_domain = [0, 0.5, 0.9]
		set_array =[[0.9, 0.0, 0.0],
					[0.5, 1.0, 0.0],
					[0.3, 0.6, 1.0]]
		
		gt2fs = GeneralType2FuzzySet.from_array(primary_domain, secondary_domain, set_array)

		str_set = gt2fs.__str__()
		expected_set = '(0.9000 / 0.0000 + 0.5000 / 0.5000 + 0.3000 / 0.9000) / 1.0000 + (0.0000 / 0.0000 + 1.0000 / 0.5000 + 0.6000 / 0.9000) / 2.0000 + (0.0000 / 0.0000 + 0.0000 / 0.5000 + 1.0000 / 0.9000) / 3.0000'

		self.assertEqual(str_set, expected_set)

	def test_to_file(self):

		set_representation = '(0.9000 / 0.0000 + 0.5000 / 0.5000 + 0.3000 / 0.9000) / 1.0000 + (1.0000 / 0.5000 + 0.6000 / 0.9000) / 2.0000 + (1.0000 / 0.9000) / 3.0000'
		gt2fs = GeneralType2FuzzySet.from_representation(set_representation)

		filename = os.path.join(os.path.dirname(__file__), 'save_file_test.txt')
		gt2fs.save_file(filename, num_dec_places=2)

		with open(filename, 'r') as fuzzy_file:
			set_read = fuzzy_file.read()

		self.assertEqual(set_read, set_representation)

		with self.assertRaises(Exception) : gt2fs.save_file('')
		with self.assertRaises(Exception) : gt2fs.save_file(None)

	def test_to_array_explicit(self):
		gt2fs = GeneralType2FuzzySet.from_representation('''(0.90/0.00 + 0.50/0.20 + 0.20/0.40 + 0.35/0.60 + 0.10/0.80              )/1.00 
														+   (0.50/0.00 + 0.35/0.20 + 0.35/0.40 + 0.20/0.60 + 0.50/0.80              )/2.00 
														+   (                                    0.35/0.60 + 0.35/0.80              )/3.00 
														+   (0.10/0.00 + 0.35/0.20 + 0.50/0.40 + 0.10/0.60 + 0.35/0.80 + 0.25/1.00  )/4.00 
														+   (0.35/0.00 + 0.50/0.20 + 0.10/0.40 + 0.20/0.60 + 0.20/0.80              )/5.00''')

		primary_domain, secondary_domain, set_array = gt2fs.to_array_explicit()

		self.assertListEqual(primary_domain, [1.00, 2.00, 3.00, 4.00, 5.00])
		self.assertListEqual(secondary_domain, [0.00, 0.20, 0.40, 0.60, 0.80, 1.00])
		
		expected_set_array = np.array([ [0.90, 0.50, 0.00, 0.10, 0.35],
										[0.50, 0.35, 0.00, 0.35, 0.50],
										[0.20, 0.35, 0.00, 0.50, 0.10],
										[0.35, 0.20, 0.35, 0.10, 0.20],
										[0.10, 0.50, 0.35, 0.35, 0.20],
										[0.00, 0.00, 0.00, 0.25, 0.00] ])

		np.testing.assert_array_equal(expected_set_array, set_array)

	def test_to_array_implicit(self):
		gt2fs = GeneralType2FuzzySet.from_representation('''(0.90 / 0.00 + 0.50 / 0.20 + 0.20 / 0.40 + 0.35 / 0.60 + 0.10 / 0.80              ) / 0.80 
														+   (0.50 / 0.00 + 0.35 / 0.20 + 0.35 / 0.40 + 0.20 / 0.60 + 0.50 / 0.80              ) / 2.20 
														+   (                                          0.35 / 0.60 + 0.35 / 0.80              ) / 3.40 
														+   (0.10 / 0.00 + 0.35 / 0.20 + 0.50 / 0.40 + 0.10 / 0.60 + 0.35 / 0.80 + 0.25 / 1.00) / 3.90
														+   (0.35 / 0.00 + 0.50 / 0.20 + 0.10 / 0.40 + 0.20 / 0.60 + 0.20 / 0.80              ) / 4.70''')

		primary_domain = [1.00, 2.00, 3.00, 4.00, 5.00]
		secondary_domain = [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]

		set_array = gt2fs.to_array_implicit(primary_domain, secondary_domain)

		expected_set_array = np.array([ [0.90, 0.50, 0.00, 0.10, 0.35],
										[0.50, 0.35, 0.00, 0.35, 0.50],
										[0.20, 0.35, 0.00, 0.50, 0.10],
										[0.35, 0.20, 0.35, 0.10, 0.20],
										[0.10, 0.50, 0.35, 0.35, 0.20],
										[0.00, 0.00, 0.00, 0.25, 0.00] ])

		np.testing.assert_array_equal(expected_set_array, set_array)

	def test_primary_domain(self):
		gt2fs = GeneralType2FuzzySet.from_representation('''(0.90 / 0.00 + 0.50 / 0.20 + 0.20 / 0.40 + 0.35 / 0.60 + 0.10 / 0.80              ) / 1.00 
														+   (0.50 / 0.00 + 0.35 / 0.20 + 0.35 / 0.40 + 0.20 / 0.60 + 0.50 / 0.80              ) / 2.00 
														+   (                                          0.35 / 0.60 + 0.35 / 0.80              ) / 3.00 
														+   (0.10 / 0.00 + 0.35 / 0.20 + 0.50 / 0.40 + 0.10 / 0.60 + 0.35 / 0.80 + 0.25 / 1.00) / 4.00 
														+   (0.35 / 0.00 + 0.50 / 0.20 + 0.10 / 0.40 + 0.20 / 0.60 + 0.20 / 0.80              ) / 5.00''')

		primary_domain = gt2fs.primary_domain()

		expected_primary_domain =  [1.00, 2.00, 3.00, 4.00, 5.00]

		self.assertListEqual(primary_domain, expected_primary_domain)

	def test_add_element(self):
		gt2fs = GeneralType2FuzzySet()

		# test add new smf
		gt2fs.add_element(6.00, 0.5, 0.3)
		self.assertDictEqual(gt2fs[6.00].elements(), {0.5:0.3})

		# test add to existing smf
		gt2fs.add_element(6.00, 0.6, 0.4)
		self.assertDictEqual(gt2fs[6.00].elements(), {0.5:0.3, 0.6:0.4})

		# assert that 0 secondary grade is not added
		gt2fs.add_element(6.00, 0.7, 0)
		self.assertDictEqual(gt2fs[6.00].elements(), {0.5:0.3, 0.6:0.4, 0.7:0.0})

		# test for exceptions
		with self.assertRaises(Exception) : gt2fs.add_element(0.4, 0.2, -0.1)
		with self.assertRaises(Exception) : gt2fs.add_element(0.4, 0.2, 1.1)
		with self.assertRaises(Exception) : gt2fs.add_element(0.4, -0.1, 0.2)
		with self.assertRaises(Exception) : gt2fs.add_element(0.4, 1.1, 0.2)

	def test_add_membership_function(self):
		gt2fs = GeneralType2FuzzySet.from_representation('''(0.90 / 0.00 + 0.50 / 0.20 + 0.20 / 0.40 + 0.35 / 0.60 + 0.10 / 0.80              ) / 1.00 
														+   (0.50 / 0.00 + 0.35 / 0.20 + 0.35 / 0.40 + 0.20 / 0.60 + 0.50 / 0.80              ) / 2.00 
														+   (                                          0.35 / 0.60 + 0.35 / 0.80              ) / 3.00 
														+   (0.35 / 0.00 + 0.50 / 0.20 + 0.10 / 0.40 + 0.20 / 0.60 + 0.20 / 0.80              ) / 5.00''')

		smf = SecondaryMembershipFunction.from_representation('0.10 / 0.00 + 0.35 / 0.20 + 0.50 / 0.40 + 0.10 / 0.60 + 0.35 / 0.80 + 0.25 / 1.00')
		
		gt2fs.add_membership_function(4.00, smf)

		# check correct set creation
		self.assertDictEqual(gt2fs[1.00].elements(), {0.00:0.90, 0.20:0.50, 0.40:0.20, 0.60:0.35, 0.80:0.10})
		self.assertDictEqual(gt2fs[2.00].elements(), {0.00:0.50, 0.20:0.35, 0.40:0.35, 0.60:0.20, 0.80:0.50})
		self.assertDictEqual(gt2fs[3.00].elements(), {0.60:0.35, 0.80:0.35})
		self.assertDictEqual(gt2fs[4.00].elements(), {0.00:0.10, 0.20:0.35, 0.40:0.50, 0.60:0.10, 0.80:0.35, 1.00:0.25})
		self.assertDictEqual(gt2fs[5.00].elements(), {0.00:0.35, 0.20:0.50, 0.40:0.10, 0.60:0.20, 0.80:0.20})

	def test_footprint_of_uncertainty(self):
		gt2fs = GeneralType2FuzzySet.from_representation('''(0.90 / 0.00 + 0.50 / 0.20 + 0.60 / 0.40 + 0.35 / 0.60 + 0.10 / 0.80              ) / 1.00 
														+   (0.50 / 0.00 + 0.35 / 0.20 + 0.35 / 0.40 + 0.20 / 0.60 + 0.50 / 0.80              ) / 2.00 
														+   (                                          0.35 / 0.60 + 0.35 / 0.80              ) / 3.00 
														+   (0.10 / 0.00 + 0.35 / 0.20 + 0.50 / 0.40 + 0.10 / 0.60 + 0.35 / 0.80 + 0.25 / 1.00) / 4.00 
														+   (0.35 / 0.00 + 0.50 / 0.20 + 0.10 / 0.40 + 0.20 / 0.60 + 0.20 / 0.80              ) / 5.00''')
		
		expected_fou = {1.00:(0.00, 0.80),
						2.00:(0.00, 0.80),
						3.00:(0.60,0.80),
						4.00:(0.00, 1.00),
						5.00:(0.00, 0.80)}

		fou = gt2fs.footprint_of_uncertainty()

		for primary_domain_element in expected_fou:
			self.assertEqual(fou[primary_domain_element].left, expected_fou[primary_domain_element][0])
			self.assertEqual(fou[primary_domain_element].right, expected_fou[primary_domain_element][1])

	def test__getitem__(self):

		gt2fs = GeneralType2FuzzySet.from_representation('''(0.90 / 0.00 + 0.50 / 0.20 + 0.20 / 0.40 + 0.35 / 0.60 + 0.10 / 0.80              ) / 1.00 
														+   (0.50 / 0.00 + 0.35 / 0.20 + 0.35 / 0.40 + 0.20 / 0.60 + 0.50 / 0.80              ) / 2.00 
														+   (                                          0.35 / 0.60 + 0.35 / 0.80              ) / 3.00 
														+   (0.10 / 0.00 + 0.35 / 0.20 + 0.50 / 0.40 + 0.10 / 0.60 + 0.35 / 0.80 + 0.25 / 1.00) / 4.00 
														+   (0.35 / 0.00 + 0.50 / 0.20 + 0.10 / 0.40 + 0.20 / 0.60 + 0.20 / 0.80              ) / 5.00''')

		self.assertDictEqual(gt2fs[1.00].elements(), {0.00:0.90, 0.20:0.50, 0.40:0.20, 0.60:0.35, 0.80:0.10})
		self.assertDictEqual(gt2fs[2.00].elements(), {0.00:0.50, 0.20:0.35, 0.40:0.35, 0.60:0.20, 0.80:0.50})
		self.assertDictEqual(gt2fs[3.00].elements(), {0.60:0.35, 0.80:0.35})
		self.assertDictEqual(gt2fs[4.00].elements(), {0.00:0.10, 0.20:0.35, 0.40:0.50, 0.60:0.10, 0.80:0.35, 1.00:0.25})
		self.assertDictEqual(gt2fs[5.00].elements(), {0.00:0.35, 0.20:0.50, 0.40:0.10, 0.60:0.20, 0.80:0.20})

		with self.assertRaises(Exception) : gt2fs[6.00]

	def test_vertical_slice(self):

		gt2fs = GeneralType2FuzzySet.from_representation('''(0.90 / 0.00 + 0.50 / 0.20 + 0.20 / 0.40 + 0.35 / 0.60 + 0.10 / 0.80              ) / 1.00 
														+   (0.50 / 0.00 + 0.35 / 0.20 + 0.35 / 0.40 + 0.20 / 0.60 + 0.50 / 0.80              ) / 2.00 
														+   (                                          0.35 / 0.60 + 0.35 / 0.80              ) / 3.00 
														+   (0.10 / 0.00 + 0.35 / 0.20 + 0.50 / 0.40 + 0.10 / 0.60 + 0.35 / 0.80 + 0.25 / 1.00) / 4.00 
														+   (0.35 / 0.00 + 0.50 / 0.20 + 0.10 / 0.40 + 0.20 / 0.60 + 0.20 / 0.80              ) / 5.00''')

		self.assertDictEqual(gt2fs.vertical_slice(1)._elements, {0.00:0.90, 0.20:0.50, 0.40:0.20, 0.60:0.35, 0.80:0.10})
		self.assertDictEqual(gt2fs.vertical_slice(2)._elements, {0.00:0.50, 0.20:0.35, 0.40:0.35, 0.60:0.20, 0.80:0.50})
		self.assertDictEqual(gt2fs.vertical_slice(3)._elements, {0.60:0.35, 0.80:0.35})
		self.assertDictEqual(gt2fs.vertical_slice(4)._elements, {0.00:0.10, 0.20:0.35, 0.40:0.50, 0.60:0.10, 0.80:0.35, 1.00:0.25})
		self.assertDictEqual(gt2fs.vertical_slice(5)._elements, {0.00:0.35, 0.20:0.50, 0.40:0.10, 0.60:0.20, 0.80:0.20})

		with self.assertRaises(Exception) : gt2fs.vertical_slice(6.00)

	def test_primary_membership(self):

		gt2fs = GeneralType2FuzzySet.from_representation('''(0.90 / 0.00 + 0.50 / 0.20 + 0.20 / 0.40 + 0.35 / 0.60 + 0.10 / 0.80              ) / 1.00 
														+   (0.50 / 0.00 + 0.35 / 0.20 + 0.35 / 0.40 + 0.20 / 0.60 + 0.50 / 0.80              ) / 2.00 
														+   (                                          0.35 / 0.60 + 0.35 / 0.80              ) / 3.00 
														+   (0.10 / 0.00 + 0.35 / 0.20 + 0.50 / 0.40 + 0.10 / 0.60 + 0.35 / 0.80 + 0.25 / 1.00) / 4.00 
														+   (0.35 / 0.00 + 0.50 / 0.20 + 0.10 / 0.40 + 0.20 / 0.60 + 0.20 / 0.80              ) / 5.00''')

		self.assertListEqual(gt2fs.primary_membership(1), [0.00, 0.20, 0.40, 0.60, 0.80])
		self.assertListEqual(gt2fs.primary_membership(2), [0.00, 0.20, 0.40, 0.60, 0.80])
		self.assertListEqual(gt2fs.primary_membership(3), [0.60, 0.80])
		self.assertListEqual(gt2fs.primary_membership(4), [0.00, 0.20, 0.40, 0.60, 0.80, 1.00])
		self.assertListEqual(gt2fs.primary_membership(5), [0.00, 0.20, 0.40, 0.60, 0.80])

		with self.assertRaises(Exception) : gt2fs.primary_membership(6.00)

	def test_secondary_grade(self):
		gt2fs = GeneralType2FuzzySet.from_representation('''(0.90 / 0.00 + 0.50 / 0.20 + 0.20 / 0.40 + 0.35 / 0.60 + 0.10 / 0.80              ) / 1.00 
														+   (0.50 / 0.00 + 0.35 / 0.20 + 0.35 / 0.40 + 0.20 / 0.60 + 0.50 / 0.80              ) / 2.00 
														+   (                                          0.35 / 0.60 + 0.35 / 0.80              ) / 3.00 
														+   (0.10 / 0.00 + 0.35 / 0.20 + 0.50 / 0.40 + 0.10 / 0.60 + 0.35 / 0.80 + 0.25 / 1.00) / 4.00 
														+   (0.35 / 0.00 + 0.50 / 0.20 + 0.10 / 0.40 + 0.20 / 0.60 + 0.20 / 0.80              ) / 5.00''')

		primary_domain = [1.00, 2.00, 3.00, 4.00, 5.00]
		secondary_domain = [0.0, 0.2, 0.4, 0.6, 0.8]
		expected_sec_grade_array = np.array([ [0.90, 0.50, 0.00, 0.10, 0.35],
										[0.50, 0.35, 0.00, 0.35, 0.50],
										[0.20, 0.35, 0.00, 0.50, 0.10],
										[0.35, 0.20, 0.35, 0.10, 0.20],
										[0.10, 0.50, 0.35, 0.35, 0.20],
										[0.00, 0.00, 0.00, 0.25, 0.00] ])

		for primary_domain_val_idx in range(len(primary_domain)):
			for secondary_domain_val_idx in range(len(secondary_domain)):
				
				expected_sec_grade = expected_sec_grade_array[secondary_domain_val_idx][primary_domain_val_idx]
				if expected_sec_grade > 0:
					self.assertEqual(gt2fs.secondary_grade( primary_domain[primary_domain_val_idx], 
										secondary_domain[secondary_domain_val_idx]), expected_sec_grade)

	def test_embedded_type2_sets_count(self):
		gt2fs = GeneralType2FuzzySet.from_representation('''(0.90 / 0.00 + 0.50 / 0.20 + 0.20 / 0.40 + 0.35 / 0.60 + 0.10 / 0.80              ) / 1.00 
														+   (0.50 / 0.00 + 0.35 / 0.20 + 0.35 / 0.40 + 0.20 / 0.60 + 0.50 / 0.80              ) / 2.00 
														+   (                                          0.35 / 0.60 + 0.35 / 0.80              ) / 3.00 
														+   (0.10 / 0.00 + 0.35 / 0.20 + 0.50 / 0.40 + 0.10 / 0.60 + 0.35 / 0.80 + 0.25 / 1.00) / 4.00 
														+   (0.35 / 0.00 + 0.50 / 0.20 + 0.10 / 0.40 + 0.20 / 0.60 + 0.20 / 0.80              ) / 5.00''')

		expected_embedded_set_count = 5 * 5 * 2 * 6 * 5

		self.assertEqual(gt2fs.embedded_type2_sets_count(), expected_embedded_set_count)

	def test_embedded_type2_sets(self):
		gt2fs = GeneralType2FuzzySet.from_representation('''(0.90 / 0.00 + 0.50 / 0.20) / 1.00 
														+   (0.35 / 0.40 + 0.20 / 0.60) / 2.00 
														+   (0.15 / 0.80 + 0.25 / 1.00) / 3.00 ''')

		expected_result = [[(0.9, 0, 1), (0.35, 0.4, 2), (0.15, 0.8, 3)],
							[(0.9, 0, 1), (0.35, 0.4, 2), (0.25, 1, 3)], 
							[(0.9, 0, 1), (0.2, 0.6, 2), (0.15, 0.8, 3)],
							[(0.9, 0, 1), (0.2, 0.6, 2), (0.25, 1, 3)],
							[(0.5, 0.2, 1), (0.35, 0.4, 2), (0.15, 0.8, 3)],
							[(0.5, 0.2, 1), (0.35, 0.4, 2), (0.25, 1, 3)], 
							[(0.5, 0.2, 1), (0.2, 0.6, 2), (0.15, 0.8, 3)],
							[(0.5, 0.2, 1), (0.2, 0.6, 2), (0.25, 1, 3)]]

		self.assertListEqual(gt2fs.embedded_type2_sets(), expected_result)

if __name__ == '__main__':
	unittest.main()