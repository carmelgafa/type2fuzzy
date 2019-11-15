import numpy as np
from matplotlib import colors as mcolors

class ZSliceType2FuzzySetPlot():
	'''
	Plotter class for a interval type-2 fuzzy set.
	'''

	def __init__(self, zt2fs):
		'''
		init

		Arguments:
		----------
		it2fs -- a general type-2 fuzzy set
		'''
		self._zslicetype2set = zt2fs
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


		colors = dict(mcolors.BASE_COLORS, **mcolors.CSS4_COLORS)

		# Sort colors by hue, saturation, value and name.
		by_hsv = sorted((tuple(mcolors.rgb_to_hsv(mcolors.to_rgba(color)[:3])), name)
						for name, color in colors.items())
		sorted_names = [name for hsv, name in by_hsv]

		step = int(156 / len(self._zslicetype2set.zslices()))

		count = 1
		for slice in self._zslicetype2set.zslices():
			set = self._zslicetype2set[slice]
			upper_membership_function = set.higher_membership_function()
			lower_membership_function = set.lower_membership_function()

			primary_domain = set.primary_domain()

		# x_array_res = len(primary_domain)

			curr_ax.plot(primary_domain, upper_membership_function, color=sorted_names[count])
			curr_ax.plot(primary_domain, lower_membership_function, color=sorted_names[count])

			curr_ax.fill_between(primary_domain, upper_membership_function, lower_membership_function, color = sorted_names[count],alpha = 0.3)

			count = count + step

		# # X axis ticks
		# x_ticks = np.linspace(0, self.divs-1 ,self.divs)
		# x_diff = (primary_domain[len(primary_domain)-1] - primary_domain[0]) / (self.divs-1)
		# x_label = ((x_ticks * x_diff)+primary_domain[0])
		# x_formatted_label =  ['%.2f' % elem for elem in x_label]
		# curr_ax.set_xticks(x_ticks * (x_array_res / (self.divs-1)))
		# curr_ax.set_xticklabels(x_formatted_label)

		curr_ax.set_xlabel('x')
		curr_ax.set_ylabel('u')
