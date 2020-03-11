from type2fuzzy.membership.type1fuzzyset import Type1FuzzySet
import matplotlib.pyplot as plt
import numpy as np

class Type1FuzzyVariable():
    '''
    A type-1 fuzzy variable that is mage up of a number of type-1 fuzzy sets
    '''

    def __init__(self, min_val, max_val, res, name=''):
        '''
        creates a new type-1 fuzzy variable (universe)

        Arguments:
            min_val {number} -- minimum value of variable
            max_val {number} -- maximum value of variable
            res {int} -- resolution of variable, number of ufic
        '''
        self._sets={}
        self._max_val = max_val
        self._min_val = min_val
        self._res = res
        self._name = name

    @property
    def name(self):
        return self._name

    def _add_set(self, name, f_set):
        '''
        adds a fuzzy set to the variable

        Arguments:
            name {string} -- name of the set
            f_set {Type1FuzzySet} -- The set
        '''
        self._sets[name] = f_set

    def get_set(self, name):
        return self._sets[name]

    def add_triangular(self, name, low, mid, high):
        '''[summary]
        
        Arguments:
            name {[type]} -- [description]
            low {[type]} -- [description]
            mid {[type]} -- [description]
            high {[type]} -- [description]
        '''

        new_set = Type1FuzzySet.create_triangular(self._min_val, 
                    self._max_val, self._res, low, mid, high, name)

        self._add_set(name, new_set)

        return new_set


    def generate_sets(self, n):
        '''
        generates 2n+1 fuzzy sets in the variable

        Arguments:
            n {int} -- the number of sets generated will be 2n+1
        '''
        no_sets = (2 * n) + 1
        set_half_support = (self._max_val - self._min_val) / (2 * n)

        # set_count will ne used to name the sets
        set_count = 1

        # first set will be half triangle with both low and mid point at the min value
        s = Type1FuzzySet.create_triangular(self._min_val, self._max_val, self._res, 0, 0, set_half_support)
        self._add_set(str(set_count), s)

        set_count = set_count + 1

        for i in range(0, no_sets-2):
            s = Type1FuzzySet.create_triangular(self._min_val, self._max_val, self._res,
                    i*set_half_support, 
                    (i+1)*set_half_support,
                    (i+2)*set_half_support)
            self._add_set(str(set_count), s)
            set_count = set_count + 1

        # last set will be half triangle with both mid and high point at the hight value
        s = Type1FuzzySet.create_triangular(self._min_val, self._max_val, self._res, 
                self._max_val - set_half_support, self._max_val, self._max_val)
        self._add_set(str(set_count), s)


    def plot_variable(self):
        '''
        plots a graphical representation of the fuzzy variable

        Reference:
            https://stackoverflow.com/questions/4700614/how-to-put-the-legend-out-of-the-plot
        '''
        ax = plt.subplot(111)

        for n ,s in self._sets.items():
            ax.plot(s.domain_elements(), s.dom_elements(), label=n)

        # Shrink current axis by 20%
        pos = ax.get_position()
        ax.set_position([pos.x0, pos.y0, pos.width * 0.8, pos.height])

        # Put a legend to the right of the current axis
        ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))

        plt.show()

    def __str__(self):
        return ', '.join(self._sets.keys())



if __name__=="__main__":
    var = Type1FuzzyVariable(0,100,100)
    var.generate_sets(2)
    var.add_triangular('test', 10, 50, 90)
    var.plot_variable()
