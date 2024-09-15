'''Generation of type-1 fuzzy sets'''

from type1fuzzyset import Type1FuzzySet

def create_triangular_set(
    idx_a:int,
    idx_b:int,
    idx_c:int,
    resolution=100,
    precision=3)->Type1FuzzySet:
    '''Creates a new triangular set'''

    print(idx_a, idx_b, idx_c)

    t1fs = Type1FuzzySet(resolution=resolution)

    if (idx_a < 0) or (idx_b < 0) or (idx_c < 0):
        raise ValueError('Point values must be non-negative')

    if (idx_a > idx_b) or (idx_b > idx_c):
        raise ValueError('Point values must be in increasing order')

    if (idx_a >= resolution) or (idx_b >= resolution) or (idx_c >= resolution):
        raise ValueError('Point values must be less than resolution')

    if idx_c == idx_b:
        for point in range(idx_a, idx_b+1):
            dom = (point - idx_a) / (idx_b - idx_a)
            t1fs.add_element(point, round(dom, precision))
    elif idx_a == idx_b:
        for point in range(idx_b, idx_c):
            dom = (idx_c - point) / (idx_c - idx_b)
            t1fs.add_element(point, round(dom, precision))
    else:
        for point in range(idx_a, idx_c):
            dom = max(
                min(
                    (point - idx_a) / (idx_b - idx_a),
                    (idx_c - point) / (idx_c - idx_b))
                , 0)
            t1fs.add_element(point, round(dom, precision))

    return t1fs

def create_gaussian_set():
    '''Creates a new gaussian set'''
    pass

if __name__ == '__main__':
    import matplotlib.pyplot as plt

    tri_set_a = create_triangular_set(idx_a=0, idx_b=5, idx_c=10, resolution=11)
    tri_set_a.plot_set()

    # create a set with idx_a and idx_b both equal to 0
    tri_set_b = create_triangular_set(idx_a=0, idx_b=0, idx_c=5, resolution=11)
    tri_set_b.plot_set()

    # create a set with idx_b and idx_c both equal to 9
    tri_set_c = create_triangular_set(idx_a=5, idx_b=10, idx_c=10, resolution=11)
    tri_set_c.plot_set()

    plt.show()
