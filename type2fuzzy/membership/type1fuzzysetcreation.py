'''Generation of type-1 fuzzy sets'''

from type2fuzzy.membership.type1fuzzyset import Type1FuzzySet

def create_triangular_set(
    res:int,
    pt_a:int,
    pt_b:int,
    pt_c:int,
    precision=3)->Type1FuzzySet:
    '''Creates a new triangular set'''

    t1fs = Type1FuzzySet(resolution=res)

    if pt_c == pt_b:
        for point in range(pt_a, pt_b+1):
            dom = (point - pt_a) / (pt_b - pt_a)
            t1fs.add_element(point, round(dom, precision))
    elif pt_a == pt_b:
        for point in range(pt_b, pt_c+1):
            dom = (pt_c - point) / (pt_c - pt_b)
            t1fs.add_element(point, round(dom, precision))
    else:
        for point in range(pt_a, pt_c+1):
            dom = max(
                min(
                    (point - pt_a) / (pt_b - pt_a),
                    (pt_c - point) / (pt_c - pt_b))
                , 0)
            t1fs.add_element(point, round(dom, precision))

    return t1fs

def create_gaussian_set():
    '''Creates a new gaussian set'''
    pass

if __name__ == '__main__':
    print(create_triangular_set(res=10, pt_a=0, pt_b=5, pt_c=10))
