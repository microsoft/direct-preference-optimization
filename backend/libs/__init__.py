""" This file is used to add the parent directory to the python path
 so that the modules in the parent directory can be imported in the test files. """
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
