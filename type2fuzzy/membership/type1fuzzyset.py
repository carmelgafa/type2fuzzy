import numpy as np
from type2fuzzy.membership.crispset import CrispSet

class Type1FuzzySet:
	'''
	Reference:
	----------
	Zadeh, Lotfi Asker. "The concept of a linguistic variable and its 
	application to approximate reasoning—I." Information sciences 8.3 (1975): 199-249.

	'''
	def __init__(self, name=''):
		self._elements = {}
		self._empty = True
		self._precision = 3
		self._name = name

	def __eq__(self, value):
		current_domain_len = len(self.domain_elements())
		value_domain_len = len(value.domain_elements())
		union_domain_len = len(list(set(self.domain_elements()).union(value.domain_elements())))

		if current_domain_len != value_domain_len:
			return False

		if union_domain_len != value_domain_len:
			return False

		current_dom_len = len(self.degree_of_membership())
		value_dom_len = len(value.degree_of_membership())
		union_dom_len = len(list(set(self.degree_of_membership()).union(value.degree_of_membership())))

		if current_dom_len != value_dom_len:
			return False

		if union_dom_len != value_dom_len:
			return False

		return True

	def __getitem__(self, x_val):
		'''
		For a given value of x, return the degree of membership

		Reference:
		----------
		Zadeh, Lotfi Asker. "The concept of a linguistic variable and its 
		application to approximate reasoning—I." Information sciences 8.3 (1975): 199-249.

		Arguments:
		----------
		x_val -- value of x 

		Returns:
		--------
		degree of membership -- float

		'''
		return self._elements[x_val]

	def __str__(self):

		set_elements = []
		dec_places_formatter = '''%0.{}f'''.format(self._precision)

		for domain_val, dom_val in self._elements.items():
			set_elements.append(f'{dec_places_formatter % dom_val}/{dec_places_formatter % domain_val}')

		set_representation = ' + '.join(set_elements)

		return set_representation

	def __repr__(self):
		return f'{self.__class__.__name__}({str(self)})'

	@property
	def name(self):
		return self._name

	@ classmethod
	def from_representation(cls, set_representation, name=''):
		'''
		Creates a type-1 fuzzy set from a set representation of the form
		'a1/u1 + a2/u2 + ... + an/un'

		Reference:
		---------
		Zadeh, Lotfi Asker. "The concept of a linguistic variable and its 
		application to approximate reasoning—I." Information sciences 8.3 (1975): 199-249.

		Arguments:
		----------
		set_representation -- string, representation of the t1fs

		Returns:
		--------
		t1fs -- Type-1 Fuzzy Set

		Raises:
		-------
		Exception -- if set_representation is empty, None or invalid
		'''
		if set_representation == None:
			raise Exception('Type-1 Set Representation cannot be null')
		if set_representation == '':
			raise Exception('Type-1 Set Representation cannot be empty')

		t1fs = cls()

		try:
			# remove spaces, tabs returns,
			translation_table = dict.fromkeys(map(ord, ' \t\n\r'), None)
			set_representation = set_representation.translate(translation_table)

			# by splitting by + we will get 
			# the degree of memberships / domain combinations
			set_elements = set_representation.split('+')

			for element in set_elements:
				# we now split the membership function from the
				# primary domain value
				dom_val, domain_val = element.split('/')
				t1fs.add_element(float(domain_val), float(dom_val))

		except ValueError:
			raise Exception('Invalid set type-1 format')

		t1fs._name = name

		return t1fs

	@ classmethod
	def from_alphacut_type1_set(cls, alphacut_set, name=''):
		
		t1fs = cls()
		for cut in alphacut_set.cuts():
			limits = alphacut_set[cut]
			t1fs.add_element(limits.left, cut)
			t1fs.add_element(limits.right, cut)

		# sort dictionary with domain 
		# TODO. do this if required only
		domain_list = t1fs.domain_elements()
		domain_list.sort()
		new_elements = {}
		for domain_value in domain_list:
			new_elements[domain_value] = t1fs._elements[domain_value]
		t1fs._elements = new_elements

		t1fs._name = name

		return t1fs

	@classmethod
	def create_triangular(cls, univ_low, univ_hi, univ_res, set_low, set_mid, set_hi, name=''):

		'''
		Creates a triangular type 1 fuzzy set in a defined universe of discourse
		The triangle is mage of three points; the low where the dom is 0, the mid where the
		dom is 1 and the high where the dom is 0

		References
		----------
		Pedrycz, Witold, and Fernando Gomide. 
		An introduction to fuzzy sets: analysis and design. Mit Press, 1998.

		Arguments:
		----------
		univ_low -- lower value of the universe of discourse
		univ_hi -- higher value of the universe of discourse
		univ_res -- resolution of the universe of discourse
		set_low -- sel low point, where dom is 0
		set_mid -- sel mid point, where dom is 1
		set_hi -- sel high point, where dom is 0

		Returns:
		--------
		The new type1 triangular fuzzy set
		'''

		if univ_hi <= univ_low:
			raise Exception('Error in universe definition')
		if (set_hi < set_mid) or (set_mid < set_low):
			raise Exception('Error in triangular set definition')

		t1fs = cls()

		precision = len(str(univ_res))
		domain_elements =  np.round(np.linspace(univ_low, univ_hi, univ_res), precision)

		idx_mid = (np.abs(domain_elements - set_mid)).argmin()
		set_mid = domain_elements[idx_mid]

		idx_low = (np.abs(domain_elements - set_low)).argmin()
		set_low = domain_elements[idx_low]

		idx_hi = (np.abs(domain_elements - set_hi)).argmin()
		set_hi = domain_elements[idx_hi]

		if idx_hi == idx_mid:
			for domain_val in domain_elements[idx_low:idx_mid+1]:
				dom = (domain_val-set_low)/(set_mid-set_low)
				t1fs.add_element(domain_val, round(dom, precision))			
		elif idx_low == idx_mid:
			for domain_val in domain_elements[idx_mid:idx_hi+1]:
				dom = (set_hi-domain_val)/(set_hi-set_mid)
				t1fs.add_element(domain_val, round(dom, precision))
		else:
			for domain_val in domain_elements[idx_low:idx_hi+1]:
				dom = dom = max(min((domain_val - set_low)/(set_mid - set_low), (set_hi - domain_val)/(set_hi - set_mid)), 0)
				t1fs.add_element(domain_val, round(dom, precision))

		t1fs._name = name

		return t1fs

	@classmethod
	def create_triangular_ex(cls, primary_domain, a, b, c, name=''):

		'''
		Creates a triangular type 1 fuzzy set in a defined universe of discourse
		The triangle is mage of three points; the low where the dom is 0, the mid where the
		dom is 1 and the high where the dom is 0

		References
		----------
		Pedrycz, Witold, and Fernando Gomide. 
		An introduction to fuzzy sets: analysis and design. Mit Press, 1998.

		Arguments:
		----------

		a -- set low point, where dom is 0
		b -- set mid point, where dom is 1
		c -- set high point, where dom is 0

		Returns:
		--------
		The new type1 triangular fuzzy set

		Exceptions:
		-----------
			Raises exception if lower value or higher value is equal to middle value.
			Unlike create_triangular, create_triangular_ex requires a non-right triangle.
		'''
		if (c <= b) or (b <= a):
			raise Exception('Error in triangular set definition')

		t1fs = cls()

		for x in primary_domain:
			dom = max(min((x - a)/(b - a), (c - x)/(c - b)), 0)
			t1fs.add_element(x, dom)

		t1fs._name = name

		return t1fs

	@staticmethod
	def adjust_value(val, val_array):
		idx = (np.abs(val_array - val)).argmin()
		return val_array[idx]

	@classmethod
	def create_trapezoidal(cls, domain, a, b, c, d, name=''):
		'''
		'''
		t1fs = cls()

		for domain_val in domain:
			if domain_val > a and domain_val < d:
				if b == a:
					dom = min(max((d-domain_val)/(d-c), 0), 1)
				elif d==c:
					dom = min(max((domain_val-a)/(b-a), 0), 1)
				else:
					dom = min(max(min((domain_val-a)/(b-a), (d-domain_val)/(d-c)), 0), 1)

				t1fs.add_element(domain_val, dom)
			else:
				t1fs.add_element(domain_val, 0)

		t1fs._name = name

		return t1fs

	@property
	def empty(self):
		'''
		True if the set is empty, i.e. there is no element with dom > 0
		'''
		return self._empty

	def elements(self):
		'''
		Returns a copy of the elements making up this t1fs in the form a dictionary

		Arguments:
		----------

		Returns:
		--------
		elements - dict, containing domain:degree_of_membership pairs
		'''
		elements = self._elements
		return elements

	def element_count(self):
		return len(self._elements)

	def add_element(self, domain_val, dom_val):
		'''
		Adds a new element to the t1fs. If there is already an element at the stated
		domain value the maximum degree of membership value is kept

		Arguments:
		----------
		domain_val -- float, the value of x
		degree_of_membership, float value between 0 and 1. The degree of membership
		'''
		if dom_val > 1:
			raise ValueError('degree of membership must not be greater than 1, {} : {}'.format(domain_val, dom_val))

		if domain_val in self._elements:
			self._elements[domain_val] = max(self._elements[domain_val], dom_val)
		else:
			self._elements[domain_val] = dom_val
			self._empty = False

	def domain_elements(self):
		'''
		Return a list of all the domain elements

		Returns:
		--------
		domain_vals -- list, containing all the values of the domain
		'''
		domain_vals = list(self._elements.keys())
		return domain_vals
	
	def dom_elements(self):
		'''
		Returns a list of all the doms in the set

		Returns:
		--------
		dom_vals -- list, containing all the values of the dom
		'''
		dom_vals = list(self._elements.values())
		return dom_vals

	def degree_of_membership(self):
		'''
		Return a list of all the degree of membership values

		Returns:
		--------
		doms -- list, containing all the values of the degree of membership values
		'''
		doms = list(self._elements.values())
		return doms

	def size(self):
		'''
		The size of the set

		Returns:
		--------
		set_size: int, the number of elements in the set
		'''
		set_size = len(self._elements)
		return set_size

	def domain_limits(self):
		'''
		Returns the domain limits of this t1fs

		Reference:
		----------

		Arguments:
		----------

		Returns:
		--------
		limits -- CrispSet containting the smallest an largest domain value
		'''

		limits = CrispSet(min(self._elements.keys()), max(self._elements.keys()))
		return limits
	
	def alpha_cut(self, alpha_val):

		if alpha_val == 0:
			filter_idx = (np.array(self.degree_of_membership()) > 0).nonzero()[0]

		else:
		# create a filter of the degrees of membership that exceed the cut value
			filter_idx = (np.array(self.degree_of_membership()) >= alpha_val).nonzero()[0]

		# appply the filter on the domain to get the values included in the alpha-cut
		cut = np.array(self.domain_elements())[filter_idx]

		limits = CrispSet()

		if len(cut>0):
			limits.left = min(cut)
			limits.right = max(cut)

		return limits

	def extend(self, func):

		resultant_set = Type1FuzzySet()

		for domain_val in self.domain_elements():
			resultant_set.add_element(func(domain_val), self[domain_val])
		
		return resultant_set

	# operators
	def join(self, a_set):

		resultant_set = Type1FuzzySet()

		for domain_element in self.domain_elements():
			for a_set_domain_element in a_set.domain_elements():
				
				resultant_set.add_element(max(domain_element, a_set_domain_element), 
											min(self[domain_element], a_set[a_set_domain_element]))

		return resultant_set

	def meet(self, a_set):

		resultant_set = Type1FuzzySet()

		for domain_element in self.domain_elements():
			for a_set_domain_element in a_set.domain_elements():
				
				resultant_set.add_element(min(domain_element, a_set_domain_element), 
											min(self[domain_element], a_set[a_set_domain_element]))

		return resultant_set

	def negation(self):
		resultant_set = Type1FuzzySet()

		for domain_element in self.domain_elements():
				resultant_set.add_element(1 - domain_element, 
											self[domain_element])

		return resultant_set

	def union(self, other_smf):
		resultant_set = set.intersection(set(self._elements), set(other_smf._elements))

		resultant_smf = {}
		for  domain_val in resultant_set:
			resultant_smf[domain_val] = max(self._elements[domain_val], other_smf.elements[domain_val])

		return resultant_smf

	def intersection(self, other_smf):
		'''
		'''
		resultant_set = set.intersection(set(self._elements), set(other_smf._elements))

		resultant_smf = {}
		for  domain_val in resultant_set:
			resultant_smf[domain_val] = min(self._elements[domain_val], other_smf.elements[domain_val])

		return resultant_smf

	def plot_set(self, ax, col=''):
		ax.plot(self.domain_elements(), self.dom_elements(), col)
		ax.set_ylim([-0.1,1.1])
		ax.set_title(self._name)
		ax.grid(True, which='both', alpha=0.4)
		ax.set(xlabel='x', ylabel='$\mu(x)$')
