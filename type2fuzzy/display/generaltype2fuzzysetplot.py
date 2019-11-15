import numpy as np

class GeneralType2FuzzySetPlot():
	'''
	Plotter class for a general type-2 fuzzy set.
	'''

	def __init__(self, gt2fs):
		'''
		init

		Arguments:
		----------
		gt2fs         -- a general type-2 fuzzy set
		'''
		self._generaltype2set = gt2fs
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

		primary_domain, secondary_domain, set_array = self._generaltype2set.to_array_explicit()
		y_array_res, x_array_res = np.shape(set_array)

		curr_ax.imshow(set_array, cmap='Reds')

		# X axis ticks
		x_ticks = np.linspace(0, self.divs-1 ,self.divs)
		x_diff = (primary_domain[len(primary_domain)-1] - primary_domain[0]) / (self.divs-1)
		x_label = ((x_ticks * x_diff)+primary_domain[0])
		x_formatted_label =  ['%.2f' % elem for elem in x_label]
		curr_ax.set_xticks(x_ticks * (x_array_res / (self.divs-1)))
		curr_ax.set_xticklabels(x_formatted_label)

		# Y axis ticks
		y_ticks = np.linspace(0, self.divs-1 ,self.divs)
		y_diff = (secondary_domain[len(secondary_domain)-1] - secondary_domain[0]) / (self.divs-1)
		y_label = ((y_ticks * y_diff) + secondary_domain[0])
		y_formatted_label =  ['%.2f' % elem for elem in y_label]
		curr_ax.set_yticks(y_ticks * (y_array_res / (self.divs-1)))
		curr_ax.set_yticklabels(y_formatted_label)

		curr_ax.set_xlabel('x')
		curr_ax.set_ylabel('u')

		# invert axis as set arrays start from 0 value so sets appear inverted
		curr_ax.invert_yaxis()
