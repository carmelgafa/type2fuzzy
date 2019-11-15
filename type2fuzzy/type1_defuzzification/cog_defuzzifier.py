from type2fuzzy.membership.type1fuzzyset import Type1FuzzySet

def cog_defuzzify(type1_set):
	'''
	Centre of gravity defuzzification method

	References:
	-----------
	Pedrycz, Witold. Fuzzy control and fuzzy systems (2nd. Research Studies Press Ltd., 1993.

	Arguments:
	----------
	type1_set   -- Type1FuzzySet, the set whose centroid is to be computed

	Returns:
	--------
	centroid    -- float, the centroid of this set

	Raises:
	-------
	Exception if the denominator of the calculation is zero

	'''
	numerator = 0
	denominator = 0

	for domain_element in type1_set.domain_elements():
		numerator = numerator + (domain_element * type1_set[domain_element])
		denominator = denominator + type1_set[domain_element]

	centroid = 0
	if denominator == 0:
		raise Exception('Cannot determine centroid')
	else:
		centroid = numerator / denominator

	return centroid
