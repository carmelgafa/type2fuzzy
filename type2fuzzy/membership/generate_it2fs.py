'''
generation of interval type 2 fuzzy sets
'''
import math
import numpy as np

from type2fuzzy.membership.intervaltype2fuzzyset import IntervalType2FuzzySet
from type2fuzzy.membership.crispset import CrispSet

def create_gaussian_fixed_sigma(primary_domain, m1, m2, sigma=1.0):
	'''
	Creates an interval type-2 fuzzy set with fixed standard deviation and uncertain mean

	Arguments:
	----------
	primary_domain -- list, elements of primary domain

	m1 -- lowest value of mean

	m2 -- highest value of mean
	
	sigma -- standard deviation , default 1

	Returns:
	--------
	interval_set -- created interval type-2 fuzzy set

	References:
	-----------
	Karnik, Nilesh N., and Jerry M. Mendel. 
	"Introduction to type-2 fuzzy logic systems." 
	1998 IEEE International Conference on Fuzzy Systems Proceedings.
	IEEE World Congress on Computational Intelligence (
	Cat. No. 98CH36228). Vol. 2. IEEE, 1998.
	'''
	# check that m1 is smaller than m2
	if m1 > m2:
		raise Exception('ERROR: m1 vaue must be smaller or equal to m2')
	
	interval_set = IntervalType2FuzzySet()
	toggle_peak = False
	element = None

	for x in primary_domain:

		u1 = math.exp(-0.5*((x-float(m1))/sigma)**2)
		u2 = math.exp(-0.5*((x-float(m2))/sigma)**2)

		# once m1 has a value of 1 the plateu starts and ands when m2 reaches a value of 1
		if u1 == 1:
			toggle_peak = True
		if u2 == 1:
			toggle_peak = False

		if toggle_peak:
			element = CrispSet(min(u1, u2), 1)
		else:
			element = CrispSet(min(u1, u2), max(u1, u2))

		# add the element to the it2fs
		interval_set.add_element(x, element)

	return interval_set

def create_gaussian_fixed_mean(primary_domain, sigma1, sigma2, mean=1.0):
	'''
	Creates an interval type-2 fuzzy set with fixed standard deviation and uncertain mean

	Arguments:
	----------
	primary_domain -- list, elements of primary domain

	sigma1 -- lowest value of standard deviation

	sigma2 -- highest value of standard deviation

	mean -- mean , default 1

	Returns:
	--------
	interval_set -- created interval type-2 fuzzy set

	References:
	-----------
	Karnik, Nilesh N., and Jerry M. Mendel. 
	"Introduction to type-2 fuzzy logic systems." 
	1998 IEEE International Conference on Fuzzy Systems Proceedings.
	IEEE World Congress on Computational Intelligence (
	Cat. No. 98CH36228). Vol. 2. IEEE, 1998.
	'''
	# check that m1 is smaller than m2
	if sigma1 > sigma2:
		raise Exception('ERROR: m1 vaue must be smaller or equal to m2')
	
	interval_set = IntervalType2FuzzySet()
	u1 = 0
	u2 = 0

	for x in primary_domain:

		u1 = math.exp(-0.5*((x-float(mean))/sigma1)**2)
		u2 = math.exp(-0.5*((x-float(mean))/sigma2)**2)

		# add the element to the it2fs
		interval_set.add_element(x, CrispSet(min(u1, u2), max(u1, u2)))

	return interval_set