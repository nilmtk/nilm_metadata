from setuptools import setup, find_packages

setup(
    name='nilm_metadata',
    version='0.2.0',
    packages = find_packages(),
    install_requires = ['PyYAML'],
    description='Concatenate NILM metadata',
    author='Jack Kelly',
    author_email='jack.kelly@imperial.ac.uk',
    url='https://github.com/nilmtk/nilm_metadata',
#    long_description=open('README.md').read(),
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT',
        'Programming Language :: Python',
        'Topic :: Scientific/Engineering :: Mathematics',
    ],
    keywords='smartmeters power electricity energy analytics redd '
             'disaggregation nilm nialm'
)
