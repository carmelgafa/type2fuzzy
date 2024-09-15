'''Type1FuzzySet class implementation'''
import numpy as np
import matplotlib.pyplot as plt

class Type1FuzzySetException(Exception):
    '''Type-1 Fuzzy Set Exception'''
    def __init__(self, message):
        super().__init__(message)

class Type1FuzzySet:
    '''
    Reference:
    ----------
    Zadeh, Lotfi Asker. "The concept of a linguistic variable and its 
    application to approximate reasoning—I." Information sciences 8.3 (1975): 199-249.

    '''
    def __init__(self, resolution=100):
        self._elements = [0 for i in range(resolution)]
        self._empty = True
        self._precision = 3

    def __eq__(self, type1fs):
        ''' Compares two Type-1 Fuzzy Sets for equality. '''

        if len(self._elements) != len(type1fs._elements):
            return False

        for idx, val in enumerate(self._elements):
            if val != type1fs[idx]:
                return False

        return True

    def __getitem__(self, idx):
        ''' return the degree of membership '''
        return self._elements[idx]

    def __str__(self):

        set_representation = ''
        for idx, val in enumerate(self._elements):
            set_representation = set_representation + f'{val} / {idx} + '

        return set_representation

    def __repr__(self):
        return f'{self.__class__.__name__}({str(self)})'

    @property
    def empty(self):
        '''
        True if the set is empty, i.e. there is no element with dom > 0
        '''
        return self._empty

    def elements(self) -> list:
        ''' Returns a copy of the elements making up this t1fs '''
        return  self._elements.copy()

    def element_count(self):
        '''returns the number of elements in the set'''
        return len(self._elements)

    def add_element(self, idx, dom_val):
        ''' Adds a new element to the t1fs. '''
        if dom_val > 1:
            raise Type1FuzzySetException(
                'degree of membership must not be greater than 1')

        if idx > len(self._elements)-1:
            raise Type1FuzzySetException(
                f'domain index {idx} out of range. maximum domain index is {len(self._elements)-1}')

        # try:
        self._elements[idx] = dom_val
        # except IndexError:
        #     print(f'error on index {idx}')
    
        self._empty = False

    # def domain_elements(self):
    #     '''
    #     Return a list of all the domain elements

    #     Returns:
    #     --------
    #     domain_vals -- list, containing all the values of the domain
    #     '''
    #     domain_vals = list(self._elements.keys())
    #     return domain_vals

    def size(self):
        '''
        The size of the set

        Returns:
        --------
        set_size: int, the number of elements in the set
        '''
        set_size = len(self._elements)
        return set_size



    # def alpha_cut(self, alpha_val):
    #     '''creates an alpha-cut of the t1fs'''
    #     # create a filter of the degrees of membership that exceed the cut value
    #     if alpha_val == 0:
    #         filter_idx = (np.array(self.degree_of_membership()) > 0).nonzero()[0]

    #     else:
    #     # create a filter of the degrees of membership that exceed the cut value
    #         filter_idx = (np.array(self.degree_of_membership()) >= alpha_val).nonzero()[0]

    #     # apply the filter on the domain to get the values included in the alpha-cut
    #     cut = np.array(self.domain_elements())[filter_idx]

    #     limits = CrispSet()

    #     if len(cut>0):
    #         limits.left = min(cut)
    #         limits.right = max(cut)

    #     return limits

    def extend(self, func):
        '''extends the t1fs with the function func'''
        resultant_set = Type1FuzzySet()

        for domain_val in self.domain_elements():
            resultant_set.add_element(func(domain_val), self[domain_val])

        return resultant_set

    # operators
    def join(self, a_set):
        '''joins two t1fs'''
        resultant_set = Type1FuzzySet()

        for domain_element in self.domain_elements():
            for a_set_domain_element in a_set.domain_elements():

                resultant_set.add_element(
                    max(
                        domain_element,
                        a_set_domain_element),
                    min(
                        self[domain_element],
                        a_set[a_set_domain_element]))

        return resultant_set

    def meet(self, a_set):
        '''meets two t1fs'''
        resultant_set = Type1FuzzySet()

        for domain_element in self.domain_elements():
            for a_set_domain_element in a_set.domain_elements():

                resultant_set.add_element(
                    min(
                        domain_element,
                        a_set_domain_element),
                    min(
                        self[domain_element],
                        a_set[a_set_domain_element]))

        return resultant_set

    def negation(self):
        '''negates the t1fs'''
        resultant_set = Type1FuzzySet()

        for domain_element in self.domain_elements():
            resultant_set.add_element(
                1 - domain_element,
                self[domain_element])

        return resultant_set

    def union(self, other_smf):
        '''unions two t1fs'''
        resultant_set = set.intersection(set(self._elements), set(other_smf.elements))

        resultant_smf = {}
        for  domain_val in resultant_set:
            resultant_smf[domain_val] = max(
                self._elements[domain_val],
                other_smf.elements[domain_val])

        return resultant_smf

    def intersection(self, other_smf):
        ''' intersects two t1fs'''
        resultant_set = set.intersection(set(self._elements), set(other_smf.elements))

        resultant_smf = {}
        for  domain_val in resultant_set:
            resultant_smf[domain_val] = min(
                self._elements[domain_val],
                other_smf.elements[domain_val])

        return resultant_smf

    def plot_set(self, ax=None, col='', name='set'):
        '''plots the t1fs'''
        
        if ax is None:
            ax = plt.gca()
        
        ax.plot(self._elements)
        ax.set_ylim([-0.1,1.1])
        ax.set_title(name)
        ax.grid(True, which='both', alpha=0.4)
        ax.set(xlabel='x', ylabel='$\mu(x)$')


if __name__ == '__main__':
    f_set = Type1FuzzySet(resolution=10)
    f_set.add_element(0, 0)
    f_set.add_element(1, 0)
    f_set.add_element(2, 0.2)
    f_set.add_element(3, 0.4)
    f_set.add_element(4, 0.6)
    f_set.add_element(5, 0.8)
    f_set.add_element(6, 1.0)
    f_set.add_element(7, 0.5)
    f_set.add_element(8, 0)
    f_set.add_element(9, 0)

    f_set.plot_set()
    plt.show()