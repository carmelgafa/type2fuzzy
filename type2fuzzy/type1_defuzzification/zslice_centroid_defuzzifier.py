
from type2fuzzy.membership.alphacuttype1fuzzyset import AlphaCutType1FuzzySet


def zslice_centroid_defuzzify(zSlice_set):
	
	numerator = 0
	denominator = 0

	for cut in zSlice_set.cuts():
		left = zSlice_set[cut].left
		right = zSlice_set[cut].right

		numerator = numerator + (cut * ((left + right)/2))
		denominator = denominator + cut
	
	centroid = numerator / denominator

	return centroid