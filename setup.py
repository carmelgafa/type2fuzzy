from setuptools import setup, find_packages
from distutils.core import setup
from os import path

DESCRIPTION = 'Library for type-2 fuzzy logic research'

VERSION = '0.1.52'

setup(
	author = 'Carmel Gafa',
	author_email = 'carmelgafa@gmail.com',
	name = 'type2fuzzy',
	version = VERSION,
	description = DESCRIPTION,
	long_description=open('README.md').read(),	
	long_description_content_type = 'text/markdown',
	classifiers=
	[
		'Development Status :: 3 - Alpha',
		'Intended Audience :: Developers',
		'Topic :: Software Development :: Build Tools',
		'License :: OSI Approved :: MIT License',
		'Programming Language :: Python :: 3',
		'Programming Language :: Python :: 3.4',
		'Programming Language :: Python :: 3.5',
		'Programming Language :: Python :: 3.6',
	],
	url = 'https://github.com/carmelgafa/type2fuzzy',
	packages = 
	[
		'type2fuzzy', 
		'type2fuzzy/membership',
		'type2fuzzy/display',
		'type2fuzzy/measurement',
		'type2fuzzy/type1_defuzzification',
		'type2fuzzy/type_reduction',
	],
	license='MIT',
	install_requires=
	[
		'numpy',
		'matplotlib',
	],
	keywords = 
	[
		'type-2 fuzzy',
		'type reduction', 
		'gt2fs', 
		'it2fs',
	],
)