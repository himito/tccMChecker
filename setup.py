from setuptools import setup, find_packages
from pip.req import parse_requirements
from codecs import open
from os import path

basedir = path.abspath(path.dirname(__file__))

readme_path = path.join(basedir, 'README.rst')
requirements_path = path.join(basedir, 'requirements.txt')

# Get the long description from the README file
with open(readme_path, encoding='utf-8') as f:
    long_description = f.read()

# Get require packages from requirements.txt
install_reqs = parse_requirements(requirements_path, session=False)
requirements = [str(r.req) for r in install_reqs]

setup(
    name='tccMChecker',
    version='1.0.0',
    license='GPLv2',

    description='Model Checker for the tcc calculus',
    long_description=long_description,
    url='https://github.com/himito/tccMChecker',

    # Author details
    author='Jaime Arias',
    author_email='jaime.arias@inria.fr',

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Topic :: Scientific/Engineering',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
    ],

    keywords='model-checking process-calculus',

    packages=find_packages(exclude=['examples', 'docs', 'tests']),
    install_requires=requirements,
    zip_safe=False,
)

