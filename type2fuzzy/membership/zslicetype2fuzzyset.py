import numpy as np

class ZSliceType2FuzzySet:

	def __init__(self):
		'''
		datastructure defining a z-slice type-2 fuzzy set is a dictionary having
		an interval type-2 fuzzy set for every z_value such as:
		key: value of z-slice
		value: corresponding interval typ2-2 fuzzy set
		'''
		self._z_slice_set_elements = {}
		self._empty = True

	@ classmethod
	def from_general_type2_set(cls, gt2fs, no_slices):
		
		zt2fs = cls()

		z_vals = np.linspace(0, 1, no_slices+1)

		for z_val in z_vals:
			z_sliced_set =  gt2fs.z_slice(z_val)

			if not z_sliced_set.empty:
				zt2fs.add_element(z_val, z_sliced_set)# 
				zt2fs._empty = False
		return zt2fs

	@property
	def empty(self):
		return self._empty

	def add_element(self, z_slice_val, z_sliced_set):
		self._z_slice_set_elements[z_slice_val] = z_sliced_set


	@staticmethod
	def adjust_value(val, val_array):
		val_array=np.array(val_array)
		idx = (np.abs(val_array - val)).argmin()
		return val_array[idx]

	def __getitem__(self, z_slice_val):
		'''
		For a given z-slice value, 
		return the corresponding interval type-2 fuzzy set

		Arguments:
		----------
		z_slice_val -- value of z-slice

		Returns:
		--------
		it2fs - corresponding interval type-2 set
		'''
		if z_slice_val not in self.zslices():
			raise Exception(f'z-slice value of {z_slice_val} not in this set.')

		z_slice_val = self.adjust_value(z_slice_val, self.zslices())

		return self._z_slice_set_elements[z_slice_val]

	def zslices(self):
		return list(self._z_slice_set_elements.keys())

	def __str__(self):
		'''

		'''
		representation = []

		for slice in self._z_slice_set_elements:
			representation.append(f'slice {slice}:\n {self._z_slice_set_elements[slice]}')

		return '\n'.join(representation)
	
	def __repr__(self):
		return f'{self.__class__.__name__}(str(self))'