'''
Type1FuzzyVariable class implementation
'''
from math import ceil
import numpy as np
from type1fuzzyset import Type1FuzzySet
from type1fuzzysetcreation import create_triangular_set

class Type1FuzzyVariable():
    '''
    A type-1 fuzzy variable that is mage up of a number of type-1 fuzzy sets
    '''

    def __init__(self, name:str, min_val:float, max_val:float, resolution=100):
        '''
        creates a new type-1 fuzzy variable (universe)

        Arguments:
            min_val {number} -- minimum value of variable
            max_val {number} -- maximum value of variable
            res {int} -- resolution of variable
        '''
        self._sets={}
        self._max_val = max_val
        self._min_val = min_val
        self._resolution = resolution
        self._name = name
        self._domain = [x for x in np.arange(min_val, max_val, (max_val - min_val) / resolution)]


    @property
    def name(self):
        '''returns the name of the variable'''
        return self._name

    def convert_domain_to_index(self, value:float)->int:
        ''' converts a domain value to the nearest domain index'''
        return ceil((self._max_val - self._min_val)/self._resolution * (value - self._min_val))

    def add_triangular_set(self, name:str, low:float, mid:float, high:float):
        '''
        adds a triangular fuzzy set to the variable

        Arguments:
            name {string} -- name of the set
            low {number} -- set low point, where dom is 0
            mid {number} -- set mid point, where dom is 1
            high {number} -- set high point, where dom is 0

        Returns:
            [Type1FuzzySet] -- the new set
        '''
        idx_a = self.convert_domain_to_index(low)
        idx_b = self.convert_domain_to_index(mid)
        idx_c = self.convert_domain_to_index(high)
        new_set = create_triangular_set(idx_a, idx_b, idx_c)
        self.add_set(name, new_set)


    def add_set(self, name:str, f_set:Type1FuzzySet):
        '''
        adds a fuzzy set to the variable

        Arguments:
            name {string} -- name of the set
            f_set {Type1FuzzySet} -- The set
        '''
        self._sets[name] = f_set

    def get_set(self, name: str)-> Type1FuzzySet:
        '''returns the fuzzy set with the given name'''
        return self._sets[name]

    # def add_triangular(self, name, low, mid, high):
    #     '''
    #     adds a triangular fuzzy set to the variable

    #     Arguments:
    #         name {string} -- name of the set
    #         low {number} -- set low point, where dom is 0
    #         mid {number} -- set mid point, where dom is 1
    #         high {number} -- set high point, where dom is 0

    #     Returns:
    #         [Type1FuzzySet] -- the new set
    #     '''

    #     new_set = Type1FuzzySet.create_triangular(self._min_val,
    #                 self._max_val, self._resolution, low, mid, high, name)

    #     self.add_set(name, new_set)

    #     return new_set


    # def generate_sets(self, n):
    #     '''
    #     generates 2n+1 fuzzy sets in the variable

    #     Arguments:
    #         n {int} -- the number of sets generated will be 2n+1
    #     '''
    #     no_sets = (2 * n) + 1
    #     set_half_support = (self._max_val - self._min_val) / (2 * n)

    #     # set_count will ne used to name the sets
    #     set_count = 1

    #     # first set will be half triangle with both low and mid point at the min value
    #     s = Type1FuzzySet.create_triangular(
    #         self._min_val, self._max_val, self._resolution, 0, 0, set_half_support)
    #     self.add_set(str(set_count), s)

    #     set_count = set_count + 1

    #     for i in range(0, no_sets-2):
    #         s = Type1FuzzySet.create_triangular(self._min_val, self._max_val, self._resolution,
    #                 i*set_half_support,
    #                 (i+1)*set_half_support,
    #                 (i+2)*set_half_support)
    #         self.add_set(str(set_count), s)
    #         set_count = set_count + 1

    #     # last set will be half triangle with both mid and high point at the hight value
    #     s = Type1FuzzySet.create_triangular(self._min_val, self._max_val, self._resolution,
    #             self._max_val - set_half_support, self._max_val, self._max_val)
    #     self.add_set(str(set_count), s)


    def plot_variable(self):
        '''
        plots a graphical representation of the fuzzy variable

        Reference:
            https://stackoverflow.com/questions/4700614/how-to-put-the-legend-out-of-the-plot
        '''
        import matplotlib.pyplot as plt

        ax = plt.subplot(111)

        for n ,s in self._sets.items():
            ax.plot(self._domain, s.elements(), label=n)

        # Shrink current axis by 20%
        pos = ax.get_position()
        ax.set_position([pos.x0, pos.y0, pos.width * 0.8, pos.height])

        # Put a legend to the right of the current axis
        ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))

        plt.show()

    def __str__(self):
        return ', '.join(self._sets.keys())


    def _get_domain_index(self, domain_point:float):
        return (np.abs(self._domain - domain_point)).argmin()

if __name__=="__main__":
    var = Type1FuzzyVariable("test", 0.0, 50.0)
    var.add_triangular_set("low", 0.0, 0.0, 25.0)
    var.add_triangular_set("mid", 0.0, 25.0, 50.0)
    var.add_triangular_set("high", 25.0, 50.0, 50.0)

    var.plot_variable()
