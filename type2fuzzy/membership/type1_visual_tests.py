''' Visual tests for type 1 fuzzy sets '''
from type1_fuzzyset_creation import create_triangular_set
import matplotlib.pyplot as plt


def test_type1_fuzzyset_intersection():
    '''
    Tests the intersection of two type 1 fuzzy sets.
    
    The sets are t1fs = [0, 0, 10] and t2fs = [0, 10, 10]
    The intersection is computed and plotted, along with the two original sets.
    '''
    t1fs = create_triangular_set(idx_a=0, idx_b=0, idx_c=10, resolution=11)
    t2fs = create_triangular_set(idx_a=0, idx_b=10, idx_c=10, resolution=11)
    t3fs = t1fs.intersection(t2fs)

    t3fs.plot_set()
    t2fs.plot_set()
    t1fs.plot_set()

    plt.show()


if __name__ == '__main__':
    test_type1_fuzzyset_intersection()
