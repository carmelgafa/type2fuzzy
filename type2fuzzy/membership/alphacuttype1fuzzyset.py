import numpy as np

class AlphaCutType1FuzzySet:

	def __init__(self):
		'''
		datastructure defining an alpha-slice type-1 fuzzy set 
		is a dictionary having an crisp set for every alpha-cut such as:
		key: value of alpha-cut
		value: corresponding crisp set
		'''
		self._set_definition={}
		self._empty = True

	def __getitem__(self, cut):
		return self._set_definition[cut]

	def alpha_slices(self):
		return self._set_definition.keys()

	@classmethod
	def from_type1fuzzyset(cls, t1fs, number_of_cuts):
		'''
		Converts a Type-1 Fuzzy Set into the union of slices

		Arguments:
		----------
		t1fs -- Type1FuzzySet, the set to convert
		number_of_cuts -- the number of alpha slices
		'''
		
		at1fs = cls()
		
		delta = 1 / number_of_cuts
		precision = len(str(number_of_cuts))

		limits = None
		# TODO: go back to other version?
		#for cut in np.linspace(delta, 1, number_of_cuts):
		for cut in np.linspace(0, 1, number_of_cuts):
			
			cut = round(cut, precision)
			limits = t1fs.alpha_cut(cut)
			
			if not limits.empty:
				at1fs.add_element(cut, limits)
		
		return at1fs

	@property
	def empty(self):
		'''
		Return True if the set is empty
		'''
		return self._empty

	def add_element(self, alpha_cut, limits):
		'''
		'''
		if not limits.empty:
			self._set_definition[alpha_cut] = limits
			self._empty = False

	def cuts(self):
		'''
		returns the alpha-cuts that make this set
		'''
		return self._set_definition.keys()

	def __str__(self):
		'''
		returns a string representation of the alpha-cut type-1 fuzzy set in the form:
		
		alpha-cut_value_1: [left_limit_1, right_limit_1]
		...
		alpha-cut_value_n: [left_limit_n, right_limit_n]

		'''
		representation = []
		for alpha_cut in self._set_definition.keys():
			representation.append(f'{alpha_cut} : {self._set_definition[alpha_cut]}')
		
		return '\n'.join(representation)

	def __repr__(self):
		return f'{self.__class__.__name__}(str(self))'