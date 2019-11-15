from type2fuzzy.membership.type1fuzzyset import Type1FuzzySet

class SecondaryMembershipFunction(Type1FuzzySet):
	'''
	A secondary membership function is a vertical slice of mu(X=x, u)

	Reference:
	----------
	J. M. Mendel and R. I. B. John, “Type-2 fuzzy sets made simple,” IEEE
	Trans. Fuzzy Syst., vol. 10, no. 2, pp. 117–127, Apr. 2002.
	'''

	def __init__(self):
			super().__init__()
