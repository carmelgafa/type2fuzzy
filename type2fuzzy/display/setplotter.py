import matplotlib.pyplot as plt
import numpy as np
import math
from type2fuzzy.display.generaltype2fuzzysetplot import GeneralType2FuzzySetPlot
from type2fuzzy.display.type1fuzzysetplot import Type1FuzzySetPlot
from type2fuzzy.display.intervaltype2fuzzysetplot import IntervalType2FuzzySetPlot
from type2fuzzy.display.zslicetype2fuzzysetplot import ZSliceType2FuzzySetPlot
class SetPlotter():
	'''
	Plotting of fuzzy sets
	'''
	def __init__(self):
		'''
		initialized a list that contains all set plots
		'''
		self._setplots = []

	def add_generaltype2set(self, generaltype2set):
		'''
		Adds a general type-2 fuzzy set to the list of the sets to be plotted

		Arguments:
		----------
		generaltype2set     -- GeneralType2FuzzySet, the set to be plotted
		'''
		self._setplots.append(GeneralType2FuzzySetPlot(generaltype2set))

	def add_invervaltype2set(self, intervaltype2set):
		'''
		Adds an interval type-2 fuzzy set to the list of the sets to be plotted

		Arguments:
		----------
		intervaltype2set     -- GeneralType2FuzzySet, the set to be plotted
		'''
		self._setplots.append(IntervalType2FuzzySetPlot(intervaltype2set))

	def add_zslicetype2set(self, zslicetype2set):
		'''
		Adds a z-slice type-2 fuzzy set to the list of the sets to be plotted

		Arguments:
		----------
		intervaltype2set     -- GeneralType2FuzzySet, the set to be plotted
		'''
		self._setplots.append(ZSliceType2FuzzySetPlot(zslicetype2set))

	def add_type1fuzzyset(self, type1fuzzyset):
		self._setplots.append(Type1FuzzySetPlot(type1fuzzyset))

	def plot(self, number_cols):
		'''
		Plots all the sets in the list

		Arguments:
		----------
		number_cols -- the number of columns for this sheet
		'''
		number_rows = math.ceil(len(self._setplots)/number_cols)

		_, ax = plt.subplots(number_rows, number_cols)

		single_line = (number_rows == 1) or (number_cols == 1)

		for idx, setplot in enumerate(self._setplots):

			# calculate the row and column number
			row = int(idx / number_cols)
			col = idx % number_cols

			if single_line:
				setplot.plot(ax[row+col])
			else:
				setplot.plot(ax[row, col])

		plt.show()
