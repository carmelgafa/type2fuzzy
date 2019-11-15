'''
Creation, loading and represenation of general type 2 fuzzy sets
'''
import numpy as np
import itertools

def _pri_dom_from_point(point, x_inc=1):
	'''
	Returns the x value from the point touple, adjusted to the closest x value 
	defined in the primary domain array

	Parameters:
	-----------
	point -- the point touple
	x_inc -- the increment of x in the primary domain array x[k+1] - x[k]
				Default value set to 1

	Returns:
	--------
	x - the value of x in the point
	'''
	return (np.round(point[0] / x_inc)) * x_inc

def _sec_dom_from_point(point, u_inc):
	'''
	Returns the u value from the point touple

	Parameters:
	-----------
	point -- the point touple
	u_inc -- the increment of u in the primary domain array u[k+1] - u[k]
				Default value set to 1

	Returns:
	--------
	u - the value of u in the point
	'''
	return (np.round(point[1] / u_inc)) * u_inc

def _deltaleft_from_point(point):
	'''
	Returns the delta_left value from the point touple

	Parameters:
	-----------
	point -- the point touple

	Returns:
	--------
	delta_left - the value of delta_left in the point
	'''
	return point[2]

def _deltaright_from_point(point):
	'''
	Returns the delta_right value from the point touple

	Parameters:
	-----------
	point -- the point touple

	Returns:
	--------
	delta_right - the value of delta_right in the point
	'''
	return point[3]

def generate_gt2set_horizontal(primary_domain, secondary_domain, set_definition):
	'''
	Experimemtal method for generating a type-2 fuzzy set from a pointwise definition
	where each point is a touple (x, u, delta_left, delta_right); where:
	x is the primary domain value of the point
	u is the secondary domain value of the point
	delta_left is the spread of the type 2 set to the left and
	delta_right is the spread to the right of the type 2 set such that
	a triangular funation is forment at u with values x-delta_left, x, x+delta_right

	Parameters:
	-----------
	primary_domain -- 1D array, data vector for primary domain
	secondary_domain -- 1D array, data vector for secondary domain [0,1]
	point_set -- 1D array, data for points that make up the type-2 set

	Returns:
	-------
	gt2fs -- 2D array describing the type-2 set
	'''
	np.seterr(invalid='ignore')

	sec_dom_increment = secondary_domain[1] - secondary_domain[0]
	pri_dom_increment = primary_domain[1] - primary_domain[0]

	gt2fs = np.zeros([len(secondary_domain), len(primary_domain)])

	for idx in range(0, len(set_definition) - 1):

		start_point = set_definition[idx]
		end_point = set_definition[idx + 1]
		assert(_pri_dom_from_point(start_point) <= _pri_dom_from_point(end_point))

		pri_dom_pt_start = _pri_dom_from_point(start_point, pri_dom_increment)
		pri_dom_pt_end = _pri_dom_from_point(end_point, pri_dom_increment)

		deltaleft_pt_start = _deltaleft_from_point(start_point)
		deltaleft_pt_end = _deltaleft_from_point(end_point)
		deltaright_pt_start = _deltaright_from_point(start_point)
		deltaright_pt_end = _deltaright_from_point(end_point)

		sec_dom_pt_start = _sec_dom_from_point(start_point, sec_dom_increment)
		sec_dom_pt_end = _sec_dom_from_point(end_point, sec_dom_increment)

		# generation
		r_k = (primary_domain - pri_dom_pt_start) / (pri_dom_pt_end - pri_dom_pt_start)

		u_k = (r_k * (sec_dom_pt_end - sec_dom_pt_start)) + sec_dom_pt_start
		u_k = (np.round(u_k / sec_dom_increment)) * sec_dom_increment
		u_k_idx = (np.round(u_k / sec_dom_increment)).astype(int)

		left_limit_k = (r_k * (pri_dom_pt_end - deltaleft_pt_end - pri_dom_pt_start +
							deltaleft_pt_start)) + (pri_dom_pt_start - deltaleft_pt_start)
		right_limit_k = (r_k * (pri_dom_pt_end + deltaright_pt_end - pri_dom_pt_start -
								deltaright_pt_start)) + (pri_dom_pt_start + deltaright_pt_start)

		# filter the ones with acceptable secondary domain value
		filter_u = (u_k >= 0) & (u_k <= 1)
		filter_x = (primary_domain >= pri_dom_pt_start) & (primary_domain <= pri_dom_pt_end)
		_filter = filter_u & filter_x
		filter_idx = _filter.nonzero()[0]

		previous_index = None
		for index in filter_idx:
			i = u_k_idx[index]
			sec_grade = np.maximum(np.minimum((primary_domain - left_limit_k[index]) / (primary_domain[index] - left_limit_k[index]),
										(right_limit_k[index] - primary_domain) / (right_limit_k[index] - primary_domain[index])), 0)
			gt2fs[i, :] = np.maximum(gt2fs[i, :], sec_grade)

			# fill up missing portions between points
			missing_range = []
			if previous_index != None:
				step = np.sign(u_k_idx[index] - u_k_idx[index-1])
				if step != 0:
					missing_range = np.arange(
						u_k_idx[previous_index]+step, u_k_idx[index], step)
					gt2fs[missing_range, :] = np.maximum(
						gt2fs[missing_range, :], sec_grade)

			previous_index = index

	return gt2fs
