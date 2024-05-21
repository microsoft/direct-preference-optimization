""" This file is used to import the search_vector_index_service module from the backend folder """
import sys
import os
testdir = os.path.dirname(__file__)
SRCDIR = '../../backend'
sys.path.insert(0, os.path.abspath(os.path.join(testdir, SRCDIR)))
