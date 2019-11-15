import logging
from type2fuzzy.membership.crispset import CrispSet
from type2fuzzy.membership.intervaltype2fuzzyset import IntervalType2FuzzySet


def it2_kernikmendel_reduce(it2fs, precision=5, information='none'):
	reduced_set = None

	if information == 'none':
		reduced_set = _it2_kernikmendel_reduce_noinfo(it2fs, precision)
	elif information == 'full':
		reduced_set = _it2_kernikmendel_reduce_fullinfo(it2fs, precision)
	
	return reduced_set

def _it2_kernikmendel_reduce_noinfo(it2fs, precision=5):

	numerator = 0
	denominator = 0
	error_threshold = 1e-5
	counter = 0
	primary_domain_elements = it2fs.primary_domain()

	centroid = CrispSet(primary_domain_elements[0], primary_domain_elements[len(primary_domain_elements)-1])


	centroid_left = it2fs.mid_domain_element()
	while True:

		centroid.left = centroid_left
		numerator = 0
		denominator = 0

		for domain_element in it2fs.primary_domain():

			if domain_element >= centroid_left:
				numerator = numerator + (domain_element * it2fs[domain_element].left)
				denominator = denominator + it2fs[domain_element].left
			else:
				numerator = numerator + (domain_element * it2fs[domain_element].right)
				denominator = denominator + it2fs[domain_element].right

		if denominator == 0:
			centroid.left = it2fs.mid_domain_element()
			logging.log(logging.ERROR, 'error in calculating z_l, denominator is 0')
			break

		centroid_left = numerator / denominator

		if abs(centroid_left - centroid.left) <= error_threshold:
			break
		
		if counter == 15:
			break

		counter = counter + 1

	counter = 0
	centroid_right = it2fs.mid_domain_element()
	
	while True:

		centroid.right = centroid_right
		numerator = 0
		denominator = 0

		for domain_element in it2fs.primary_domain():

			if domain_element <= centroid_right:
				numerator = numerator + (domain_element * it2fs[domain_element].left)
				denominator = denominator + it2fs[domain_element].left
			else:
				numerator = numerator + (domain_element * it2fs[domain_element].right)
				denominator = denominator + it2fs[domain_element].right

		if denominator == 0:
			centroid_right = it2fs.mid_domain_element()
			logging.log(logging.ERROR, 'error in calculating z_l, denominator is 0')
			break

		centroid_right = numerator / denominator

		if abs(centroid_right - centroid.right) <= error_threshold:
			break
		
		if counter == 15:
			break

		counter = counter + 1

	centroid.left = round(centroid.left, precision)
	centroid.right = round(centroid.right, precision)
	return centroid


def _it2_kernikmendel_reduce_fullinfo(it2fs, precision=5):

	numerator = 0
	denominator = 0
	error_threshold = 1e-5
	counter = 0
	primary_domain_elements = it2fs.primary_domain()

	centroid = CrispSet(primary_domain_elements[0], primary_domain_elements[len(primary_domain_elements)-1])

	logging.log(logging.INFO,'starting recursion...')

	centroid_left = it2fs.mid_domain_element()
	logging.log(logging.DEBUG, f'Initial value of centroid left= {centroid_left}')
	
	while True:

		centroid.left = centroid_left
		numerator = 0
		denominator = 0

		for domain_element in it2fs.primary_domain():

			if domain_element >= centroid_left:
				numerator = numerator + (domain_element * it2fs[domain_element].left)
				denominator = denominator + it2fs[domain_element].left
			else:
				numerator = numerator + (domain_element * it2fs[domain_element].right)
				denominator = denominator + it2fs[domain_element].right

		logging.log(logging.DEBUG, f'numerator: {numerator}, denominator: {denominator}, centroid: {centroid_left}')

		if denominator == 0:
			centroid.left = it2fs.mid_domain_element()
			logging.log(logging.ERROR, 'error in calculating z_l, denominator is 0')
			break

		centroid_left = numerator / denominator

		if abs(centroid_left - centroid.left) <= error_threshold:
			break
		
		if counter == 15:
			logging.log(logging.ERROR, 'cannot converge...')
			break

		counter = counter + 1

	counter = 0
	centroid_right = it2fs.mid_domain_element()
	logging.log(logging.DEBUG,f'Initial value of centroid right= {centroid_right}')
	
	while True:

		centroid.right = centroid_right
		numerator = 0
		denominator = 0

		for domain_element in it2fs.primary_domain():

			if domain_element <= centroid_right:
				numerator = numerator + (domain_element * it2fs[domain_element].left)
				denominator = denominator + it2fs[domain_element].left
			else:
				numerator = numerator + (domain_element * it2fs[domain_element].right)
				denominator = denominator + it2fs[domain_element].right

		if denominator == 0:
			centroid_right = it2fs.mid_domain_element()
			logging.log(logging.ERROR, 'error in calculating z_l, denominator is 0')
			break

		centroid_right = numerator / denominator

		logging.log(logging.DEBUG, f'numerator: {numerator}, denominator: {denominator}, centroid: {centroid_right}')

		if abs(centroid_right - centroid.right) <= error_threshold:
			break
		
		if counter == 15:
			break

		counter = counter + 1

	return centroid