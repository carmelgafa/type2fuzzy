'''Crisp set implementation'''

class CrispSetException(Exception):
    '''Crisp set exception'''   

    def __init__(self, message):
        super().__init__(message)

class CrispSet:
    '''
    Implements a Crisp set
    todo: implement better properties

    '''
    def __init__(self, left_val=None, right_val=None):
        '''
        Creates a crisp set. Initially the set is empty with left and right 
        limit values set to None

        Arguments:
        ----------
        left_val -- float, the value of the left limit
        right_val -- float, the value of the right limit

        Raises:
        -------
        Exception if both limits are not None and if the left limit is
        greater than the right limit
        '''
        self._empty = True
        self._left_val = None
        self._right_val = None
        self._precision = 5

        if (left_val is not None) and (right_val is not None):
            if left_val > right_val:
                raise CrispSetException('ERROR: Incorrect crisp set limits. Left')
            self._empty= False
            self._left_val = left_val
            self._right_val = right_val

    @property
    def empty(self)->bool:
        '''
        Returns True if the set is empty
        '''
        return self._empty

    @property
    def left(self)->float:
        '''
        Returns the left limit of the set
        '''
        return self._left_val

    @left.setter
    def left(self, value:float)->None:
        '''
        Sets the left limit of the set. Check is bot left and right limit and sets the 
        set as not empty if both are not None
        '''

        if (self.right is not None) and (value is not None) and (value > self.right):
            raise CrispSetException('ERROR: invalid left value')

        self._left_val = value

        if (self._left_val is not None) and (self._right_val is not None):
            self._empty= False

        if (self._left_val is None) and (self._right_val is None):
            self._empty= True

    @property
    def right(self)->float:
        '''
        Returns the right limit of the set
        '''
        return self._right_val

    @right.setter
    def right(self, value:float)->None:
        '''
        Sets the right limit of the set. Check is bot left and right limit and sets the 
        set as not empty if both are not None
        '''
        if (self.left is not None) and (value is not None) and (value < self.left):
            raise CrispSetException('ERROR: invalid left value')

        self._right_val = value

        if (self._left_val is not None) and (self._right_val is not None):
            self._empty= False

        if (self._left_val is None) and (self._right_val is None):
            self._empty= True

    @property
    def mid(self)->float:
        '''
        Computes the mid point to the crisp set.
        
        Returns:
        --------
        mid_point -- float, the crisp set mid point

        Raises:
        -------
        Exception if the set is empty
        '''

        if self.left is None or self.right is None:
            raise CrispSetException('ERROR: Mid point cannot be found for this set.')

        if self._empty:
            raise CrispSetException('ERROR: Mid point cannot be found for an empty set.')

        mid_point = (self._left_val+self._right_val)/2
        return mid_point

    def union(self, crisp_set:'CrispSet'):
        '''performs the union operation between two crisp sets'''
        self._left_val = min(self._left_val, crisp_set.left)
        self._right_val = max(self._right_val, crisp_set.right)

    def __str__(self)->str:

        dec_places_formatter = f'%0.{self._precision}f'
        representation = ''
        if self._left_val == self._right_val:
            representation = f'[{ dec_places_formatter % self._left_val}]'
        else:
            representation = f'''[{ dec_places_formatter % self._left_val},
            {dec_places_formatter % self._right_val}]'''

        return representation

    def __repr__(self)->str:
        return f'{self.__class__.__name__}({str(self)})'
