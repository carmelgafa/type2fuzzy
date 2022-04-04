import numpy as np
import itertools
from type2fuzzy.membership.secondarymf import SecondaryMembershipFunction as smf
from type2fuzzy.membership.generate_gt2mf import generate_gt2set_horizontal
from type2fuzzy.membership.intervaltype2fuzzyset import IntervalType2FuzzySet


class GeneralType2FuzzySet:
    '''
    An implementation of a general type 2 fuzzy set
    As a data structure, the general type-2 fuzzy set
    is represented by a dict of
    {primary_domain_val : secondary membership function object}
    '''

    def __init__(self):
        '''
        The data structure, the general type-2 fuzzy set
        is represented by a dict of
        {primary_domain_val : secondary membership function object}
        '''
        self.vertical_slices = {}
        self._precision = 4

    def __getitem__(self, primary_domain_val):
        '''
        For a given value of the primary domain,
        return the secondary membership function object

        Arguments:
        ----------
        primary_domain_val -- value of primary domain

        Returns:
        --------
        secondary_membership_function - smf object
        '''
        if primary_domain_val not in self.vertical_slices:
            raise Exception('Primary domain value of {} not in this set.'.format(primary_domain_val))

        return self.vertical_slices[primary_domain_val]

    def __eq__(self, value):

        current_primary_len = len(self.primary_domain())
        value_primary_len = len(value.primary_domain())
        union_primary_len = len(list(set(self.primary_domain()).union(value.primary_domain())))

        if current_primary_len != value_primary_len:
            return False 

        if union_primary_len != value_primary_len:
            return False

        for pri_domain in self.primary_domain():
            if self[pri_domain] != value[pri_domain]:
                return False

        return True

    def __str__(self):
        '''
        Returns a formal representation of the general type-2 fuzzy set in the form:
        '(a1/u1 + a2/u2 + ... + an/un)/x1 + ... + (b1/u1 + b2/u2 + ... + bn/un)/xn'

        Reference:
        ----------
        J. M. Mendel and R. I. B. John, “Type-2 fuzzy sets made simple,” IEEE
        Trans. Fuzzy Systems, vol. 10, no. 2, pp. 117–127, Apr. 2002.

        Arguments:
        ----------
        num_dec_places  -- number of decimal places

        Returns:
        --------
        set_representation -- string representation of gt2fs
        '''
        represented_slices = []
        dec_places_formatter = '''%0.{}f'''.format(self._precision)

        for primary_domain_val in self.primary_domain():
            sec_domains = list(self.vertical_slice(primary_domain_val).domain_elements())
            doms = list(self.vertical_slices[primary_domain_val].dom_elements())

            def slice_rep_creation(sec_domains, doms): return dec_places_formatter % (
                doms)+' / ' + dec_places_formatter % (sec_domains)

            m = map(slice_rep_creation, sec_domains, doms)

            slice_rep = ' + '.join(m)
            represented_slices.append('(' + slice_rep + ')')

        def f2(sec_domains, doms): return doms + ' / ' + dec_places_formatter % (sec_domains)
        m2 = map(f2, self.primary_domain(), represented_slices)
        set_representation = ' + '.join(m2)

        return set_representation

    def __repr__(self):
        return f'{self.__class__.__name__}({str(self)})'

    @classmethod
    def from_representation(cls, set_representation):
        '''
        Creates a general type-2 fuzzy set from a set representation of the form
        '(a1/u1 + a2/u2 + ... + an/un)/x1 + ... +(b1/u1 + b2/u2 + ... + bn/un)/xm'

        Reference:
        ---------
        J. M. Mendel and R. I. B. John, “Type-2 fuzzy sets made simple,” IEEE
        Trans. Fuzzy Systems, vol. 10, no. 2, pp. 117–127, Apr. 2002.

        Definition of secondary grade - pg 119

        Arguments:
        ----------
        set_representation -- string, representation of the gt2fs

        Returns:
        --------
        gt2fs -- GeneralType2FuzzySet

        Raises:
        -------
        Exception -- if set_representation is empty, None or invalid
        '''
        if set_representation is None:
            raise Exception('Type-2 Set Representation cannot be null')
        if set_representation == '':
            raise Exception('Type-2 Set Representation cannot be empty')

        gt2fs = cls()

        try:
            # remove spaces, tabs returns,
            translation_table = dict.fromkeys(map(ord, ' \t\n\r'), None)
            set_representation = set_representation.translate(translation_table)

            # by splitting by +( we will get the secondary mfs
            # we would lose the initial ( of each mf except for the
            # first one - this will be removed lated
            sec_mfs_s = set_representation.split('+(')

            # so lets go through the membership functions
            for sec_mf in sec_mfs_s:
                # remove the leading '('
                # this will only happen in the first mf
                translation_table = dict.fromkeys(map(ord, '('), None)
                sec_mf = sec_mf.translate(translation_table)

                # we now split the secondary membership function from the
                # primary domain value
                vertical_slice_points_s, pri_dom_val_s = sec_mf.split(')/')

                # get the primary domain value and its corresponding
                # index
                primary_domain_val = float(pri_dom_val_s)

                # split by the '+' so that we will obtain the individual
                # dom / sec domain points
                points_s = vertical_slice_points_s.split('+')

                # we then examine each point to add them to the set
                for point_s in points_s:
                    # split by / so to obtain the dom and the sec domain value
                    sec_grade_val_s, sec_dom_val_s = point_s.split('/')

                    # get the secondary domain value and its corresponding
                    # index
                    secondary_domain_val = float(sec_dom_val_s)

                    sec_grade = float(sec_grade_val_s)
                    # add the point to the set
                    gt2fs.add_element(primary_domain_val, secondary_domain_val, sec_grade)
        except ValueError:
            raise Exception('Invalid set format')

        return gt2fs

    @classmethod
    def from_array(cls, primary_domain, secondary_domain, set_array):
        '''
        Creates a general type-2 fuzzy set from an array representation 
        of set where given is
        x -- a list containing the values of the primary domain
        u -- a list containing the values of the secondary domain
        set_array -- a 2D array where the rows map to the values of the u list
                                    the cols map to the values of the x list
                                    each value is the secondary grade value for
                                    the particular x / u combination
        

        Reference:
        ---------

        Arguments:
        ----------
        set_array -- 2D array containing the secondary grade values of the gt2fs
        x -- list containing the values of the primary domain
        u -- list containing the values of the secondary domain

        Returns:
        --------
        gt2fs -- GeneralType2FuzzySet

        Raises:
        -------
        Exception -- if there is a mismatch between the x, u and set_array dimensions
        '''
        set_array = np.array(set_array)

        # check that array sizes are correct
        (secondary_domain_size, primary_domain_size) = np.shape(set_array)

        if secondary_domain_size != len(secondary_domain):
            raise Exception('Secondary domain size mismatch')

        if primary_domain_size != len(primary_domain):
            raise Exception('Primary domain size mismatch')

        gt2fs = cls()

        # load all the elements in the array
        for pri_dom_val_idx, pri_dom_val in enumerate(primary_domain):
            for sec_dom_val_idx, sec_dom_val in enumerate(secondary_domain):
                gt2fs.add_element(pri_dom_val, sec_dom_val, set_array[sec_dom_val_idx][pri_dom_val_idx])

        return gt2fs

    @classmethod
    def load_file(cls, set_filename):
        '''
        Loads a general type-2 fuzzy set from a file. File must have the
        following format:
        '(a1/u1 + a2/u2 + ... + an/un)/x1 + (b1/u1 + b2/u2 + ... + bn/un)/xn'

        Reference:
        ---------
        J. M. Mendel and R. I. B. John, “Type-2 fuzzy sets made simple,” IEEE
        Trans. Fuzzy Systems, vol. 10, no. 2, pp. 117–127, Apr. 2002.

        Definition of secondary grade - pg 119

        Arguments:
        ----------
        set_filename -- string, filename of the set

        Returns:
        --------
        gt2fs -- GeneralType2FuzzySet

        Raises:
        -------
        Exception -- if set_filename is empty, None or invalid
        '''
        representation = ''
        
        try:
            with open(set_filename, 'r') as file:
                representation = file.read()
        except IOError:
            raise Exception('Could not read file {}'.format(set_filename))
        
        gt2fs = cls()
        gt2fs = GeneralType2FuzzySet.from_representation(representation)

        return gt2fs

    @classmethod
    def from_horizontal_representation(cls, primary_domain, secondary_domain, set_def):
        '''
        Experimental method of representing a general type-2 fuzzy set by defining the
        spread at the points of piecewise type-1 parts.
        each point is a tuple (x, u, delta_left, delta_right); where:
        x is the primary domain value of the point
        u is the secondary domain value of the point
        delta_left is the spread of the type 2 set to the left and
        delta_right is the spread to the right of the type 2 set such that
        a triangular function is formed at u with values x-delta_left, x, x+delta_right

        Reference:
        ----------

        Arguments:
        ----------
        None

        Returns:
        --------
        gt2fs -- GeneralType2FuzzySet
        '''
        set_array = generate_gt2set_horizontal(primary_domain, secondary_domain, set_def)
        return GeneralType2FuzzySet.from_array(primary_domain, secondary_domain, set_array)

    def vertical_slice(self, primary_domain_val):
        '''
        For a given value of the primary domain, 
        returns a representation of the vertical slice
        in the form of a dict
        {secondary_domain : secondary_grade,  ... }

        Reference:
        ----------
        J. M. Mendel and R. I. B. John, “Type-2 fuzzy sets made simple,” IEEE
        Trans. Fuzzy Systems, vol. 10, no. 2, pp. 117–127, Apr. 2002.

        Arguments:
        ----------
        primary_domain_val -- value of primary domain

        Returns:
        --------
        vertical_slice - dict representing the values if the vertical slice
        '''
        return self[primary_domain_val]

    def save_file(self, set_filename, num_dec_places=4):
        '''
        Writes a formal representation of the general type-2 fuzzy set of the form:
        '(a1/u1 + a2/u2 + ... + an/un)/x1 + ... + (b1/u1 + b2/u2 + ... + bn/un)/xn'
        in a file

        Reference:
        ----------
        J. M. Mendel and R. I. B. John, “Type-2 fuzzy sets made simple,” IEEE
        Trans. Fuzzy Systems, vol. 10, no. 2, pp. 117–127, Apr. 2002.

        Arguments:
        ----------
        set_filename -- string containing the path of the file to be written
        num_dec_places -- number of decimal places used for secondary membership function, default 4

        Returns:
        --------
        None
        '''
        try:
            with open(set_filename, 'w') as fuzzy_file:
                fuzzy_file.write(self.__str__())
        except IOError:
            raise Exception('Unable to write file {}'.format(set_filename))

    def to_array_explicit(self):
        '''
        Transforms a General type 2 fuzzy set into a 2D array

        Arguments:
        ----------
        None

        Returns:
        --------
        primary_domain -- 1D array containing all the values in the primary domain
        secondary_domain -- 1D array containing all the values in the secondary domain
        set_array -- 2D array containing the degree of membership for the corresponding
                    primary/secondary combination
        '''

        # get all possible value of the secondary domain by a union with all the elements of
        # each vertical slice
        secondary_domain = []
        for primary_domain_val in self.vertical_slices:
            secondary_domain = list(set().union(secondary_domain, list(self[primary_domain_val].domain_elements())))

        secondary_domain.sort()

        # get all possible value of the primary domain
        primary_domain =  list(self.vertical_slices.keys())
        primary_domain.sort()

        # create an array to hold the dom
        set_array = np.zeros((len(secondary_domain), len(primary_domain)))

        for primary_domain_val in self.vertical_slices:
            pri_domain_idx = primary_domain.index(primary_domain_val)

            for sec_domain_val in self.vertical_slice(primary_domain_val).elements():
                sec_domain_idx = secondary_domain.index(sec_domain_val)

                set_array[sec_domain_idx, pri_domain_idx] = self.vertical_slice(primary_domain_val)[sec_domain_val]

        return primary_domain, secondary_domain, set_array

    def to_array_implicit(self, primary_domain, secondary_domain):
        '''
        Transforms a General type 2 fuzzy set into a 2D array but specifying the primary
        and secondary domain discrete values. The values of the set are thereby approximated 
        to these specified values

        Arguments:
        ----------
        primary_domain -- 1D array containing all the values in the primary domain
        secondary_domain -- 1D array containing all the values in the secondary domain

        Returns:
        --------
        set_array -- 2D array containing the degree of membership for the corresponding
                        primary/secondary combination
        '''

        # convert domain lists to numpy arrays
        primary_domain = np.array(primary_domain)
        secondary_domain = np.array(secondary_domain)
        
        # create resultant set
        set_array = np.zeros((len(secondary_domain), len(primary_domain)))

        # for each primary domain element, get closest element form list
        for primary_domain_val in self.vertical_slices:
            pri_dom_val_idx = np.argmin(np.abs(primary_domain - primary_domain_val))

            # for each secondary domain element, get closest element form list
            for sec_domain_val in self.vertical_slices[primary_domain_val]._elements:
                sec_dom_val_idx = np.argmin(np.abs(secondary_domain-sec_domain_val))

                # add set element in array
                set_array[sec_dom_val_idx, pri_dom_val_idx] = self.vertical_slice(primary_domain_val)[sec_domain_val]

        return set_array

    def primary_domain(self):
        '''
        The primary domain of this fuzzy set

        Arguments:
        ----------
        None

        Returns:
        --------
        primary_domain -- 1D array containing all the values in the primary domain
        '''
        primary_domain = list(self.vertical_slices.keys())
        return primary_domain

    def add_element(self, primary_domain_val, secondary_domain_val, secondary_grade):
        '''
        Adds a new element to the general type-2 fuzzy set. 
        Will not add the element if the secondary grade is 0
        Will raise and exception if secondary domain is <1 and >0
        or secondary grade is <1 and >0

        Arguments:
        ----------
        primary_domain_val -- float, value of the primary domain
        secondary_domain_val -- float, value of the secondary domain, must be <1 and >0
        secondary_grade -- float value of the secondary grade, must be <1 and >0

        Returns:
        --------
        None

        Raises:
        -------
        Exception if secondary domain is <1 and >0
        or secondary grade is <1 and >0
        '''
        # ignore if secondary grade = 0
        # if secondary_grade == 0:
        # 	return
        
        # raise exception if secondary grade >1 or <0
        if secondary_grade > 1 or secondary_grade < 0:
            raise Exception('Invalid secondary grade value {} at x={} and u={}'.format(secondary_grade, primary_domain_val, secondary_domain_val))

        # raise exception if secondary domain >1 or <0
        if secondary_domain_val > 1 or secondary_domain_val < 0:
            raise Exception('Invalid secondary domain value {} at x={}'.format(secondary_domain_val, primary_domain_val))

        # if the primary domain exists just add the value of the smf
        # if not create a new smf to that primary domain value and
        # add that value
        if primary_domain_val in self.vertical_slices:
            self.vertical_slices[primary_domain_val].add_element(
                secondary_domain_val, secondary_grade)
        else:
            secondary_function = smf()
            secondary_function.add_element(secondary_domain_val, secondary_grade)
            self.vertical_slices[primary_domain_val] = secondary_function

    def add_membership_function(self, primary_domain_val, membership_function):
        '''
        Adds a membership function to the general type-2 fuzzy set. 
        uses the add_element() method and uses the checks implemented in
        that function
        
        Arguments:
        ----------
        primary_domain_val -- float, value of the primary domain
        membership_function -- TYpe1FuzzySet, membership function to be added

        Returns:
        --------
        None
        '''
        for secondary_domain_val in membership_function.domain_elements():
            self.add_element(primary_domain_val, secondary_domain_val, membership_function[secondary_domain_val])

    def footprint_of_uncertainty(self):
        '''
        For all values of x, return the limits of the values of u where 
        the secondary grade > 0

        Reference:
        ----------
        J. M. Mendel and R. I. B. John, “Type-2 fuzzy sets made simple,” IEEE
        Trans. Fuzzy Systems, vol. 10, no. 2, pp. 117–127, Apr. 2002.

        Arguments:
        ----------
        None
        
        Returns:
        --------
        footprint -- dict of primary domain element : (limits tuple)
        '''
        fou = {}

        for primary_domain_val in self.primary_domain():
            limits = self.vertical_slices[primary_domain_val].domain_limits()
            if not limits.empty:
                fou[primary_domain_val] = limits

        return fou

    def z_slice(self, slice_value):
        '''

        '''
        sliced_set = IntervalType2FuzzySet()

        for primary_domain_val in self.primary_domain():
            cut = self.vertical_slices[primary_domain_val].alpha_cut(slice_value)

            if not cut.empty:
                sliced_set.add_element_from_crispset(primary_domain_val, cut)

        return sliced_set

    def primary_membership(self, primary_domain_val):
        '''
        Returns the domain of the secondary membership function that is called the
        primary membership

        Reference:
        ----------
        J. M. Mendel and R. I. B. John, “Type-2 fuzzy sets made simple,” IEEE
        Trans. Fuzzy Systems, vol. 10, no. 2, pp. 117–127, Apr. 2002.

        Arguments:
        ----------
        None

        Returns:
        --------
        _primary_membership -- list containing the domain of the secondary function
                                at X = primary_domain_val
        '''
        if primary_domain_val not in self.vertical_slices:
            raise Exception('Primary domain value not in this set.')

        _primary_membership = self.vertical_slices[primary_domain_val].domain_elements()
        return _primary_membership

    def secondary_grade(self, primary_domain_val, secondary_domain_val):
        '''
        returns the amplitude of a secondary membership function,
        that is the secondary grade.
        
        Reference:
        ----------
        J. M. Mendel and R. I. B. John, “Type-2 fuzzy sets made simple,” IEEE
        Trans. Fuzzy Systems, vol. 10, no. 2, pp. 117–127, Apr. 2002.

        Arguments:
        ----------
        primary_domain_val -- float, value of primary domain
        secondary_domain_val -- float, value of secondary domain

        Returns:
        --------
        secondary_grade -- float, value of secondary grade
        '''

        if secondary_domain_val > 1 or secondary_domain_val < 0:
            raise Exception('Invalid secondary domain value')

        if primary_domain_val not in self.primary_domain():
            raise Exception('Invalid primary domain value')

        secondary_grade = self.vertical_slices[primary_domain_val].elements()[secondary_domain_val]
        return secondary_grade

    def embedded_type2_sets_count(self):
        '''
        returns the number of embedded type-2 fuzzy sets that can be 
        generated from this general type-2 fuzzy set.
        
        Reference:
        ----------
        J. M. Mendel and R. I. B. John, “Type-2 fuzzy sets made simple,” IEEE
        Trans. Fuzzy Systems, vol. 10, no. 2, pp. 117–127, Apr. 2002.

        Arguments:
        ----------
        None

        Returns:
        --------
        embedded_count -- float, number of et2fs
        '''
        count = 1
        for primary_domain_val in self.primary_domain():
            count = count * self.vertical_slice(primary_domain_val).element_count()
        
        return count

    def embedded_type2_sets(self):
        '''
        Lists all the type 2 embedded sets of this gt2fs.
        List will contain tuples in the form
        [(sec_grade_1, sec_domain_1, pri_domain_1), ... , (sec_grade_n, sec_domain_n, pri_domain_n)]

        Reference:
        ----------
        J. M. Mendel and R. I. B. John, “Type-2 fuzzy sets made simple,” IEEE
        Trans. Fuzzy Systems, vol. 10, no. 2, pp. 117–127, Apr. 2002.

        Arguments:
        ----------
        None

        Returns:
        --------
        results -- list, containing embedded type 2 sets

        '''
        set_array = []
        primary_domain, secondary_domain, set_array = self.to_array_explicit()

        # get an index array
        index_array = np.indices(set_array.shape)[0]

        # create a list with the number of non zero elements in each vertical slice
        # i.e. the number of non zero element in each column
        col_gen = [index_array[set_array[:, x] > 0, x] for x in range((set_array.shape)[1])]

        # the number of columns is the number of elements in the domain
        domain_index = range(0, (set_array.shape)[1])

        results = []
        # for every combination of the column elemnets create a type 2 embedded fuzzy set
        for t in itertools.product(*col_gen):
            embedded = list(map(lambda i: (set_array[t[i]][i], secondary_domain[t[i]], primary_domain[i]) , domain_index))
            results.append(embedded)

        return results

    def _format_slice(self, vertical_slice):
        x = list(vertical_slice.elements.keys())
        y = list(vertical_slice.elements.values())

        def f(x, y): return "%0.4f" % (y)+'/'+"%0.2f" % (x)
        m = map(f, x, y)
        slice_rep = ' + '.join(m)
        return slice_rep

    def union(self, gt2fs):
        
        resultant_gt2fs = GeneralType2FuzzySet()

        primary_domain_a = self.primary_domain()
        primary_domain_b = gt2fs.primary_domain()

        primary_domain_union = list(set().union(primary_domain_a, primary_domain_b))

        for primary_domain_element in primary_domain_union:
            if primary_domain_element not in primary_domain_a:
                resultant_gt2fs.add_membership_function(primary_domain_element, gt2fs[primary_domain_element])
            elif primary_domain_element not in primary_domain_b:
                resultant_gt2fs.add_membership_function(primary_domain_element, self[primary_domain_element])
            else:
                resultant_gt2fs.add_membership_function(primary_domain_element, self[primary_domain_element].join(gt2fs[primary_domain_element]))

        return resultant_gt2fs

    def intersection(self, gt2fs):
        '''
        intersection  
        '''
        resultant_gt2fs = GeneralType2FuzzySet()

        primary_domain_a = self.primary_domain()
        primary_domain_b = gt2fs.primary_domain()

        primary_domain_union = list(set().union(primary_domain_a, primary_domain_b))

        for primary_domain_element in primary_domain_union:
            if primary_domain_element not in primary_domain_a:
                resultant_gt2fs.add_membership_function(primary_domain_element, gt2fs[primary_domain_element])
            elif primary_domain_element not in primary_domain_b:
                resultant_gt2fs.add_membership_function(primary_domain_element, self[primary_domain_element])
            else:
                resultant_gt2fs.add_membership_function(primary_domain_element, self[primary_domain_element].meet(gt2fs[primary_domain_element]))

        return resultant_gt2fs

    def complement(self):
        '''
        finds the complement of a general type 2 fuzzy set 
        '''
        resultant_gt2fs = GeneralType2FuzzySet()

        for primary_domain_element in self.primary_domain():
                    resultant_gt2fs.add_membership_function(primary_domain_element, self[primary_domain_element].negation())

        return resultant_gt2fs
