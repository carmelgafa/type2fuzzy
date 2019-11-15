import numpy as np

class Type1FuzzySetPlot():
	'''
	Plotter class for a general type-2 fuzzy set.
	'''

	def __init__(self, t1fs):
		'''
		init

		Arguments:
		----------
		t1fs         -- a type-1 fuzzy set
		'''
		self._type1set = t1fs
		self.divs = 5

	def plot(self, curr_ax):
		'''
		Plots a type-1 fuzzy set as an graph

		Arguments:
		----------
		ax          -- the axis for this plot
		row         -- the row where this plot is placed
		col         -- the column where this row is placed
		'''
		degree_of_membership = self._type1set.degree_of_membership()
		domain = self._type1set.domain_elements()

		x_array_res = len(domain)

		curr_ax.plot(domain, degree_of_membership)

		curr_ax.set_xlabel('x')
		curr_ax.set_ylabel('u')
