#!/bin/bash
#python setup.py build
#jython ez_setup.py

# This is the current way to create a python 2.7 distribution from source, really
python setup.py bdist_egg

# TODO: have setup.py read version number from a text file or from github tag
tar cvf metadig-py-1.2.1.tar dist metadig
