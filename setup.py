from setuptools import setup
from setuptools import find_packages

long_description = '''
Metadig provides tools that can be used by the MetaDIG Quality Engine
'''
#with open("README.md", "r") as fh:
#long_description = fh.read()

setup(name='metadig',
      version='1.0.0',
      author="Peter Slaughter",
      author_email="slaughter@nceas.ucsb.edu",
      description='Metadig Quality Engine Python Library',
      long_description=long_description,
      url='https://github.com/NCEAS/metadig-py',
      download_url='https://github.com/NCEAS/metadig/tarball/1.0.0',
      license='Apache-2',
      packages=find_packages(),
      install_requires=[
                        #'scipy>=0.14',
      ],
      classifiers=[
          'Development Status :: 1 - Development/Unstable',
          'License :: OSI Approved :: Apache 2 ',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.6',
          'Topic :: Software Development :: Libraries',
          'Topic :: Software Development :: Libraries :: Python Modules'
      ]
)
