from type2fuzzy.membership.type1fuzzyset import Type1FuzzySet

def mom_defuzzify(type1_set):
    '''
    Mean of Maxima defuzzification method

    References:
    -----------
    Mamdani, E. H., H. J. Efstathiou, and K. Sugiyama. 
    "Developments in fuzzy logic control." Decision and Control, 1984. 
    The 23rd IEEE Conference on. Vol. 23. IEEE, 1984.

    Arguments:
    ----------
    type1_set   -- Type1FuzzySet, the set whose centroid is to be computed

    Returns:
    --------
    centroid    -- float, the centroid of this set

    Raises:
    -------
    '''

    max_domain_elements = []
    max_dom = 0

    for domain_element in type1_set.domain_elements():

        if type1_set[domain_element] > max_dom:
            max_dom = type1_set[domain_element]
            max_domain_elements.clear()
            max_domain_elements.append(domain_element)
        elif type1_set[domain_element] == max_dom:
            max_domain_elements.append(domain_element)

    centroid = sum(max_domain_elements)/len(max_domain_elements)

    return centroid
