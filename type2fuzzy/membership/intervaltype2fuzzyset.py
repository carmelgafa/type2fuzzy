'''
Interval Type-2 Fuzzy Set
contains the following classes:
- IntervalType2FuzzySet
- IntervalType2FuzzySetException
'''
from type2fuzzy.membership.crispset import CrispSet


class IntervalType2FuzzySetException(Exception):
    '''Interval Type-2 Fuzzy Set Exception'''
    def __init__(self, message):
        super().__init__(message)

class IntervalType2FuzzySet:
    '''An interval type-2 fuzzy set class'''

    def __init__(self):
        self._interval_set_elements = {}
        self._empty=True

    def __getitem__(self, primary_domain_val:float)->CrispSet:
        '''
        For a given value of the primary domain, 
        return the crisp set

        Arguments:
        ----------
        primary_domain_val -- value of primary domain

        Returns:
        --------
        crisp_set - corresponding crisp set
        '''
        if primary_domain_val not in self._interval_set_elements:
            raise IntervalType2FuzzySetException(
                f'Primary domain value of {primary_domain_val} not in this set.')

        return self._interval_set_elements[primary_domain_val]

    @property
    def empty(self):
        '''
        Returns True if set is empty
        '''
        return self._empty

    @ classmethod
    def from_general_type2_set(cls, gt2fs)->'IntervalType2FuzzySet':
        '''
        Creates an Interval Type-2 Fuzzy Set from a General
        Type-2 Fuzzy Set

        Arguments:
        ----------
        gt2fs -- the general type-2 fuzzy set

        Returns:
        --------
        it2fs -- the resulting interval type-2 fuzzy set
        '''
        it2fs = cls()

        it2fs = gt2fs.z_slice(0)

        return it2fs

    @classmethod
    def from_representation(cls, set_representation:str)->'IntervalType2FuzzySet':
        '''creates an interval type-2 fuzzy set from a string representation'''
        if set_representation is None:
            raise IntervalType2FuzzySetException(
                'Interval Type-2 Set Representation cannot be null')
        if set_representation == '':
            raise IntervalType2FuzzySetException(
                'Interval Type-2 Set Representation cannot be empty')

        it2fs = cls()

        try:
            # remove spaces, tabs returns,
            translation_table = dict.fromkeys(map(ord, ' \t\n\r'), None)
            set_representation = set_representation.translate(translation_table)

            # by splitting by '+' we will get the secondary mfs
            sec_mfs_s = set_representation.split('+')

            # so lets go through the membership functions
            for sec_mf in sec_mfs_s:

                # we now split the membership function from the
                # primary domain value
                vslice_points_s, pri_dom_val_s = sec_mf.split('/')

                # get the primary domain value and its corresponding
                # index
                primary_domain_val = float(pri_dom_val_s)

                # the vertical slice points is represented by [left, right]
                # remove the braces
                translation_table = dict.fromkeys(map(ord, '[]'), None)
                vslice_points_s = vslice_points_s.translate(translation_table)

                # split by the '+' so that we will obtain the individual
                # dom / sec domain points
                left_s, right_s = vslice_points_s.split(',')

                left = float(left_s)
                right = float(right_s)

                it2fs.add_element_from_crispset(primary_domain_val, CrispSet(left, right))
        except ValueError as exp:
            raise IntervalType2FuzzySetException('Invalid set format') from exp

        return it2fs

    @classmethod
    def load_file(cls, set_filename:str)->'IntervalType2FuzzySet':
        '''
        Loads a interval type-2 fuzzy set from a file. File must have the
        following format:
        '[l1, h1]/x1 + [l2, h2]/x2 + ... + [ln, hn]/xn'

        Reference:
        ---------

        Arguments:
        ----------
        set_filename -- string, filename of the set

        Returns:
        --------
        it2fs -- IntervalType2FuzzySet

        Raises:
        -------
        Exception -- if set_filename is empty, None or invalid
        '''
        representation = ''

        try:
            with open(set_filename, 'r', encoding='utf-8') as file:
                representation = file.read()
        except IOError as exp:
            raise IntervalType2FuzzySetException(f'Could not read file {set_filename}') from exp

        it2fs = cls()
        it2fs = IntervalType2FuzzySet.from_representation(representation)

        return it2fs

    @classmethod
    def from_hmf_lmf(cls, primary_domain, hmf, lmf)->'IntervalType2FuzzySet':
        '''creates an interval type-2 fuzzy set from a hmf and lmf'''
        it2fs = cls()
        for idx, primary_domain_element in enumerate(primary_domain):
            it2fs.add_element_from_crispset(primary_domain_element, CrispSet(lmf[idx], hmf[idx]))

        return it2fs

    def primary_domain(self)->list[float]:
        '''
        The primary domain of this fuzzy set

        Arguments:
        ----------
        None

        Returns:
        --------
        primary_domain -- list, containing all the values in the primary domain
        '''
        primary_domain = list(self._interval_set_elements.keys())
        return primary_domain

    def mid_domain_element(self)->float:
        '''
        returns the middle domain element
        '''
        return self.primary_domain()[int(len(self.primary_domain())/2)]

    def __str__(self)->str:
        '''
        Creates a string representation of the interval type 2 fuzzy set in the form:
        (lower_1, upper_1)/domain_1 + ... + (lower_n, upper_n)/domain_n
        '''
        set_representation_list = []

        for primary_domain_element in self.primary_domain():
            set_representation_list.append(
                f'{self._interval_set_elements[primary_domain_element]}/{primary_domain_element}\n')

        set_representation = '+'.join(set_representation_list)

        return set_representation

    def __repr__(self)->str:
        return f'{self.__class__.__name__}(str(self))'

    def add_element_from_values(self, primary_domain_val, left, right):
        '''
        Adds an element to the set from the given values

        Arguments:
        ----------
        primary_domain_val -- the primary domain value
        left -- the left value of the crisp set
        right -- the right value of the crisp set

        Returns:
        --------
        None
        '''
        self.add_element_from_crispset(primary_domain_val, CrispSet(left, right))


    def add_element_from_crispset(self, primary_domain_val:float, crisp_set:CrispSet)->None:
        '''
        adds an element to the set from the given crisp set

        Arguments:
        ----------
        primary_domain_val -- the primary domain value
        crisp_set -- the crisp set
        '''

        if crisp_set.empty:
            return

        if primary_domain_val in self._interval_set_elements:
            self._interval_set_elements[primary_domain_val].union(crisp_set)
        else:
            self._interval_set_elements[primary_domain_val] = crisp_set

        if self._empty:
            self._empty = False


    def lower_membership_function(self)->list[float]:
        '''returns the lower membership function'''
        umf = []

        for limits in self._interval_set_elements.values():
            umf.append(limits.left)

        return umf

    def higher_membership_function(self)->list[float]:
        '''returns the higher membership function'''
        hmf = []

        for limits in self._interval_set_elements.values():
            hmf.append(limits.right)

        return hmf
