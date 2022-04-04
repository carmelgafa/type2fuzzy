# Type2Fuzzy Project

A type-2 fuzzy logic library providing:

1. Ways to define and work with general type-2 fuzzy sets
2. Ways to define and work with interval type-2 fuzzy sets
3. Ways to generate z-sliced sets from general type-2 fuzzy sets
4. Functions to perform wavy-slice type-reduction (Mendel-John) on general type-2 fuzzy sets
5. Functions to perform interval type-2 reduction (Karnik-Mendel)
6. Functions to perform partial-centroid type-reduction on general type-2 fuzzy sets
7. Functions to perform defuzzification of type-1 fuzzy sets
8. Tools to measure the performance of algorithms
9. Tools to plot general, interval and z-sliced type-2 fuzzy sets and type-1 fuzzy sets and more
10. Ways to define and work with type-1 fuzzy sets
11. Ways to define and work with type-1 linguistic variables

and more

All type2fuzzy wheels distributed on PyPI are BSD licensed.

Examples of how this library was used to work some famous type-2 fuzzy logic papers can be found [here](https://github.com/carmelgafa/type2fuzzy_examples).

## Website

The official website for this library can be found [here](http://t2fuzz.com).

## Change History

### version 0.1.49 - 04.04.2022

1. updated numpy and matplotlib versions

### version 0.1.48 - 04.04.2022

1. Renamed add_element in IntervalType2FuzzySet to add_element_from_crispset
2. Added add_element_from_values to IntervalType2FuzzySet

### version 0.1.43 - 11.03.2020

1. new version of documentation in html

### version 0.1.42 - 11.03.2020

1. type-1 fuzzy variable implemented __str__
2. type-1 fuzzy variable implemented get_set
3. type-1 fuzzy variable add_triangular_set returns created set

### version 0.1.41 - 10.03.2020

1. Type-1 fuzzy set has a name attribute and a name property
2. Type-1 fuzzy variable has a name attribute and a name property
3. Unit tests for above

### version 0.1.39 - 09.03.2020

1. added type-1 fuzzy variable

### version 0.1.37 - 07.03.2020

1. Fixed bugs in creation of type-1 fuzzy sets
2. Moved project in a virtualenv
3. Added more type-1 fuzzy set unit tests

### version 0.1.36 - 18.02.2020

1. Added generation of triangular type-1 sets unit test. Removed extended method

### version 0.1.35 - 18.02.2020

1. Fixed bug in generation of triangular type-1 sets

### version 0.1.34 - 18.11.2019

1. Ability to [create Interval Type-2 fuzzy sets having a gaussian function with fixed mean and fixed standard deviation](http://t2fuzz.com/type2fuzzy/membership/generate_it2fs.html) as per Karnik and Mendel 1996 - Karnik, Nilesh N., and Jerry M. Mendel. "Introduction to type-2 fuzzy logic systems." 1998 IEEE International Conference on Fuzzy Systems Proceedings. IEEE World Congress on Computational Intelligence (Cat. No. 98CH36228). Vol. 2. IEEE, 1998.
2. An experimental way to [define General Type-2 fuzzy sets through horizontal slices](http://t2fuzz.com/membership/type2fuzzy/generate_gt2mf.html)

### version 0.1.33 - 15.11.2019

1. Updated repo information

### version 0.1.32 - 15.11.2019

1. [Get domain limits for a type-1 fuzzy set](http://t2fuzz.com/type2fuzzy/membership/type1fuzzyset.html#type2fuzzy.membership.type1fuzzyset.Type1FuzzySet.domain_limits)

### version 0.1.31 - 12.11.2019

1. Added library [website](http://t2fuzz.com)
2. *Convert a gt2fs into an it2fs* -[An it2fs can be generated form a gt2fs by using from_general_type2_set](http://t2fuzz.com/type2fuzzy/membership/intervaltype2fuzzyset.html#type2fuzzy.membership.intervaltype2fuzzyset.IntervalType2FuzzySet.from_general_type2_set)
3. *Creation of it2fs as found in literature* - [Creation of it2fs as specified by Karnik and Mendel](http://t2fuzz.com/type2fuzzy/membership/generate_it2fs.html)
