'''
type2fuzzy.type_reduction 

Type-2 Fuzzy Set Type reducers<br/>
Mendel-John.<br/>
Karnik-Mendel.<br/>
Hagras.<br/>
Partial Centroid.<br/>
'''

from type2fuzzy.type_reduction.gt2_mendeljohn_reducer import gt2_mendeljohn_reduce
from type2fuzzy.type_reduction.gt2_partialcentroid_reducer import gt2_partialcentroid_reduce
from type2fuzzy.type_reduction.it2_karnikmendel_reducer import it2_kernikmendel_reduce
from type2fuzzy.type_reduction.zslice_hagras_reducer import zslice_hagras_reduce

__all__ = ['gt2_mendeljohn_reduce', 'gt2_partialcentroid_reduce',
				'it2_kernikmendel_reduce', 'zslice_hagras_reduce']
