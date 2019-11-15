import numpy as np

class IntervalType2FuzzySetPlot():
	'''
	Plotter class for a interval type-2 fuzzy set.
	'''

	def __init__(self, it2fs):
		'''
		init

		Arguments:
		----------
		it2fs -- a general type-2 fuzzy set
		'''
		self._intervaltype2set = it2fs
		self.divs = 5

	def plot(self, curr_ax):
		'''
		Plots a general type-2 fuzzy set as an image

		Arguments:
		----------
		ax -- the axis for this plot
		row -- the row where this plot is placed
		col -- the column where this row is placed
		'''
		# and set them as current axis
		# curr_ax = ax[row,col]

		primary_domain = self._intervaltype2set.primary_domain()
		upper_membership_function = self._intervaltype2set.higher_membership_function()
		lower_membership_function = self._intervaltype2set.lower_membership_function()

		x_array_res = len(primary_domain)

		curr_ax.plot(primary_domain, upper_membership_function, color='blue')
		curr_ax.plot(primary_domain, lower_membership_function, color='blue')

		curr_ax.fill_between(primary_domain, upper_membership_function, lower_membership_function, color = "grey",alpha = 0.3)

		# # X axis ticks
		# x_ticks = np.linspace(0, self.divs-1 ,self.divs)
		# x_diff = (primary_domain[len(primary_domain)-1] - primary_domain[0]) / (self.divs-1)
		# x_label = ((x_ticks * x_diff)+primary_domain[0])
		# x_formatted_label =  ['%.2f' % elem for elem in x_label]
		# curr_ax.set_xticks(x_ticks * (x_array_res / (self.divs-1)))
		# curr_ax.set_xticklabels(x_formatted_label)

		curr_ax.set_xlabel('x')
		curr_ax.set_ylabel('u')
